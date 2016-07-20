# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:41:49 2016

@author: aedouard
"""

import json
from TweetPreprocessor import TweetPreprocessor
import nltk
import utils
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE
import bokeh.plotting as bp
from bokeh.models import HoverTool, BoxSelectTool
from bokeh.plotting import figure, show, output_file
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import lda
from nltk.stem.porter import PorterStemmer
import csv
from sklearn.feature_extraction.text import CountVectorizer
from itertools import groupby
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import string
from collections import Counter
from nltk.corpus import stopwords

colormap = np.array([
        "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c", 
        "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5", 
        "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f", 
        "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5", 
        
        "#6c4c56", "#8c8caa", "#8ba097", "#cd1076", "#00af7e", 
        "#c1fdd5", "#97a08b", "#9b9b9b", "#6a5ed6", "#5f5c4a", 
        "#eae6de", "#8f8fa7", "#c39797", "#ffd9df", "#1E90FF", 
        "#8B1A1A", "#8B3626", "#FF4500", "#FFC125", "#CDCD00", 
        
        "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c", 
        "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5", 
        "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f", 
        "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5", 
        
        "#6c4c56", "#8c8caa", "#8ba097", "#cd1076", "#00af7e", 
        "#c1fdd5", "#97a08b", "#9b9b9b", "#6a5ed6", "#5f5c4a", 
        "#eae6de", "#8f8fa7", "#c39797", "#ffd9df", "#1E90FF", 
        "#8B1A1A", "#8B3626", "#FF4500", "#FFC125", "#CDCD00"
    ])

def loadTweets(fileName):
    tweets = None
    results = {}
    with open(fileName) as f:
        tweets = json.load(f)
    for key, group in groupby(tweets['tweets'], lambda x: x['time_frame']):
        if  str(key) not in results :
            results[str(key)] = [] 
        for tweet1 in group:
            results[str(key)].append(tweet1)
        
        """
        print("Key",key)
        for tweet1 in group:
            must_add = True
            for tweet2 in group:
                print(tweet1['id'] , tweet2['id'],tweet1['id'] == tweet2['id'])
                if tweet1['id'] == tweet2['id']:
                    print ('blab')
                    continue
                #print ('blob')
                break                
                cosine = utils.get_cosine(tweet1['text'],tweet2['text'])
                #print (tweet1['id'] , tweet2['id'], cosine)
                #print(cosine,cosine>0.9)
                if  cosine > 0.9:
                    must_add = False 
                   # print(tweet1['text'], tweet2['text'], cosine)
                    break
            #print("just break", must_add)
            if must_add :
                #print("adding", len(results[str(key)]))
                results[str(key)].append(tweet1)
        break
    #print(results) 
    """          
    return results
    
def preprocess(fileName):
    tknzr = TweetTokenizer()
    #nltk.download('stopwords')
    stop = stopwords.words('english')
    #stop += [ '<url>',  '<user>', '<repeat>', '<elong>']
    #the tweet processor 
    tweet_processor = TweetPreprocessor()
    #load the tweets 
    """tweets_file = '/Users/aedouard/Documents/_dev/these/data/websummit_dump_20151106155110'
    with open(tweets_file) as f:
        tweets = json.load(f)
    """
    tweets = loadTweets(fileName)
    #tweet_texts_processed = []
    #tweet_texts = []
    new_data = {}
    found = 0
    #stemming 
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    #print(tweets.keys())
    #print('\n'.join([t['text'] for t in tweets['1639']]))
    #sys.exit(1)
    for key in tweets.keys():
        d = tweets[key]
        new_data[key] = []
        print (key, len(d))
        for i  in range(len(d)):
            add = True
            tweet1 = d[i]
            for j in range(0, i):
                tweet2 = d[j]
                cosine = utils.get_cosine(tweet1['text'],tweet2['text'])
                if cosine > 0.9:
                    add = False
                    found = found+1
                    break;
            if add:
                
                no_punctuation = tweet1["text"].translate(string.punctuation)
                tokens = nltk.word_tokenize(no_punctuation)
                #count = Counter(tokens)
                filtered = [w for w in tokens if not w in stopwords.words('english')]
                #parts = tknzr.tokenize(tweet_processor.preprocess(tweet1["text"]))
               
                #clean = [i for i in parts if i not in stop]
                 
                texts = [p_stemmer.stem(i) for i in filtered]
                tweet1["processed"] = texts
                new_data[key].append(tweet1)
               

    return new_data    
    #tweet_texts = [tweet["text"] for tweet in tweets] # list of all tweet texts
    #tweet_texts_processed = [str.join(" ", tweet["processed"]) for tweet in tweets] # list of pre-processed tweet texts
    #originals = [tweet["original"] for tweet in tweets]
    #return {'text':tweet_texts, 'processed':tweet_texts_processed, 'extras':tweets }#{'originals':originals, 'ids':[tweet["tweet_id"] for tweet in tweets]}}
    
def tsne_clustering(data,vz):
    output_file("lines.html", title="line plot example")
    plot_tfidf = bp.figure(plot_width=900, plot_height=700, title="Web Summit 2015 tweets (tf-idf)",
    tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
    x_axis_type=None, y_axis_type=None, min_border=1)
    tfidf = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))
    svd = TruncatedSVD(n_components=50, random_state=0)
    svd_tfidf = svd.fit_transform(vz[:10000])
    svd_tfidf.shape
    tsne_tfidf = tsne_model.fit_transform(svd_tfidf)
    
    tsne_tfidf.shape
    plot_tfidf.scatter(x=tsne_tfidf[:,0], y=tsne_tfidf[:,1],
                    source=bp.ColumnDataSource({
                        "tweet": data['text'][:10000], 
                        "processed": data['processed'][:10000]
                    }))

    hover = plot_tfidf.select(dict(type=HoverTool))
    hover.tooltips={"tweet": "@tweet (processed: \"@processed\")"}
    show(plot_tfidf)

def kmeans(tsne_model, vz,data,cat):
    num_clusters = 2
    kmeans_model = MiniBatchKMeans(n_clusters=num_clusters, init='k-means++', n_init=1, 
                             init_size=1000, batch_size=1000, verbose=False, max_iter=1000)
    kmeans = kmeans_model.fit(vz)
    kmeans_clusters = kmeans.predict(vz)
    kmeans_distances = kmeans.transform(vz)
    sorted_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(num_clusters):
        print("Cluster %d:" % i, end='')
        for j in sorted_centroids[i, :10]:
            print(' %s' % terms[j], end='')
        print()
    tsne_kmeans = tsne_model.fit_transform(kmeans_distances[:10000])
   
    output_file(cat+".html", title="Euro 2016")
    plot_kmeans = bp.figure(plot_width=900, plot_height=700, title="Euro 2016 (k-means)",
        tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
        x_axis_type=None, y_axis_type=None, min_border=1)
    
    plot_kmeans.scatter(x=tsne_kmeans[:,0], y=tsne_kmeans[:,1], 
                        color=colormap[kmeans_clusters][:10000], 
                        source=bp.ColumnDataSource({
                            "tweet": data['text'][:10000], 
                            "processed": data['processed'][:10000],
                            "cluster": kmeans_clusters[:10000]
                        }))
    hover = plot_kmeans.select(dict(type=HoverTool))
    hover.tooltips={"tweet": "@tweet (processed: \"@processed\" - cluster: @cluster)"}
    show(plot_kmeans)

def scores(tweets) :
    tweets = ' '.join(tweets)
    no_punctuation = tweets.translate(string.punctuation)
    tokens = nltk.word_tokenize(no_punctuation)
    #count = Counter(tokens)
    filtered = [w for w in tokens if not w in stopwords.words('english')]
    count = Counter(filtered)
    print (count.most_common(10))
   # print (tokens)
    
def topics_lda(data, cat):
    
    cvectorizer = CountVectorizer(min_df=4, max_features=10000, stop_words='english')
    cvz = cvectorizer.fit_transform(data['processed'])
    
    n_topics = 5
    n_iter = 1000
    lda_model = lda.LDA(n_topics=n_topics, n_iter=n_iter)
    X_topics = lda_model.fit_transform(cvz)  
    n_top_words = 10
    topic_summaries = []
    
    topic_word = lda_model.topic_word_  # get the topic words
    vocab = cvectorizer.get_feature_names()
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        topic_summaries.append(' '.join(topic_words))
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    tsne_lda = tsne_model.fit_transform(X_topics[:10000])
    doc_topic = lda_model.doc_topic_
    lda_keys = []
    for i, tweet in enumerate(data['extras']):
        lda_keys += [doc_topic[i].argmax()]
    
    output_file(cat+".html", title="Websumbimt kmeans")
    plot_lda = bp.figure(plot_width=900, plot_height=700, title="Event Detection (LDA)",
    tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
    x_axis_type=None, y_axis_type=None, min_border=1)

    plot_lda.scatter(x=tsne_lda[:,0], y=tsne_lda[:,1], 
                     color=colormap[lda_keys][:10000], 
                     source=bp.ColumnDataSource({
                        "tweet": tweet_texts[:10000], 
                        "processed": tweet_texts_processed[:10000],
                        "topic_key": lda_keys[:10000]
                    }))
    hover = plot_lda.select(dict(type=HoverTool))
    hover.tooltips={"tweet": "@tweet (processed: \"@processed\" - topic: @topic_key)"}
    show(plot_lda)   
    
    
data = preprocess('/Users/aedouard/Dropbox/_dev/HackaTAL2016/result/Groupe_A/en/Roumanie_Suisse_2016-06-15_18h_en_relevant.json')
for key in data.keys():
    tweet_texts = [d["text"] for d in data[key]]
    tweet_texts_processed = [str.join(" ",d["processed"]) for d in data[key]]
    to_processed =  {'text':tweet_texts, 'processed':tweet_texts_processed, 'extras':data[key] }
    vectorizer = TfidfVectorizer(min_df=4, max_features = 10000)
    #print(len(tweet_texts_processed))
    if len(tweet_texts_processed) > 10:
        #scores (tweet_texts_processed)
        #continue
        vz = vectorizer.fit_transform(tweet_texts_processed)
        tsne_model = TSNE(n_components=2, verbose=1, random_state=0)
        kmeans(tsne_model,vz,to_processed, str(key))
    #topics_lda(to_processed,str(key))    
