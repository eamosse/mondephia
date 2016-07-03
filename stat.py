# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 00:23:56 2016

@author: aedouard
"""

import json 
from dateutil.parser import parse
from datetime import datetime

with open('time_chart_1.json') as data_file:    
        data = json.load(data_file)
        previous = None
        res = []
        seuil = data['moyenne']- data['ecart_type']/2
        for d in data['data']:
            if d['val'] < seuil :
                previous = d 
                continue
            if not previous :
                previous = d
            if d['val'] >= previous['val'] :
                res.append(d)
                previous = d
        newlist = sorted(res, key=lambda k: k['idx'])
        for d in newlist:
            
        print (res)
        