# -*- coding: utf-8 -*-
"""Twitter data_svm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1o4OH585y0VmDRvJuvdg2kp6Z0b9c_5Xd
"""

import pandas as pd

df=pd.read_csv(r"/content/drive/MyDrive/COVIDSenti-A.csv")

df

df.head(10)

df.shape

df.info()

df.describe()

df.columns

df.label.value_counts()

df[df['label']=='neg']

df[df['label']=='pos']

df[df['label']=='neu']

df[df['label']=='neu'].loc[17,'tweet']

df[df['label']=='neg'].loc[16,'tweet']

df[df['label']=='pos'].loc[70,'tweet']

df.isnull().sum()

import re 
import numpy as np

# write function for removing @user
def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i,'',input_txt)
    return input_txt

# create new column with removed @user
df['tweet'] = np.vectorize(remove_pattern)(df['tweet'], '@[\w]*')

# to remove HTTP and urls from tweets
df['tweet'] = df['tweet'].apply(lambda x: re.split('https:\/\/.*', str(x))[0])

# remove special characters, numbers, punctuations
df['tweet'] = df['tweet'].str.replace('[^a-zA-Z#]+',' ')

df['tweet'] = df['tweet'].str.replace('#',' ')

# Making all the words in lower case
df['tweet']=df['tweet'].str.lower()

df.head()

# remove short words
df['tweet'] = df['tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w) > 2]))

df.head()

df[df['label']=='neu'].loc[17,'tweet']

# create new variable tokenized tweet 
tokenized_tweet = df['tweet'].apply(lambda x: x.split())

#Importing required resources
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

# import these modules
from nltk.stem import WordNetLemmatizer
  
lemmatizer = WordNetLemmatizer()
  
# apply lemmatizer for tokenized_tweet
tokenized_tweet = tokenized_tweet.apply(lambda x: [lemmatizer.lemmatize(i) for i in x])

tokenized_tweet

# join tokens into one sentence
for i in range(len(tokenized_tweet)):
    tokenized_tweet[i] = ' '.join(tokenized_tweet[i])
# change df['Tweet'] to tokenized_tweet

df['Tweet']  = tokenized_tweet

df.drop('tweet',axis=1,inplace=True)

df.head()

X = df['Tweet']
y = df['label']

# Splitting the dataset into training and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.3, random_state = 0)

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vect = TfidfVectorizer(max_features = 5000)
tfidf_vect.fit(df['Tweet'])
X_train_tfidf = tfidf_vect.transform(X_train)
X_test_tfidf = tfidf_vect.transform(X_test)

print(X_train_tfidf)

print(X_test_tfidf)

print(tfidf_vect.vocabulary_)

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import ConfusionMatrixDisplay,classification_report
from sklearn.preprocessing import LabelBinarizer

svm_model = SVC(probability = True, kernel = 'linear')
svm_model.fit(X_train_tfidf, y_train )

svm_predictions = svm_model.predict(X_test_tfidf)
Predicted_data = pd.DataFrame()
Predicted_data['Tweet'] = X_test
Predicted_data['Label'] = svm_predictions
Predicted_data

Predicted_data['Label'].value_counts()

ConfusionMatrixDisplay.from_predictions(y_test, svm_predictions)

svm_accuracy = accuracy_score(svm_predictions, y_test)*100
svm_accuracy

print("Classification Report:")
print(classification_report(y_test, svm_predictions))

