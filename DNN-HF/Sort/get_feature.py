"""
Generate features for DNN model training

Input:
uid_list(list):[uid], uid: the user id of tager users.
sample(dictonary):{wid:label}, the microblogs that needs to generate feaures(label is null for test set).
text(dictonary):{wid:"microblog text content"}.
has_pic(dictonary):{wid:whether wid has pic(0/1)}.
has_video(dictonary):{wid:whether wid has video(0/1)}.
text_length(dictonary):{wid:the length of text}.
topic_num(dictonary):{wid:the number of topics}.
topic(dictonary):{uid:[topic]}.
huguan(list):[uid], the users that follow the target users.
tags(dictonary):{tag:weight}, the extended user interest tags and their weights.
usertopic(dictonary):{topic:weight}, the user interest topics and their weights.
sim(dictonary):{uid:similarity}, the interactive behaviour similarity between uid and target users.

Ouput:
samples.dat: eight features for each sample.
"""
#min-max normalization
def max_min(data):
    ma = 0
    mi = 1000000
    for item in data.keys():
        if data[item] > ma:
            ma = data[item]
        if data[item] < mi:
            mi = data[item]
    for item in data.keys():
        data[item] = (data[item] - mi) / (ma-mi)
    return data

#compute Tag_score
def get_tag_score():
    #load tags
    tags = max_min(tags)
    score = {}
    for i in text:
        score[i] = 0
        for tag in tags.keys():
            l = tag.split(',')
            flag = 0
            for tt in l:
                if tt not in text[i]:
                    flag = 1
                    break
            if flag == 0:
                score[i] += tags[tag]
    return score

#compute Topic_score
def get_topic_score():
    #load usertopic
    score = {}
    usertopic_set = set(usertopic)
    for i in text:
        score[i] = 0
        t = set(topic[i])
        tmp = usertopic_set & t
        for item in tmp:
            score[i] += usertopic[item]
    return score

#compute Social_score
def get_social_score():
    #load huguan
    social_score = {}
    for wid in wid_uid.keys():
        social_score[wid] = 0
        for u in wid_uid[wid]:
            if u in huguan:
                social_score[wid] += 1
        social_score[wid] /= len(wid_uid[wid])
    return social_score

#compute Interactive_score
def get_interactive_score():
    #load sim
    score ={}
    for wid in wid_uid.keys():
        score[wid] = 0
        if len(wid_uid[wid]) == 1 and wid_uid[wid][0] == uid:
            score[wid] = 1
            continue
        count = 0
        for u in wid_uid[wid]:
            if u == uid:
                continue
            count += 1
            score[wid] += sim[u]
        if count != 0:
            score[wid] /= count 
    return score

def save_result(sample,tag_score,topic_score,interactive_score,social_score,text_length,topic_num,has_pic,has_video):
    filename = './samples.dat'
    with open(filename,'a',encoding='utf-8') as f:
        for wid in sample.keys():
            f.write(wid+'\t'+str(tag_score[wid])+'\t'+str(topic_score[wid])+'\t'+str(interactive_score[wid])+'\t'+str(has_pic[wid])+'\t'+str(has_video[wid])+'\t'+str(social_score[wid])+'\t'+str(text_length[wid])+'\t'+str(topic_num[wid])+'\t'+str(sample[wid])+'\n')
        f.close()
        
if __name__ == '__main__':
    #load uid_list
    for uid in uid_list:
        #load sample,wid_uid,text,topic,has_pic,has_video,text_length,topic_num
        tag_score = get_tag_score() 
        topic_score = get_topic_score()
        interactive_score = get_interactive_score() 
        social_score = get_social_score()
    save_result(sample,tag_score,topic_score,interactive_score,social_score,text_length,topic_num,has_pic,has_video) 