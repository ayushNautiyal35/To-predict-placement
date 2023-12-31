# -*- coding: utf-8 -*-
"""To_calculate_passing_year.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ehLwlRydVsZX67pBxXQkVw4rMOBu3toV
"""

from pathlib import Path
import pandas as pd
import urllib.request

def import_data():
  url="https://raw.githubusercontent.com/ayushNautiyal35/To-predict-placement/main/calculate_year_dataset/Final%20Lead%20Data.xlsx"
  return pd.read_excel(url)

data=import_data()

data

data.info()

data['What is your current academic year?'].value_counts()

data['Academic Year'].value_counts()

data=data.drop_duplicates(subset='ID')
data.info()

data['What is your current academic year?']=data['What is your current academic year?'].replace('1st Year',1.0)

data['What is your current academic year?']=data['What is your current academic year?'].replace('2nd Year',2.0)

data['What is your current academic year?']=data['What is your current academic year?'].replace('3rd Year',3.0)

data['What is your current academic year?']=data['What is your current academic year?'].replace('Final Year',4.0)

data['What is your current academic year?'].value_counts()

data['Academic Year']=data['Academic Year'].fillna(0)
data['What is your current academic year?']=data['What is your current academic year?'].fillna(0)

import numpy as np
data["Passing Year"]=np.nan
data["Passing Year"].size

for  i in range(0,data["Passing Year"].size-1):
  if(not(data.loc[i,'Academic Year']==0.0)):
    data.at[i,'Passing Year']=2023+(4-data.loc[i,'Academic Year'])
  elif(not(data.loc[i,'What is your current academic year?']==0.0)):
    data.at[i,'Passing Year']=2023+(4-data.loc[i,'What is your current academic year?'])

data["Passing Year"].value_counts()

data.info()



data

data.info()

data.to_excel('output_file_calculate_passing_year.xlsx', index=False)
