# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 00:23:56 2016

@author: aedouard
"""

import json 
from dateutil.parser import parse
from datetime import datetime

def findSpike():
    with open('time_chart_1.json') as data_file:    
            data = json.load(data_file)
            res = []
            seuil = data['moyenne']- data['ecart_type']/2
            for d in data['data']:
                if d['val'] > seuil :
                    res.append(d)
                    """
                    previous = d 
                    continue
                if not previous :
                    previous = d
                if d['val'] >= previous['val'] :
                    res.append(d)
                    previous = d
                    """
            newlist = sorted(res, key=lambda k: k['idx'])
            for d in newlist:
                date = datetime.fromtimestamp(d['idx']/1000)
                d['idx'] = int(str(date.hour)+''+(str(date.minute) if date.minute > 10 else '0' + str(date.minute)))
                #int(str(datetime.fromtimestamp(d['idx']/1000).hour) + "" + str(datetime.fromtimestamp(d['idx']/1000).minute))
            print (res)
            return [r['idx'] for r in res] 
            

def findTweets(file): 
    spikes = findSpike()
    data = {}
    spams = []
    f = open(file)
    for line in f:
        tweet = json.loads(line)
        #print(tweet)
        if 'created_at' in tweet and 'retweeted_status' not in tweet:
            d = parse(tweet['created_at'])
            idx = int(str(d.hour)+''+(str(d.minute) if d.minute > 10 else '0' + str(d.minute)))
            if idx in spikes:
                if not str(idx) in data:
                    data[str(idx)] = []
                data[str(idx)].append(tweet['text'])
            else:
                spams.append(tweet['text'])
    with open('spams.json', 'w+') as data_file: 
            json.dump(spams, data_file, indent=4)
    return data