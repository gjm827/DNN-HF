"""
Recommendation based on user interest tags by TTI

Input:
uid_list(list):[uid], uid: the user id of tager users.
original(dictonary):{wid:wid_o}, wid_o is the original microblog id of wid.
text(dictonary):{wid:"microblog text content"}. 
test(list):[wid], the id of microblogs in test set.
tags(dictonary):{tag:weight}, the user interest tags and their weights.
num: the number of microblogs to be recommended.

Ouput:
result(set):(wid), the recommended microblog set.
"""
import math
import numpy as np

##min-max normalization
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


#Recommendation based on TTI
def TTI_recall():
    #load tags
    tags = max_min(tags)
    score = {}
    for i in test:
        score[i] = 0
        for tag in tags.keys():
            if tag in text[i]:
                score[i] += tags[tag]
    score = sorted(score.items(),key=lambda x:x[1],reverse=True)
    #recommend top-num microblogs
    result = set()
    n = len(score)
    for i in range(0,n):
        if score[i][1] <= 0:
            break
        result.add(original[score[i][0]])  
        if len(result) >= num:
            break
    return result

if __name__ == '__main__':
    #load uid_list
    for uid in uid_list:
        #load original,text,test
        result = TTI_recall() #recommendation based on TTI    