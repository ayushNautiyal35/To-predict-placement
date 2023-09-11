# -*- coding: utf-8 -*-
"""predict_placement.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eR96lTC8d1IM3Scbi8k69c1D90_W7PI8

#**Import train data**
"""

from pathlib import Path
import pandas as pd
import urllib.request

def import_data():
  url="https://raw.githubusercontent.com/ayushNautiyal35/To-predict-placement/main/Predict_placement/01%20Train%20Data.xlsx"
  return pd.read_excel(url)

data=import_data()
data

data.info()

"""#**Clean the data**"""

data.dropna(subset=("Placement Status"),inplace=True)
data

data=data.drop_duplicates(subset="Email ID")

data=data.drop("Price Tier",axis=1)

data=data.drop("Group",axis=1)

data["Attendee #"]=data["Attendee #"].fillna(data["Attendee #"].median())

data["Currency"]=data["Currency"].fillna("USD")

data["Fees Paid"]=data["Fees Paid"].fillna(0)

data['College Name']=data['College Name'].fillna("Other")

data=data.drop("Year of Graduation",axis=1)

data['How did you come to know about this event?']=data['How did you come to know about this event?'].replace("Others","college")

data=data.drop('Specify in "Others" (how did you come to know about this event)',axis=1)

data.info()

"""##Deal with object data"""

data["Placement Status"].value_counts()

data["Placement Status"]=data["Placement Status"].replace("Placed",1)
data["Placement Status"]=data["Placement Status"].replace("Not placed",0)

data["Placement Status"]

c=0
for i in data["Placement Status"]:
  if(i==1):
    c=c+1;
print(c)

"""#split in Train and Test"""

data=data.drop("Email ID",axis=1)

data=data.drop("First Name",axis=1)

from sklearn.model_selection import train_test_split
train,test=train_test_split(data,test_size=0.2,random_state=42)

train.size

test.size

data=train.drop("Placement Status",axis=1)

target=train["Placement Status"].copy()

data.head()

target.tail()

"""##Make pipeline"""

from sklearn.pipeline import make_pipeline

from sklearn.impute import SimpleImputer
import numpy as np
from sklearn.preprocessing import StandardScaler
data_num=data.select_dtypes(include=[np.number])
num_pipeline=make_pipeline(SimpleImputer(strategy="median"),StandardScaler())
data_num_prepared=num_pipeline.fit_transform(data_num)

from sklearn.preprocessing import OneHotEncoder

cat_attribute=make_pipeline(SimpleImputer(strategy="most_frequent"),OneHotEncoder(handle_unknown="ignore"))

from sklearn.compose import make_column_transformer,make_column_selector

preprocessing=make_column_transformer((num_pipeline,make_column_selector(dtype_include=np.number)),(cat_attribute,make_column_selector(dtype_include=object)))

preprocessing

data_prepared=preprocessing.fit_transform(data)

"""**Select and train model**"""

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
# Binary Classification Example
classifiers_binary = {
    "Logistic Regression": make_pipeline(preprocessing,LogisticRegression()),
    "Decision Tree": make_pipeline(preprocessing,DecisionTreeClassifier()),
    "Random Forest": make_pipeline(preprocessing,RandomForestClassifier()),
    "Support Vector Machine": make_pipeline(preprocessing,SVC()),
    "k-Nearest Neighbors": make_pipeline(preprocessing,KNeighborsClassifier())
}

print("Binary Classification Results:")
for name, clf in classifiers_binary.items():
    clf.fit(data, target)
    y_pred = clf.predict(data)
    accuracy = accuracy_score(target, y_pred)
    print(f"{name}: Accuracy = {accuracy:.2f}")
    print(classification_report(target, y_pred))

"""**Evaluate model on test**"""

x_test=test.drop("Placement Status",axis=1)
y_test=test["Placement Status"].copy()

clas=make_pipeline(preprocessing, RandomForestClassifier(random_state=42))
clas.fit(data,target)
final_predictions=clas.predict(x_test)

j=0
for i in final_predictions:
  if(i==1):
    j=j+1
print(j)

from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, final_predictions)
accuracy

"""##Now fitting for the test data set"""

def import_data():
  url="https://raw.githubusercontent.com/ayushNautiyal35/To-predict-placement/main/Predict_placement/02%20Test%20Data.xlsx"
  return pd.read_excel(url)

test_data=import_data()
dt=test_data

dt=dt.drop("Price Tier",axis=1)
dt=dt.drop("Group",axis=1)
dt=dt.drop("Year of Graduation",axis=1)
dt=dt.drop('Specify in "Others" (how did you come to know about this event)',axis=1)
dt=dt.drop("Email ID",axis=1)
dt=dt.drop("First Name",axis=1)

x=dt.drop("Placement Status",axis=1)

final_predict=clas.predict(x)
final_predict

test_data["Placement Status"]=final_predict

for i in test_data["Placement Status"]:
  if (i==0):
    test_data["Placement Status"]=test_data["Placement Status"].replace(0,"Not placed")
  else:
    test_data["Placement Status"]=test_data["Placement Status"].replace(1,"Placed")

test_data.to_excel('output_file.xlsx', index=False)