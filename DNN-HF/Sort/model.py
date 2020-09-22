"""
DNN model trianing and generate recommended microblogs.

Input:
samples.dat: eight features for each sample in trainning set .
uid_list(list):[uid], uid: the user id of tager users.
test(dictonary):{wid:[feature]} eight features for each candidate recommended microblog.
num: the number of microblogs to be recommended.

Output:
result_list(list):[wid], the microblogs to be recommended.
"""

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,f1_score
from sklearn.externals import joblib
from sklearn import preprocessing

sample = np.loadtxt('samples.dat')
x = sample[:,1:-1]
scaler=preprocessing.StandardScaler().fit(x)
x=scaler.transform(x)
y = sample[:,-1]
x_train,x_val,y_train,y_val = model_selection.train_test_split(x,y,test_size = 0.2)

#DNN model
model = MLPClassifier(activation='relu',solver='adam',max_iter=200,learning_rate_init=0.0005,hidden_layer_sizes=(64,32,16))
model.fit(x_train,y_train)
y_pred = model.predict(x_train)
print(classification_report(y_train,y_pred))

y_pred = model.predict(x_val)
print(classification_report(y_val,y_pred))

#save model
#joblib.dump(model,'model.pkl')

#load model
#model = joblib.load('model.pkl')

#load uid_list
for uid in uid_list:
    #load test
    wid = test[:,0]
    x = test[:,1:]
    x = scaler.transform(x)
    pre = model.predict_proba(x)
    #recommend microblogs
    result = {}
    for i in range(0,len(wid)):
        result[str(wid[i])] = pre[i][1]
    result = sorted(result.items(),key=lambda x:x[1],reverse=True)
    result_list = []
    for item in result:
        result_list.append(item[0])
        if len(result_list) >= num:
            break