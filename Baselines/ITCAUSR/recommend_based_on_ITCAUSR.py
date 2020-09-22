"""
Recommendation based on ITCAUSR

Input:
uid_list(list):[uid], uid: the user id of tager users.
uid_wid(dictonary):{uid:[wid]}, wid：the microblogs' id of user uid.
user_dict(dictonary)[user_i:index],assign unique index for each user.
original(dictonary):{wid:wid_o}, wid_o is the original microblog id of wid.
text(dictonary):{wid:"microblog text content"}. 
test(list):[wid], the id of microblogs in test set.
tag_list(list)[tag_i] tags for each target user.
num: the number of microblogs to be recommended.
Matrix M_x(numpy arary)

Ouput:
result(set):(wid), the recommended microblog set.
"""
import numpy as np 
np.set_printoptions(threshold=np.inf)


def get_usertag():
    u = M_x[user_dict[uid]]
    user_tag = {}
    tag_size = 10
    for i in range(0,len(tag_list)):
        user_tag[tag_list[i]] = u[i]
    user_tag = sorted(user_tag.items(),key=lambda x:x[1],reverse=True)[0:tag_size]
    d = {}
    for item in user_tag:
        d[item[0]]=item[1]
    user_tag=d
    return user_tag


def recall():
    #compute user-microblog similarity score
    score = {}
    for i in test:
        score[i] = 0
        for tag in user_tag.keys():
            if tag in text[i]:
                score[i] += user_tag[tag]
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
        #load uid_wid,original,text,test,user_dict,tag_list,M_x
        user_tag = get_usertag() #obtain user tags
        result = recall()  #recommend micrcoblogs