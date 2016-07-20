# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 00:23:56 2016

@author: aedouard
"""

import json 
from dateutil.parser import parse
from datetime import datetime

def findSpike(file):
    print(file)
    with open(file) as data_file:    
            data = json.load(data_file)
            res = []
            seuil = data['moyenne']- data['ecart_type']/2
            for d in data['data']:
                if d['val'] > seuil :
                    res.append(d)
            newlist = sorted(res, key=lambda k: k['idx'])
            for d in newlist:
                date = datetime.fromtimestamp(d['idx']/1000)
                d['idx'] = int(str(date.hour+2)+''+(str(date.minute) if date.minute >= 10 else '0' + str(date.minute)))
                
            return [r['idx'] for r in res] 
            

def findTweets(file,fileName, fileName1): 
    spikes = findSpike(fileName1)
    data = {}
    spams = []
    alls = []
    
    parts = file.split('/')
    print(parts)
    group = parts[len(parts)-3].split('_')[1]
    part = parts[len(parts)-1]
    team1 =  part.split('_')[0]
    team2 =  part.split('_')[1]
    
    stats = []
    with open('stats.json') as data_file:    
        stats = json.load(data_file)
                
    stat = {
    'team1':team1, 
    'team2':team2,
    'group':group,
    'relevant': 0, 
    'not_relevant':0, 
    'retweets': 0}
    f = open(file)
    for line in f:
        try:
            tweet = json.loads(line)
            #print(tweet)
            if 'created_at' in tweet and 'retweeted_status' not in tweet:
                d = parse(tweet['created_at'])
                idx = int(str(d.hour+2)+''+(str(d.minute) if d.minute >= 10 else '0' + str(d.minute)))
                if idx in spikes:
                    if not str(idx) in data:
                        data[str(idx)] = []
                    data[str(idx)].append(tweet['text'])
                    tweet['time_frame'] = idx
                    alls.append(tweet)
                    stat['relevant'] = stat['relevant'] + 1
                else:
                    spams.append(tweet['text'])
                    stat['not_relevant'] = stat['not_relevant'] + 1
            else:
                stat['retweets'] = stat['retweets'] + 1
        except :
            print('ignorer')
    stats.append(stat)    
    with open('stats.json', 'w+') as data_file: 
            json.dump(stats, data_file, indent=4)
    with open(fileName, 'w+') as data_file: 
            data = {'frames' : spikes, 'tweets': alls}
            json.dump(data, data_file, indent=4)
    
    return data