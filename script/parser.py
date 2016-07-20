# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 16:42:39 2016

@author: aedouard
@author: jplu
"""

import pandas
import json
import os
import re
import numpy
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import math
import datetime
import dateutil

def parse_tweets(folder):
    for path,dirs,files in os.walk(folder):
        for filename in files:    
            if filename.endswith(".json"):
                groupe_match = re.search('Groupe_([A-Z])', path)
                language_match = re.search('([a-z]{2}$)', path)
                
                if (groupe_match and language_match):
                    result_path = 'results/time_charts/' + groupe_match.group() + '/' + language_match.group()

                    if (not os.path.exists(result_path)):
                        os.makedirs(result_path)

                    print(path + '/' + filename)
                    with open(path + '/' + filename) as f:
                        count_tweets = 0
                        count_retweets = 0
                        count_unique_tweets = 0
                        tweets = []

                        for line in f:
                            try:
                                tweet = json.loads(line)
                                
                                if 'created_at' in tweet and 'retweeted_status' not in tweet:
                                    tweets.append(tweet['created_at'])
                                    count_tweets += 1
                                    count_unique_tweets += 1
                                else:
                                    count_retweets += 1
                                    count_tweets += 1

                            except: 
                                print("Issue with JSON format")
                        per_minute = create_time_bucketing(tweets)
                        lowest_confidence_interval_series = compute_lowest_confidence_interval(per_minute, tweets)
                        linear_regression_series = compute_linear_regression(per_minute)
                        create_image(per_minute, lowest_confidence_interval_series, linear_regression_series, result_path, filename)
                        linear_regression_list = linear_regression_coordinates(linear_regression_series, per_minute)
                        lowest_confidence_interval = math.floor(numpy.mean(per_minute.as_matrix())) - math.floor(numpy.std(per_minute.as_matrix()))
                        lowest_confidence_interval_timestamps = find_spikes_with_lowest_confidence_interval(lowest_confidence_interval, per_minute)
                        linear_regression_timestamps = find_spikes_with_linear_regression(linear_regression_list, per_minute)
                        
                        filtering_tweets(lowest_confidence_interval_timestamps, path + '/' + filename, result_path + '/' + filename, count_tweets, count_retweets, count_unique_tweets, "_lowest_confidence_interval")
                        filtering_tweets(linear_regression_timestamps, path + '/' + filename, result_path + '/' + filename, count_tweets, count_retweets, count_unique_tweets, "_linear_regression")

def filtering_tweets(lowest_confidence_interval_timestamps, filepath, fileresultpath, count_tweets, count_retweets, count_unique_tweets, method):
    parts = filepath.split('/')
    group = parts[len(parts)-3].split('_')[1]
    filename = parts[len(parts)-1]
    team1 =  filename.split('_')[0]
    team2 =  filename.split('_')[1]
    new_total = 0
    filtered_out = 0
    good_tweets = []

    with open(filepath) as f:
        for line in f:
            tweet = json.loads(line)

            if 'created_at' in tweet and 'retweeted_status' not in tweet:
                idx = int(dateutil.parser.parse(tweet['created_at']).timestamp())
                
                if idx in lowest_confidence_interval_timestamps:
                    tweet['time_frame'] = idx
                    good_tweets.append(tweet)
                    new_total += 1
                else:
                    filtered_out += 1
    
    stat = {
        'team1':team1, 
        'team2':team2,
        'group':group,
        'total': count_tweets,
        'not_retweets': count_unique_tweets,
        'filtered_out': filtered_out,
        'new_total:': new_total,
        'retweets': count_retweets
    }

    with open(fileresultpath.split('.')[0] + method + "_stats.json", 'w') as stats_file:    
        json.dump(stat, stats_file, indent=4)
    with open(fileresultpath.split('.')[0] + method + ".json", 'w') as result_file: 
            json.dump(good_tweets, result_file, indent=4)

def find_spikes_with_linear_regression(linear_regression_list, per_minute):
    tuples = zip(per_minute.index.tolist(), per_minute.tolist(), linear_regression_list)
    timestamps = []

    for i,j,k in tuples:
        if j >= k:
            timestamps.append(int(datetime.datetime.strptime(str(i), '%Y-%m-%d %H:%M:%S').timestamp()))
    
    return timestamps

def find_spikes_with_lowest_confidence_interval(lowest_confidence_interval, per_minute):
    tuples = zip(per_minute.index.tolist(), per_minute.tolist())
    timestamps = []

    for i,j in tuples:
        if j >= lowest_confidence_interval:
            timestamps.append(int(datetime.datetime.strptime(str(i), '%Y-%m-%d %H:%M:%S').timestamp()))
    
    return timestamps

def linear_regression_coordinates(linear_regression, per_minute):
    y = list(map(math.floor, linear_regression['linear regression'].tolist()))
    x = list(map(lambda x:per_minute.index.tolist().index(x), linear_regression.index.tolist()))
    coordinates = list(zip(x, y))
    b = coordinates[0][1]
    a = (coordinates[1][1] - coordinates[0][1]) / (coordinates[1][0] - coordinates[0][0])
    
    return list(map(lambda x: math.floor(a*per_minute.index.tolist().index(x)+b), per_minute.index.tolist()))

def create_time_bucketing(tweets):
    ones = [1] * len(tweets)
    idx = pandas.DatetimeIndex(list(map(lambda x:x + pandas.tseries.timedeltas.to_timedelta(2, unit='h'), pandas.DatetimeIndex(tweets).tolist())))
    series = pandas.Series(ones, index=idx)
    
    return series.resample('1Min').sum().fillna(0)

def compute_lowest_confidence_interval(per_minute, tweets):
    lowest_confidence_interval = [numpy.mean(per_minute.as_matrix()) - numpy.std(per_minute.as_matrix())] * len(tweets)
    idx = pandas.DatetimeIndex(list(map(lambda x:x + pandas.tseries.timedeltas.to_timedelta(2, unit='h'), pandas.DatetimeIndex(tweets).tolist())))
    lowest_confidence_interval_series = pandas.Series(lowest_confidence_interval, index=idx)
    
    return pandas.DataFrame({'lowest confidence interval' : lowest_confidence_interval_series.resample('1Min').max().fillna(numpy.mean(per_minute.as_matrix()) - numpy.std(per_minute.as_matrix()))})

def compute_linear_regression(per_minute):
    df = per_minute.reset_index()
    df.rename(columns={0: 'values'}, inplace=True)
    lm = smf.ols(formula='values ~ index', data=df).fit()
    X_new = pandas.DataFrame({'index': [df['index'].min(), df['index'].max()]})
    preds = lm.predict(X_new)
    
    return pandas.DataFrame({'linear regression' : pandas.Series(preds.tolist(), index=[df['index'].min(), df['index'].max()])})

def create_image(per_minute, lowest_confidence_interval, linear_regression, result_path, filename):
    ax = pandas.DataFrame({'tweets per minute' : per_minute}).plot()
    ax = lowest_confidence_interval.plot(ax = ax)
    ax = linear_regression.plot(ax = ax)

    ax.set_xlabel("Time")
    ax.set_ylabel("Number of Tweets")
    
    fig = ax.get_figure()
    
    fig.savefig(result_path + '/' + filename.split('.')[0] + ".png")
    plt.close('all')

def main():
    folder  = '/Users/jplu/dev/HackaTAL2016/Tweets/Matchs/train_euro2016'
    parse_tweets(folder)

if __name__ == '__main__':
    main()