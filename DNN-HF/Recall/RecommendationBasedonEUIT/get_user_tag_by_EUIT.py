"""
Generate extended user interest tags by EUIT

Input:
uid_list(list):[uid], uid: the user id of tager users.
text(dictonary):{wid:[word]}, microblog texts after split in training set.
tfidf(dictonary):{word:tf-idf weight}.
win: the size of windows for TextRank.

Output:
tags(dictonary):{tag:weight} extended user interest tags and their weights.
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

#Compute keywords' weight by TextRank with TF-IDF
def textRank():
    d = 0.85  #damping factor
    iterator = 100  
    weight = init_weight()
    out = init_out(weight)
    value = {}
    #initial value
    for item in tfidf.keys():
        value[item] = (1-d) * tfidf[item]
    for i in range(0,iterator):
        for item in weight.keys():
            sum = 0 
            for word in weight[item]:
                sum += (weight[item][word] * value[word])/out[word]
            value[item] = (1-d)  + d * sum * (tfidf[item] + 1 )
    return value

def createC1(dataSet):
    C1 = set()
    for transaction in dataSet:
        for item in transaction:
            C1.add(item)
    C1 = list(C1)
    C1.sort()
    return map(lambda x:frozenset([x]), C1)

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for can in Ck:
        for tid in D:
            if can.issubset(tid):
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    retList = [] # Lk
    supportData = {} 
    for key in ssCnt:
        support = ssCnt[key]
        if support >= minSupport:
            retList.append(key) 
        supportData[key] = support
    return retList, supportData

def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1 == L2: 
                retList.append(Lk[i] | Lk[j]) 
    return retList

def apriori(dataSet, minSupport=3):
    C1 = createC1(dataSet)
    D = dataSet
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while len(L[k-2])>0:
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport) 
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

def calcConf(freqSet, H, supportData, br1, minConf=0.7):
    prunedH = []
    for conseq in H:
        if  len(freqSet - conseq) >1:
            continue
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            br1.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):
    m = len(H[0])
    if len(freqSet) > m+1:
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
        if len(Hmp1)>1:
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)

def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if i>1:
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

#Extend keywords based on Apriori
def keyword_extend():
    user_tag = sorted(value.items(),key=lambda x:x[1],reverse=True)
    key = []
    word_fre = {} 
    corr = {} 
    extend = {} 
    for i in range(0,20):
        key.append(user_tag[i][0])
        extend[user_tag[i][0]] = set()
        extend[user_tag[i][0]].add(user_tag[i][0])
   
    data = []
    for w in text.keys():
        num = len(text[w])
        tmp = set()
        for i in range(0,num):
            if text[w][i] in key:
                tmp.add(text[w][i])
        if len(tmp) < 2:
            continue
        data.append(tmp)
    
    ##aprioir
    L,supportData = apriori(data,2) ##L：the frequent set
    rule = generateRules(L, supportData, minConf=0.7) ##association rules
    
    #extend tags by rule. tag:word1,word2,...
    for item in rule:
        w1 = list(item[0])[0]
        w2 = list(item[1])
        for w in w2:
            extend[w1].add(w)
    result = {}
    for w1 in key:
        if len(extend[w1]) == 1: 
            result[w1] = value[w1]
            continue
        s = sorted(extend[w1])  
        st=''
        for w2 in s:
            st += w2 + ','
        st = st[0:-1]
        if st not in result:
            result[st] = value[w1]
        else:
            result[st] += value[w1]
    return result


if __name__ == '__main__':
    #load uid_list
    for uid in uid_list:
        #load text,tfidf
        tti = textRank() ##generate keywords and their weights by TextRank with TF-IDF
        tags = keyword_extend() ##extend keywords by Apriori to generate extended user interest tags