# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 20:32:09 2016

@author: aedouard
"""
import json 
import numpy as np
from datetime import datetime
from scipy.stats import linregress
import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(text1, text2):
    vec1 = text_to_vector(text1)
    vec2 = text_to_vector(text2)
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator:
        return 0.0
    else:
         return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

text1 = 'This is a foo bar sentence .'
text2 = 'This is a foo bar sentence if you might say that'

cosine = get_cosine(text1, text2)

print ('Cosine:', cosine)

def moyenne(tableau):
    return sum(tableau, 0.0) / len(tableau)

def variance(tableau):
    m=moyenne(tableau)
    return moyenne([(x-m)**2 for x in tableau])

def ecartype(tableau):
    return variance(tableau)**0.5

def linearReg(file):
    
    with open(file) as data_file:    
        data = json.load(data_file)
        ds = np.zeros(shape=(len(data['data'][0]['values']),2))
        for i,d in enumerate(data['data'][0]['values']):
            ds
            np.append(ds,[np.datetime64(datetime.fromtimestamp(d['idx']/1000)),d['idx']])
        #ds = [[d['val'],d['idx']] for d in data['data'][0]['values'] ]
    #x = ds[:,0]
    
    x = ds [:,0]
    y = ds [:,1]
    print(ds)
    parametres = np.polyfit(x, y, 1)
    print(parametres)
    
    

def process(file,save_to):
    dd = {}
    
    with open(file) as data_file:    
        data = json.load(data_file)
        ds = [int(d['val']) for d in data['data'][0]['values'] ]
        ec = ecartype(ds)
        print (ec)
        dd = {'data' :  data['data'][0]['values'], 'ecart_type' : ec, 'moyenne' : moyenne(ds)}
        
    #print(dd)
    with open(save_to, 'w+') as data_file: 
        json.dump(dd, data_file, indent=4)
        
#linearReg('time_chart.json')
