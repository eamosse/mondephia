# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 16:42:39 2016

@author: aedouard
"""

import pandas
import json
import vincent
 
dates_ITAvWAL = []
# f is the file pointer to the JSON data set
f = open('/Users/aedouard/Dropbox/_dev/HackaTAL2016/Tweets/Matchs/train_euro2016/Groupe_A/en/France_Albanie_2016-06-15_21h_en.json')
i = 0 
for line in f:
    i = i+1
    tweet = json.loads(line)
    print(tweet)
    dates_ITAvWAL.append(tweet['created_at'])
    
# a list of "1" to count the hashtags
ones = [1]*len(dates_ITAvWAL)
# the index of the series
idx = pandas.DatetimeIndex(dates_ITAvWAL)
# the actual series (at series of 1s for the moment)
ITAvWAL = pandas.Series(ones, index=idx)
# Resampling / bucketing
per_minute = ITAvWAL.resample('1Min', how='sum').fillna(0)  

time_chart = vincent.Line(ITAvWAL)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.to_json('time_chart.json')     
    
"""       
    # let's focus on hashtags only at the moment
    terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
    # track when the hashtag is mentioned
    if '#itavwal' in terms_hash:
        dates_ITAvWAL.append(tweet['created_at'])
 
# a list of "1" to count the hashtags
ones = [1]*len(dates_ITAvWAL)
# the index of the series
idx = pandas.DatetimeIndex(dates_ITAvWAL)
# the actual series (at series of 1s for the moment)
ITAvWAL = pandas.Series(ones, index=idx)
 
# Resampling / bucketing
per_minute = ITAvWAL.resample('1Min', how='sum').fillna(0)
"""