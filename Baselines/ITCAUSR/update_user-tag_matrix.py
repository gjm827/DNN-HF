"""
update_user-tag_matrix

Input:
uid_list(list):[uid], uid: the user id of tager users.
tag(dictonary):{uid:{word:weight}}.
tag_list(list)[tag_i] tags for each target user.
tag_dict(dictonary)[tag_i:index] assign unique index for each tag. 
inner(dictonary){tag_j:{tag_k:N-LIR(tag_j,tag_k)},inner correlation between tags.
outer(dictonary){tag_j:{tag_k:N-LOR(tag_j,tag_k)},outer correlation between tags.

Output:
user_list(list)[user_i], follow users for each target user.
user_dict(dictonary)[user_i:index],assign unique index for each user. 
Matrix M_re(numpy array)
"""
import numpy as np 
np.set_printoptions(threshold=np.inf)

def get_user_list():
    user_list = list(tag.keys())
    user_dict = {}
    for i in range(len(user_list)):
        user_dict[user_list[i]] = i
    return user_list,user_dict

def get_array():
    inn = np.zeros((n,n))
    out = np.zeros((n,n))
    for i in inner.keys():
        for j in inner[i].keys():
            inn[i][j] = inner[i][j]
    for i in outer.keys():
        for j in outer[i].keys():
            out[i][j] = outer[i][j]
    return inn,out

#compute M_ul
def get_Mul():
    ul = np.zeros((m,n))
    for u in tag.keys():
        for t in tag[u].keys():
            if u in user_dict:
                ul[user_dict[u]][tag_dict[t]] = tag[u][t]
    return ul

def get_Mre():
    inn,out = get_array()
    ul = get_Mul()
    ##compute M_lr
    lr = 0.5*inn + 0.5*out
    ##compute M_re
    re = np.dot(ul,lr)
    return re


if __name__ == '__main__':
    #load uid_list
    for uid in uid_list:
        #load tag,tag_list,tag_dict,innter,outer
        user_list,user_dict = get_user_list()
        n = len(tag_list)
        m = len(user_list)
        M_re = get_Mre()