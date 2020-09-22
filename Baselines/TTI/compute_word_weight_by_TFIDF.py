"""
Compute word's weight by TF-IDF
Input:
uid_list(list):[uid], uid: the user id of tager users.
uid_wid(dictonary):{uid:[wid]}, wid：the microblogs' id of user uid.
text(dictonary):{wid:[word]}, microblog texts after split in training set.

Output:
tfidf(dictonary):{word:tf-idf weight}
""""
import math
import numpy as np 

def get_word_list():
    word_list = []
    word_dict = {}
    num = 0
    for w in uid_wid[uid]:
        for item in text[w]:
            if item not in word_dict:
                word_dict[item] = num
                num += 1
            word_list.append(item)
    return word_list,word_dict       

def compute_tf_idf():
    ##compute tf:
    tf = {}
    num = len(word_list)
    for item in word_dict:
        tf[item] = word_list.count(item)
        tf[item] /= num
    
    ##compute idf:
    idf = {}
    n = len(uid_wid)
    for item in word_dict:
        count = 0
        for u in uid_wid:
            flag = 0
            for wid in uid_wid[u]:
                if item in text[wid]:
                    flag = 1
                    break
            if flag == 1:
                count += 1
        idf[item] = math.log(n/count)
    #compute tf-idf
    tfidf = {}
    for item in tf.keys():
        tfidf[item] = tf[item] * idf[item]
    return tfidf   

if __name__ == '__main__':
    #load uid_list
    for uid in uid_list:
        #load uid_wid,text
        word_list,word_dict = get_word_list() 
        tfidf = compute_tf_idf() 