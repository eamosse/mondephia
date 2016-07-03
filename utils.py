# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 20:32:09 2016

@author: aedouard
"""
import json 


def moyenne(tableau):
    return sum(tableau, 0.0) / len(tableau)

def variance(tableau):
    m=moyenne(tableau)
    return moyenne([(x-m)**2 for x in tableau])

def ecartype(tableau):
    return variance(tableau)**0.5

def process(file):
    dd = {}
    
    with open(file) as data_file:    
        data = json.load(data_file)
        ds = [d['val'] for d in data['data'][0]['values'] ]
        ec = ecartype(ds)
        print (ec)
        dd = {'data' :  data['data'][0]['values'], 'ecart_type' : ec, 'moyenne' : moyenne(ds)}
        
    print(dd)
    with open('time_chart_1.json', 'w+') as data_file: 
        json.dump(dd, data_file, indent=4)
        
process('time_chart.json')
