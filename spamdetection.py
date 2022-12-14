# -*- coding: utf-8 -*-
"""spamdetection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SJKMJQ5gRPtU1Tq4EF3OQI8NfS4N3eRN
"""

import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.linear_model import Perceptron

data=pd.read_excel("/content/drive/MyDrive/spambase excel.xlsx")

data

data.info()

data.head()

data.tail()

data.shape

data.describe()

print(data.isnull().sum())

data.rename(columns={'Column58':"Spam"},inplace=True)

data

import seaborn as sns
sns.countplot(x ='Spam', data = data)

x=Perceptron()

y = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

X=data.drop(labels="Spam",axis=1)
Y=data['Spam']

score = cross_val_score(x, X, Y, scoring='accuracy', cv=y, n_jobs=-1)

from numpy import mean
from numpy import std
print('Mean Accuracy: %.3f (%.3f)' % (mean(score), std(score)))

from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.20,random_state=101)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

x.fit(X_train,Y_train)
xpred=x.predict(X_test)

from sklearn.metrics import accuracy_score

print("Accuracy:",accuracy_score(Y_test,xpred))

#HYPER PARAMETER TUNING

from sklearn.model_selection import GridSearchCV

grid = dict()
grid['eta0'] = [0.0002, 0.002, 0.02, 0.2,2.0]
grid['max_iter'] = [1, 10, 100, 1000]

s = GridSearchCV(x, grid, scoring='accuracy', cv=y, n_jobs=-1)

results = s.fit(X_train, Y_train)

print("Accuracy:",accuracy_score(Y_test,xpred))
print('Config: %s' % results.best_params_)

# summarize all
means = results.cv_results_['mean_test_score']
params = results.cv_results_['params']
for mean, param in zip(means, params):
    print(">%.3f with: %r" % (mean, param))

#model after hyperparameter tuning
model = Perceptron(eta0=0.002,max_iter=10)
perceptron=model.fit(X_test, Y_test)
pred=perceptron.predict(X_test)

accuracy=accuracy_score(pred,Y_test)
print("accuracy score:",accuracy)

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
cf_matrix = confusion_matrix(Y_test, pred)
sns.heatmap(cf_matrix,cmap='PuBuGn',annot=True)

print(classification_report(Y_test,pred))

