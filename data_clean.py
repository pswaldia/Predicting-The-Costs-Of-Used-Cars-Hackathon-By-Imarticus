import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
import warnings
warnings.filterwarnings('ignore')

train=pd.read_excel('Participants_Data_Used_Cars/Data_Train.xlsx')
test=pd.read_excel('Participants_Data_Used_Cars/Data_Test.xlsx')



train.drop(['New_Price'],inplace=True,axis=1)
test.drop(['New_Price'],inplace=True,axis=1)

#no. of rows for which seats has a null value in train
train[train['Seats'].isnull()].shape


train['Seats'].fillna(train['Seats'].mode()[0], inplace=True)
train['Engine'].fillna('0.0 CC',inplace=True)
train['Power'].replace({'null bhp':'0.0 bhp'},inplace=True)
train['Power'].fillna('0.0 bhp',inplace=True)
train['Mileage'].fillna('0.0 kmpl',inplace=True)
train['Engine']=train['Engine'].map(lambda x:float(x.split(' ')[0]))
train['Power']=train['Power'].map(lambda x:float(x.split(' ')[0]))
train['Power'].replace({0.0:train['Power'].mean()},inplace=True)
train['Engine'].replace({0.0:train['Engine'].mean()},inplace=True)
train['Mileage']=train['Mileage'].map(lambda x:float(x.split(' ')[0]))
train['Mileage'].replace({0.0:train['Mileage'].mean()},inplace=True)

test['Seats'].fillna(test['Seats'].mode()[0], inplace=True)
test['Engine'].fillna('0.0 CC',inplace=True)
test['Power'].replace({'null bhp':'0.0 bhp'},inplace=True)
test['Power'].fillna('0.0 bhp',inplace=True)
test['Mileage'].fillna('0.0 kmpl',inplace=True)
test['Engine']=test['Engine'].map(lambda x:float(x.split(' ')[0]))
test['Power']=test['Power'].map(lambda x:float(x.split(' ')[0]))
test['Power'].replace({0.0:test['Power'].mean()},inplace=True)
test['Engine'].replace({0.0:test['Engine'].mean()},inplace=True)
test['Mileage']=test['Mileage'].map(lambda x:float(x.split(' ')[0]))
test['Mileage'].replace({0.0:test['Mileage'].mean()},inplace=True)

test.to_csv('test.csv')
train.to_csv('train.csv')