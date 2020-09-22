"""
Multi-tags correlation

Input:
uid_list(list):[uid], uid: the user id of tager users.
tag(dictonary):{uid:{word:weight}.

Output:
tag_list(list)[tag_i] tags for each target user.
tag_dict(dictonary)[tag_i:index] assign unique index for each tag. 
inner(dictonary){tag_j:{tag_k:N-LIR(tag_j,tag_k)},inner correlation between tags.
outer(dictonary){tag_j:{tag_k:N-LOR(tag_j,tag_k)},outer correlation between tags.
"""
import numpy as np 

def get_tag_list():
    tag_list = set()
    for u in tag.keys():
        for i in tag[u].keys():
            tag_list.add(i)
    tag_list = list(tag_list)
    n = len(tag_list)
    tag_dict = {}
    for i in range(0,n): 
        tag_dict[tag_list[i]] = i
    return tag_list,tag_dict

#compute inner correlation
def get_inner():
    n = len(tag_list)
    inner = {} 
    count = {}
    for i in range(0,n):
        inner[i] = {}
        inner[i][i] = 0
        count[i] = {}
        count[i][i] = 1
    ##compute LIR(innter)
    for i in tag.keys():
        for item1 in tag[i].keys():
            for item2 in tag[i].keys():
                if item1==item2:
                    continue
                j = tag_dict[item1]
                k = tag_dict[item2]
                if k not in inner[j]:
                    inner[j][k] = 0
                    count[j][k] = 0
                inner[j][k] += (tag[i][item1] * tag[i][item2]) /(tag[i][item1] + tag[i][item2]-tag[i][item1] * tag[i][item2])
                count[j][k] += 1          
    s = {}
    for i in range(0,n):
        s[i] = 0
        for j in inner[i].keys():
            if count[i][j]!=0:
                inner[i][j] /= count[i][j]
            s[i] += inner[i][j]       
    ##normalization N-LIR(inner)
    for i in range(0,n):
        for j in inner[i].keys():
            if i==j:
                inner[i][j] = 1
            else:
                inner[i][j] /= s[j]
    return inner

#compute outer correlation
def get_outer():
    outer = {}
    count = {}
    user_list = list(tag.keys())
    ##compute LOR
    for u1 in range(0,len(user_list)):
        for u2 in range(u1+1,len(user_list)):
            s1 = set(tag[user_list[u1]].keys())
            s2 = set(tag[user_list[u2]].keys())
            con =s1 & s2  
            if len(con) < 1:
                continue
            for item1 in s1-con:
                j = tag_dict[item1]
                if j not in outer:
                    outer[j] = {}
                    count[j] = {}
                for item2 in s2-con:
                    k = tag_dict[item2]
                    if k not in outer:
                        outer[k] = {}
                        count[k] = {}
                    if j not in outer[k]:
                        outer[k][j] = 0
                        count[k][j] = 0
                    if k not in outer[j]:
                        outer[j][k] = 0
                        count[j][k] = 0
                    for item3 in con:
                        q = tag_dict[item3]
                        outer[j][k] += min(inner[j][q],inner[k][q])
                        outer[k][j] = outer[j][k]
                        count[j][k] += 1
                        count[k][j] = count[j][k]
        ##normalization LOR                
        for i in outer.keys():
            for j in outer[i].keys():
                outer[i][j] /= count[i][j]
        return outer


if __name__ == '__main__':
    #load uid_list
    for uid in uid_list:
        #load tag
        tag_list,tag_dict = get_tag_list()
        innter = get_inner()
        outer = get_outer()