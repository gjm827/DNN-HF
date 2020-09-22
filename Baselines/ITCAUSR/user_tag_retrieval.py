"""
user tag retrieval by TF-Clarity and TF-IDF
Input:
uid_list(list):[uid], uid: the user id of tager users.
uid_wid(dictonary):{uid:[wid]}, wid：the microblogs' id of user uid.
text(dictonary):{wid:[word]}, microblog texts after split in training set.
follow(list):[uid], the users that the target users follow.

Output:
tfidf(dictonary):{uid:{word:tf-idf weight}}
tfclarity(dictonary):{uid:{word:tf-clarity weight}
"""
import math
import numpy as np 

def get_word_list(u):
    word_list = []
    word_dict = {}
    word_fre = {}
    num = 0
    for w in uid_wid[u]:
        for item in text[w]:
            if item not in word_dict:
                word_dict[item] = num
                num += 1
            if item not in word_fre:
                word_fre[item] = {}
            if w not in word_fre[item]:
                word_fre[item][w] = 0
            word_fre[item][w] += 1
            word_list.append(item)
    return word_list,word_dict,word_fre        

def get_allw():
    allw = {}
    for u in uid_wid:
        for w in uid_wid[u]:
            for item in text[w]:
                if item not in allw:
                    allw[item] = set()
                allw[item].add(u)
    return allw


#Compute word's weight by tf-idf
def compute_tf_idf():
    #compute tf:
    result = {}
    count = 0
    for u in follow:
        if u not in uid_wid:
            continue
        word_list,word_dict,word_fre = get_word_list(u)
        tf = {}
        num = len(word_list)
        for item in word_dict:
            tf[item] = word_list.count(item)
            tf[item] /= num
        #compute idf:
        idf = {}
        n = len(uid_wid)
        for item in word_dict:
            idf[item] = math.log(n/(len(allw[item])+1))+1
        #compute tf-idf
        tfidf = {}
        for item in tf.keys():
            tfidf[item] = tf[item] * idf[item]
        user_tag = sorted(tfidf.items(),key=lambda x:x[1],reverse=True)
        result[u] = user_tag[0:20]
    return result   

#compute word's weight by tf-clarity
def compute_tf_clarity():
    ##compute tf:
    result = {}
    count = 0
    for u in follow:
        if u not in uid_wid:
            continue
        word_list,word_dict,word_fre = get_word_list(u)
        tf = {}
        num = len(word_list)
        for item in word_dict:
            tf[item] = word_list.count(item)
            tf[item] /= num
        #compute clarity
        clarity = {}
        for word in tf.keys():
            #query 20 most relavent document
            document = sorted(word_fre[word].items(),key=lambda x:x[1],reverse=True)
            if len(document) < 20:
                clarity[word] = 1
                continue
            vocabulary = set()
            fre = {}
            for d in document[0:20]:
                words = set(text[d[0]])
                for item in words:
                    vocabulary.add(item)
                    if item not in fre:
                        fre[item] = 0
                    fre[item] += 1
                    
            clarity[word] = 0
            for item in vocabulary:
                clarity[word] += (fre[item]/20) * math.log((fre[item]/20)/(len(word_fre[item])/len(uid_wid[u])))
        #compute tf-clarity                                              
        s = {}
        for item in tf.keys():
            s[item] = tf[item] * clarity[item]
        user_tag = sorted(s.items(),key=lambda x:x[1],reverse=True)
        result[u] = user_tag[0:10]
    return result   

def norm():
    for u in result.keys():
        s = 0
        for item in result[u]:
            s += item[1]
        tag = {}
        for item in result[u]:
            tag[item[0]] = item[1]/s
        result[u] = tag
    return result


if __name__ == '__main__':
    #load uid_list
    for uid in uid_list:
        #load follow,uid_wid,text
        allw = get_allw()
        tfidf = compute_tf_idf()
        tfidf = norm()
        tfclarity = compute_tf_clarity()
        tfclarity = norm()