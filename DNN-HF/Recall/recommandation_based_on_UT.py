"""
Reommendation based on user interest topics UT

Input:
uid_list(list):[uid], uid: the user id of tager users.
uid_wid(dictonary):{uid:[wid]}, wid：the microblogs' id of user uid.
original(dictonary):{wid:wid_o}, wid_o is the original microblog id of wid.
topic_list(list):[topic], the topics in microblogs.
w_topic(dictonary):{wid:[topic]}, the topics in microblog wid.
test(list):[wid], the id of microblogs in test set.
num: the number of microblogs to be recommended.

Ouput:
result(set):(wid), the candidate recommended microblog set B.
"""
import math
import numpy as np 

def compute_tf_idf():
    tf = {}
    idf = {}
    for item in topic_list:
        tf[item] = 0
        idf[item] = 0
    ##compute tf:
    num = 0
    for w in uid_wid[uid]:
        t = set(w_topic[w])
        tmp = topic_list & t 
        for item in tmp:
            tf[item] += 1
            num += 1
    for item in tf.keys():
        tf[item] /= num
    
    ##compute idf:
    n = len(uid_wid)
    for item in topic_list:
        if tf[item] == 0:
            continue
        count = 0
        for u in uid_wid:
            flag = 0
            for wid in uid_wid[u]:
                if item in w_topic[wid]:
                    flag = 1
                    break
            if flag == 1:
                count += 1
        idf[item] = math.log(n/(count+1))+1
    tfidf = {}
    for item in tf.keys():
        tfidf[item] = tf[item] * idf[item]
    return tfidf   

def usertopic_recall():
    #compute TopicScore
    score = {}
    for i in test:
        score[i] = 0
        t = set(w_topic[i])
        tmp = topic & t
        for item in tmp:
            score[i] += tfidf[item]
    sort_score = sorted(score.items(),key=lambda x:x[1],reverse=True)
    #recommend top-num microblogs
    result = set()
    n = len(score)
    for i in range(0,n):
        if sort_score[i][1] <= 0:
            break
        result.add(original[sort_score[i][0]])
        if len(result) >= num:
            break
    return result

if __name__ == '__main__':
    #load uid_list
    for uid in uid_list:
        #load uid_wid,original,topic_list,w_topic,test
        tfidf = compute_tf_idf() #compute topic weights by TF-IDF
        user_topic = sorted(tfidf.items(),key=lambda x:x[1],reverse=True)
        topic = set()
        topic_num = 10
        for i in range(0,topic_num):
            topic.add(user_topic[i][0])
        result = usertopic_recall()