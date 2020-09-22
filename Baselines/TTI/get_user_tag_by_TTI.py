"""
Generate user interest tags by TTI

Input:
uid_list(list):[uid], uid: the user id of tager users.
text(dictonary):{wid:[word]}, microblog texts after split in training set.
tfidf(dictonary):{word:tf-idf weight}.
win: the size of windows for TextRank.

Output:
tags(dictonary):{tag:weight} user interest tags and their weights.
"""
import math
import numpy as np 

def init_weight():
    weight = {}
    for w in text.keys():
        n = len(text[w])
        for i in range(0,n):
            word = text[w][i]
            if word not in weight:
                weight[word] = {}
            for j in range(max(0,i-win+1),min(i+win,n)):
                if i==j:
                    continue
                word2 = text[w][j]
                if word2 not in weight[word]:
                    weight[word][word2] = 0
                weight[word][word2] += 1
                if word2 not in weight:
                    weight[word2] = {}
                if word not in weight[word2]:
                    weight[word2][word] = 0
                weight[word2][word] +=1
    return weight

def init_out(weight):
    out = {}
    for w1 in tfidf.keys():
        out[w1] = 0
        for w2 in weight[w1]:
            out[w1] += weight[w1][w2]
    return out

def textRank():
    d = 0.85  #damping factor
    iterator = 100  
    weight = init_weight()
    out = init_out(weight)
    value = {}
    for item in tfidf.keys():
        value[item] = (1-d) * tfidf[item]
    v = len(tfidf)
    for i in range(0,iterator):
        for item in weight.keys():
            sum = 0 
            for word in weight[item]:
                sum += (weight[item][word] * value[word])/out[word]
            value[item] = (1-d)/v  + d * sum * (tfidf[item] + 1 )
    return value

if __name__ == '__main__':
    #load uid_list
    for uid in uid_list:
        #load text,tfidf
        tti = textRank() ##generate keywords and their weights by TextRank with TF-IDF