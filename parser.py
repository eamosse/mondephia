# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 16:42:39 2016

@author: aedouard
"""

import pandas
import json
import vincent
import utils
dates_ITAvWAL = []
from dateutil.parser import parse
from datetime import datetime
# f is the file pointer to the JSON data set
f = open('/Users/aedouard/Dropbox/_dev/HackaTAL2016/Tweets/Matchs/train_euro2016/Groupe_E/fr/Belgique_Italie_2016-06-13_21h_fr.json')
i = 0 
for line in f:
    tweet = json.loads(line)
    #print(tweet)
    if 'created_at' in tweet:
        dates_ITAvWAL.append(tweet['created_at'])
    
# a list of "1" to count the hashtags
ones = [1]*len(dates_ITAvWAL)
# the index of the series
idx = pandas.DatetimeIndex(dates_ITAvWAL)
# the actual series (at series of 1s for the moment)
ITAvWAL = pandas.Series(ones, index=idx)
# Resampling / bucketing
per_minute = ITAvWAL.resample('30S').sum().fillna(0)  

time_chart = vincent.Line(per_minute)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.to_json('time_chart.json')    
utils.process('time_chart.json')

        
    