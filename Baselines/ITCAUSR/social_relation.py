"""
social relation

Input:
uid_list(list):[uid], uid: the user id of tager users.
tag(dictonary):{uid:{word:weight}}.
follow(dictonary):[uid:[uid_f]], uid follows uid_f.
user_list(list)[user_i], follow users for each target user.
user_dict(dictonary)[user_i:index],assign unique index for each user. 

Output:

Matrix M_sr(numpy arary)
"""

import numpy as np 


def get_follower():
    follower = {}
    for uid in user_list:
        follower[uid] = []
    for uid in follow.keys():
        for uid2 in follow[uid]:
            if uid2 in follower:
                follower[uid2].append(uid)
    return follower


def get_sim():
    n = len(user_list)
    sim1 = np.zeros((n,n))
    sim2 = np.zeros((n,n))
    #compute sim(Fg(ui),Fg(uj))
    for i in range(0,n):
        if user_list[i] not in follow:
            continue
        for j in range(i+1,n):
            if user_list[j] not in follow:
                continue
            con = set(follow[user_list[i]]) & set(follow[user_list[j]])
            n1 = len(follow[user_list[i]])
            n2 = len(follow[user_list[j]])
            if n1*n2==0:
                sim1[i][j]=0
            else:
                sim1[i][j] = len(con)/(n1*n2)
                sim1[j][i] = sim1[i][j]
    #compute sim(Fr(ui),Fr(uj))            
    for i in range(0,n):
        if user_list[i] not in follower:
            continue
        for j in range(i+1,n):
            if user_list[j] not in follower:
                continue
            con = set(follower[user_list[i]]) & set(follower[user_list[j]])
            n1 = len(follower[user_list[i]])
            n2 = len(follower[user_list[j]])
            if n1*n2==0:
                sim2[i][j] = 0
            else:
                sim2[i][j] = len(con)/(n1*n2)
                sim2[j][i] = sim2[i][j]     
                
    #compute sim(SR(ui),SR(uj))                            
    sim = sim1 + sim2   
    #Normalization N-sim(SR(ui),SR(uj)) 
    ma = np.max(sim)
    mi = np.min(sim)
    for i in range(0,n):
        for j in range(i,n):
            if i == j:
                sim[i][j] = 1
            else:
                sim[i][j] = (sim[i][j]-mi)/(ma-mi)
                sim[j][i] = sim[i][j]
    return sim  


if __name__ == '__main__':
    #load uid
    for uid in uid_list:
        #load tag, follow, user_list, user_dict
        users = list(tag.keys())
        follower = get_follower()
        M_sr = get_sim()