"""
Recommendation based on user-based Collaborative Filtering CF

Input:
uid_list(list):[uid], uid: the user id of tager users.
uid_wid(dictonary):{uid:[wid]}, wid：the microblogs' id of user uid.
author(dictonary):{wid:uid}, uid is the author of microblog wid.
original(dictonary):{wid:wid_o}, wid_o is the original microblog id of wid.
text(dictonary):{wid:"microblog text content"}. 
huguan(list):[uid], the users that follow the target users.
follow(list):[uid], the users that the target users follow.
social(dictonary):{uid:[uid_f]} uid_f are the users that uid follows.
test(list):[wid], the id of microblogs in test set.
tags(dictonary):{tag:weight}, the extended user interest tags and their weights.
num: the number of microblogs to be recommended.

Ouput:
uc_sim: the user similarity calculated by user content.
ib_sim: the user similarity calculated by interactive behaviours.
sr_sim: the user similarity calculated by the first soical relationship.
sr2_sim: the user similarity calculated by the second soical relationship.
result(set):(wid1,wid2,...), the candidate recommended microblog set C.
"""
import math
import numpy as np 

#min-max normalization
def max_min(data):
    ma = 0
    mi = 100
    for item in data.keys():
        if data[item] > ma:
            ma = data[item]
        if data[item] < mi:
            mi = data[item]
    for item in data.keys():
        data[item] = (data[item] - mi) / (ma-mi)
    return data

def get_wid_uid():
    wid_uid = {}
    for u in uid_wid.keys():
        for w in uid_wid[u]:
            if w not in wid_uid:
                wid_uid[w] = []
            wid_uid[w].append(u)
    return wid_uid

#compute user content similarity
def get_uc_sim():
    content = {}
    for u in follow:
        u = int(u)
        content[u] = 0
        if u not in uid_wid:
            continue
        for w in uid_wid[u]:
            score = 0
            for t in tags.keys():
                l = t.split(',')
                flag = 0
                for tt in l:
                    if tt not in text[w]:
                        flag = 1
                        break
                if flag == 0:
                    score += tags[t]
            content[u] += score
        content[u] /= len(uid_wid[u])
    return content

#compute social relationship similarity
def get_sr_sim():
    fam = {}
    for u in follow:
        fam[int(u)] = 0
    for u in huguan:
        fam[int(u)] = 1
    return fam

#compute social relationship-2 similarity
def get_sr2_sim():
    user_list = list(social.keys())
    n = len(user_list)
    sim = {}
    for i in range(0,n):
        if user_list[i] == uid:
            continue
        con = set(social[uid]) & set(social[user_list[i]])
        whole = set(social[uid]) | set(social[user_list[i]])
        if whole == 0:
            sim[user_list[i]]=0
        else:
            sim[user_list[i]] = len(con)/(len(whole))
    return sim  

#compute interactive behavior similarity
def get_ib_sim():
    sim = {}
    for u in follow:
        sim[int(u)] = 0
    for w in uid_wid[uid]:
        for u in wid_uid[w]: 
            if u == uid:
                continue
            sim[u] += 1
        if w in author and author[w] != uid:
            sim[author[w]] += 1
    for u in sim:
        if u not in uid_wid:
            continue
        sim[u] /= math.sqrt(len(uid_wid[u]))
    return sim


def get_result(sim):
    #compute CFScore based on interactive behavior similarity
    score = {}
    for wid in test:
        score[wid] = 0
        for u in wid_uid[wid]:
            if u == uid:
                continue         
            score[wid] += sim[u]
    score = sorted(score.items(),key=lambda x:x[1],reverse=True)
    #recommend top-num microblos.
    result = set()
    weibo = []
    for i in range(0,num):
        if score[i][1] <= 0:
            break
        result.add(score[i][0])
    return result

if __name__ == '__main__':
    #load uid_list
    for uid in uid_list:
        #load uid_wid,original,author,text,huguan,follow,soical,tags,test.
        wid_uid = get_wid_uid()
        tags = max_min(tags)
        uc_sim = get_uc_sim() #compute user content similarity
        sr_sim = get_sr_sim() #compute social relationship similarity
        sr2_sim = get_sr2_sim() #compute social relationship-2 similarity
        ib_sim = get_ib_sim() #compute interactive behavior similarity
        result = get_result(ib_sim) #recommend microblogs