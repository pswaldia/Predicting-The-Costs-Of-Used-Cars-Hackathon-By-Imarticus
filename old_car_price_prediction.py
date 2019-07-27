# -*- coding: utf-8 -*-
"""old_car_price_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GQ3bkk0ZOiTSC9DDzfPNCR9xz3VtpxbC

## Exploratory Data Analysis
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
import warnings
warnings.filterwarnings('ignore')

!python data_clean.py

train_df=pd.read_csv('train.csv')
test_df=pd.read_csv('test.csv')
train_df.shape,test_df.shape

uniqueCities=dict(train_df['Location'].value_counts())

print(uniqueCities)

avgPriceAccToLocation=dict(train_df.groupby('Location')['Price'].mean())
plt.barh(list(avgPriceAccToLocation.keys()),list(avgPriceAccToLocation.values()))
plt.xlabel('AveragePrice')
plt.ylabel('Cities')
plt.title('Train Set : Average Price By Cities')
plt.show()

avgPriceAccToYear=dict(train_df.groupby('Year')['Price'].mean())
plt.barh(list(avgPriceAccToYear.keys()),list(avgPriceAccToYear.values()))
plt.xlabel('AveragePrice')
plt.ylabel('Year')
plt.title('Train Set : Average Price By Year')
plt.show()

train_df.head()

train_df.drop(['Unnamed: 0'],axis=1,inplace=True)
test_df.drop(['Unnamed: 0'],axis=1,inplace=True)

"""**No. of Rows for each City**"""

train_df['Location'].value_counts()

"""**No. of Rows for each Brand**"""

plt.figure(figsize=(10,10))
avgPriceAccToBrand=dict(train_df.groupby('Name')['Price'].mean())
plt.barh(list(avgPriceAccToBrand.keys()),list(avgPriceAccToBrand.values()))
plt.xlabel('AveragePrice')
plt.ylabel('Brand')

len(train_df['Name'].value_counts())  #1876 unqiue values.  high cardinality

len(train_df['Year'].value_counts())  #22 unqiue values.  high cardinality

means_name = train_df.groupby('Name')['Price'].mean().to_dict()
count=0
for model, mean_enc in means_name.items(): 
    print(model, ":", mean_enc)
    count=count+1
    if(count==5):
      break

means_location = train_df.groupby('Location')['Price'].mean().to_dict()
count=0
for loc, mean_enc in means_location.items(): 
    print(loc, ":", mean_enc)
    count=count+1
    if(count==5):
      break

means_year=train_df.groupby('Year')['Price'].mean().to_dict()
count=0
for year, mean_enc in means_year.items(): 
    print(year, ":", mean_enc)
    count=count+1
    if(count==5):
      break

"""## Target Encoding"""

# Source: https://maxhalford.github.io/blog/target-encoding-done-the-right-way/
def calc_smooth_mean(df1, df2, cat_name, target, weight):
    # Compute the global mean
    mean = df1[target].mean()

    # Compute the number of values and the mean of each group
    agg = df1.groupby(cat_name)[target].agg(['count', 'mean'])
    counts = agg['count']
    means = agg['mean']

    # Compute the "smoothed" means
    smooth = (counts * means + weight * mean) / (counts + weight)

    # Replace each value by the according smoothed mean
    if df2 is None:
        return df1[cat_name].map(smooth)
    else:
        return df1[cat_name].map(smooth),df2[cat_name].map(smooth.to_dict())

WEIGHT = 10
train_df['Name_enc'],test_df['Name_enc'] = calc_smooth_mean(df1=train_df, df2=test_df, cat_name='Name', target='Price', weight=WEIGHT)
train_df['Loc_enc'],test_df['Loc_enc'] = calc_smooth_mean(df1=train_df, df2=test_df, cat_name='Location', target='Price', weight=WEIGHT)
train_df['Yr_enc'],test_df['Yr_enc'] = calc_smooth_mean(df1=train_df, df2=test_df, cat_name='Year', target='Price', weight=WEIGHT)

train_df.drop(['Name','Location','Year'],axis=1,inplace=True)
test_df.drop(['Name','Location','Year'],axis=1,inplace=True)

train_df['owner_enc'],test_df['owner_enc'] = calc_smooth_mean(df1=train_df, df2=test_df, cat_name='Owner_Type', target='Price', weight=WEIGHT)
train_df['trans_enc'],test_df['trans_enc'] = calc_smooth_mean(df1=train_df, df2=test_df, cat_name='Transmission', target='Price', weight=WEIGHT)

train_df.drop(['Transmission','Owner_Type'],axis=1,inplace=True)
test_df.drop(['Transmission','Owner_Type'],axis=1,inplace=True)

train_df['fuel_enc'],test_df['fuel_enc'] = calc_smooth_mean(df1=train_df, df2=test_df, cat_name='Fuel_Type', target='Price', weight=WEIGHT)

train_df.drop(['Fuel_Type'],axis=1,inplace=True)
test_df.drop(['Fuel_Type'],axis=1,inplace=True)

import numpy as np
plt.figure(figsize=(10,5))
sns.distplot(np.log(train_df['Engine']),label='train')
sns.distplot(np.log(test_df['Engine']),label='test')
plt.legend()

"""Train and test set have similar ditribution."""

plt.figure(figsize=(10,5))
sns.distplot(np.log(train_df['Power']),label='train')
sns.distplot(np.log(test_df['Power']),label='test')
plt.legend()

#converting : log transform
train_df['Power']=np.log(train_df['Power'])
train_df['Engine']=np.log(train_df['Engine'])

#converting : log transform
test_df['Power']=np.log(test_df['Power'])
test_df['Engine']=np.log(test_df['Engine'])

train_df.shape,test_df.shape

test_df.isnull().any()   
#this checks if any column have missing values or not which is highly likely given the test set contains car that are
#not present in train.  For these rows replacing them with 0 makes sense.

# Name_enc and Yr_enc contains missing values.

test_df['Name_enc']=test_df['Name_enc'].fillna(0.0)
test_df['Yr_enc']=test_df['Yr_enc'].fillna(0.0)

train_df.to_csv('final_train.csv')
test_df.to_csv('final_test.csv')

target=train_df['Price']
train_df.drop(['Price'],inplace=True,axis=1)

train_df.columns

train_df=pd.read_csv('train.csv')
test_df=pd.read_csv('test.csv')
train_df.shape,test_df.shape

train_df.drop(['Unnamed: 0'],axis=1,inplace=True)
test_df.drop(['Unnamed: 0'],axis=1,inplace=True)

test_df['Name_enc'].fillna(test_df['Name_enc'].mean(),inplace=True)
test_df['Yr_enc'].fillna(test_df['Yr_enc'].mean(),inplace=True)

target=train_df['Price']
train_df.drop(['Price'],inplace=True,axis=1)

train_df=train_df.values

test_df=test_df.values

"""## Modelling
### Random Forest
"""

from sklearn.model_selection import RandomizedSearchCV
from pprint import pprint
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 500, num = 5)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(50, 110, num = 5)]
max_depth.append(None)
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
pprint(random_grid)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import make_scorer,mean_squared_error
rf=RandomForestRegressor(max_depth=110,n_estimators=400,min_samples_leaf=2,min_samples_split=2,max_features='auto')
kf=KFold(shuffle=True,random_state=123,n_splits=5)
splits=kf.split(train_df,target)
rmse_kf=[]
for trainIndex,valIndex in splits:
  X_train,X_val=train_df[trainIndex],train_df[valIndex]
  y_train,y_val=target[trainIndex],target[valIndex]
  rf.fit(X_train,y_train)
  preds=rf.predict(X_val)
  rmse_kf.append(mean_squared_error(y_val, preds))
  print("Split rmse: " + str(mean_squared_error(y_val, preds)))

np.array(rmse_kf).mean()   #mean mse for randomforest regressor after tuning

rf=RandomForestRegressor(max_depth=110,n_estimators=400,min_samples_leaf=2,min_samples_split=2,max_features='auto')
rf.fit(train_df,target)
preds_rf=rf.predict(test_df)

"""### XGboost"""

from xgboost import XGBRegressor
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')
xgtrain = xgb.DMatrix(train_df, label=target.values)

#finding numof boosting rounds and learning rate
alg = XGBRegressor(
 learning_rate =0.1,
 n_estimators=1000,
 max_depth=5,
 min_child_weight=1,
 gamma=0,
 subsample=0.8,
 colsample_bytree=0.8,
 objective= 'reg:squarederror',
 seed=27)

xgb_param = alg.get_xgb_params()

cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'], nfold=5,metrics='rmse', early_stopping_rounds=50)

n_estimators = cvresult.shape[0]

param_test1 = {
 'max_depth':range(3,10,2),
 'min_child_weight':range(1,6,2)
}

gsearch1 = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=n_estimators, max_depth=5,
 min_child_weight=1, gamma=0, subsample=0.8, colsample_bytree=0.8,
 objective= 'reg:squarederror', nthread=4, seed=27), 
 param_grid = param_test1, scoring=make_scorer(mean_squared_error),n_jobs=4,iid=False, cv=5)
gsearch1.fit(train_df,target)
gsearch1.best_params_, gsearch1.best_score_

param_test2b = {
 'max_depth':[13,15,16],  
}
gsearch2 = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=n_estimators, max_depth=5,
 min_child_weight=1, gamma=0, subsample=0.8, colsample_bytree=0.8,
 objective= 'reg:squarederror', nthread=4, seed=27), 
 param_grid = param_test2b, scoring=make_scorer(mean_squared_error),n_jobs=4,iid=False, cv=5)
gsearch2.fit(train_df,target)
gsearch2.best_params_, gsearch2.best_score_

param_test3 = {
 'gamma':[i/10.0 for i in range(0,5)]
}
gsearch3 = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=n_estimators, max_depth=13,
 min_child_weight=1, gamma=0, subsample=0.8, colsample_bytree=0.8,
 objective= 'reg:squarederror', nthread=4, seed=27), 
 param_grid = param_test3, scoring=make_scorer(mean_squared_error),n_jobs=4,iid=False, cv=5)
gsearch3.fit(train_df,target)
gsearch3.best_params_, gsearch3.best_score_

alg = XGBRegressor(
 learning_rate =0.1,
 n_estimators=1000,
 max_depth=13,
 min_child_weight=1,
 gamma=0.1,
 subsample=0.8,
 colsample_bytree=0.8,
 objective= 'reg:squarederror',
 seed=27)

xgb_param = alg.get_xgb_params()

cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'], nfold=5,metrics='rmse', early_stopping_rounds=50)

n_estimators=cvresult.shape[0]

xgb_reg=XGBRegressor(max_depth=13,learning_rate=0.1,n_estimators=213,objective='reg:squarederror',gamma=0.1,min_child_weight=1,seed=123)
kf=KFold(shuffle=True,random_state=123,n_splits=5)
splits=kf.split(train_df,target)
rmse_kf=[]
for trainIndex,valIndex in splits:
  X_train,X_val=train_df[trainIndex],train_df[valIndex]
  y_train,y_val=target[trainIndex],target[valIndex]
  xgb_reg.fit(X_train,y_train)
  preds=xgb_reg.predict(X_val)
  rmse_kf.append(mean_squared_error(y_val, preds))
  print("Split mse: " + str(mean_squared_error(y_val, preds)))

np.array(rmse_kf).mean()

"""We will tune the subsample and colsample_bytree parameters with values separated by 0.1 in first step"""

param_test4 = {
 'subsample':[i/10.0 for i in range(6,10)],
 'colsample_bytree':[i/10.0 for i in range(6,10)]
}
gsearch4 = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=n_estimators, max_depth=13,
 min_child_weight=1, gamma=0, subsample=0.8, colsample_bytree=0.8,
 objective= 'reg:squarederror', nthread=4, seed=27), 
 param_grid = param_test4, scoring=make_scorer(mean_squared_error),n_jobs=4,iid=False, cv=5)
gsearch4.fit(train_df,target)
gsearch4.best_params_, gsearch4.best_score_

"""We will tune the subsample and colsample_bytree parameters with values separated by 0.05 in first step"""

param_test4b = {
 'colsample_bytree':[i/100.0 for i in range(75,100,5)]
}
gsearch5 = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=n_estimators, max_depth=13,
 min_child_weight=1, gamma=0, subsample=0.8, colsample_bytree=0.8,
 objective= 'reg:squarederror', nthread=4, seed=27), 
 param_grid = param_test4b, scoring=make_scorer(mean_squared_error),n_jobs=4,iid=False, cv=5)
gsearch5.fit(train_df,target)
gsearch5.best_params_, gsearch5.best_score_

param_test4b = {
 'colsample_bytree':[0.95,1]
}
gsearch5 = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=n_estimators, max_depth=13,
 min_child_weight=1, gamma=0, subsample=0.9, colsample_bytree=0.8,
 objective= 'reg:squarederror', nthread=4, seed=27), 
 param_grid = param_test4b, scoring=make_scorer(mean_squared_error),n_jobs=4,iid=False, cv=5)
gsearch5.fit(train_df,target)
gsearch5.best_params_, gsearch5.best_score_

xgb_reg=XGBRegressor(max_depth=13,learning_rate=0.1,n_estimators=213,objective='reg:squarederror',gamma=0.1,min_child_weight=1,colsample_bytree=1,subsample=0.9,seed=123)
kf=KFold(shuffle=True,random_state=123,n_splits=5)
splits=kf.split(train_df,target)
rmse_kf=[]
for trainIndex,valIndex in splits:
  X_train,X_val=train_df[trainIndex],train_df[valIndex]
  y_train,y_val=target[trainIndex],target[valIndex]
  xgb_reg.fit(X_train,y_train)
  preds=xgb_reg.predict(X_val)
  rmse_kf.append(mean_squared_error(y_val, preds))
  print("Split mse: " + str(mean_squared_error(y_val, preds)))

np.array(rmse_kf).mean()   #a slight reduction

param_test7 = {
 'reg_alpha':[0, 0.001, 0.005, 0.01, 0.05]
}
gsearch6 = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=n_estimators, max_depth=13,
 min_child_weight=1, gamma=0.1, subsample=0.9, colsample_bytree=1,
 objective= 'reg:squarederror', nthread=4, reg_alpha=0 , seed=27), 
 param_grid = param_test7, scoring=make_scorer(mean_squared_error),n_jobs=4,iid=False, cv=5)
gsearch6.fit(train_df,target)
gsearch6.best_params_, gsearch6.best_score_

xgb_reg=XGBRegressor(max_depth=13,learning_rate=0.1,n_estimators=213,objective='reg:squarederror',gamma=0.1,min_child_weight=1,colsample_bytree=1,subsample=0.9,seed=123,reg_alpha=0)
kf=KFold(shuffle=True,random_state=123,n_splits=5)
splits=kf.split(train_df,target)
rmse_kf=[]
for trainIndex,valIndex in splits:
  X_train,X_val=train_df[trainIndex],train_df[valIndex]
  y_train,y_val=target[trainIndex],target[valIndex]
  xgb_reg.fit(X_train,y_train)
  preds=xgb_reg.predict(X_val)
  rmse_kf.append(mean_squared_error(y_val, preds))
  print("Split mse: " + str(mean_squared_error(y_val, preds))) 
np.array(rmse_kf).mean()   #a slight reduction

xgb_reg=XGBRegressor(max_depth=13,learning_rate=0.1,n_estimators=213,objective='reg:squarederror',gamma=0.1,min_child_weight=1,colsample_bytree=1,subsample=0.9,seed=123,reg_alpha=0)
xgb_reg.fit(train_df,target)
preds_xgb=xgb_reg.predict(test_df)

preds_rf[:5]

preds_xgb[:5]

submit=pd.read_excel('0.77.xlsx')

submit['Price']=(preds_xgb+preds_rf)/2

submit.to_csv('rf+xgb.csv')

"""### LightGBM"""

import lightgbm as lgb

params = {
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': 'mse',
    'max_depth': 6, 
    'learning_rate': 0.1,
    'verbose': 0, 
    'early_stopping_round': 50}
n_estimators = 1000

lgb_train=lgb.Dataset(train_df,label=target)
cvresult=lgb.cv(params,lgb_train,num_boost_round=n_estimators,nfold=5,stratified=False,seed=123)

len(cvresult['l2-mean'])

n_estimators=305

param_test1 = {
 'max_depth':range(3,10,2),
}

lgb_reg=lgb.LGBMRegressor(objective='regression',learning_rate=0.1,n_estimators=n_estimators,max_depth=8,metric='mse')
gsearch1 = GridSearchCV(param_grid=param_test1,estimator = lgb_reg,n_jobs=4,iid=False, cv=5)
gsearch1.fit(train_df,target)
gsearch1.best_params_, gsearch1.best_score_

param_test2 = {
 'num_leaves':[70,80,90,100]
}
lgb_reg=lgb.LGBMRegressor(objective='regression',learning_rate=0.1,n_estimators=n_estimators,max_depth=7,metric='mse',num_leaves=31)
gsearch2 = GridSearchCV(param_grid=param_test2,estimator = lgb_reg,n_jobs=4,iid=False, cv=5)
gsearch2.fit(train_df,target)
gsearch2.best_params_, gsearch2.best_score_

params = {
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': 'mse',
    'max_depth': 7,
    'num_leaves':70,
    'learning_rate': 0.1,
    'verbose': 0, 
    'early_stopping_round': 50}
n_estimators = 1000

lgb_train=lgb.Dataset(train_df,label=target)
cvresult=lgb.cv(params,lgb_train,num_boost_round=n_estimators,nfold=5,stratified=False,seed=123)

n_estimators=len(cvresult['l2-mean'])

lgb_reg=lgb.LGBMRegressor(boosting_type='gbdt',objective='regression',learning_rate=0.1,n_estimators=n_estimators,max_depth=7,metric='mse',num_leaves=70)
kf=KFold(shuffle=True,random_state=123,n_splits=5)
splits=kf.split(train_df,target)
rmse_kf=[]
for trainIndex,valIndex in splits:
  X_train,X_val=train_df[trainIndex],train_df[valIndex]
  y_train,y_val=target[trainIndex],target[valIndex]
  lgb_reg.fit(X_train,y_train)
  preds=lgb_reg.predict(X_val)
  rmse_kf.append(mean_squared_error(y_val, preds))
  print("Split mse: " + str(mean_squared_error(y_val, preds))) 
np.array(rmse_kf).mean()   #a slight reduction

lgb_reg=lgb.LGBMRegressor(boosting_type='gbdt',objective='regression',learning_rate=0.1,n_estimators=n_estimators,max_depth=7,metric='mse',num_leaves=70)
lgb_reg.fit(train_df,target)
preds_lgb=lgb_reg.predict(test_df)

train_df.shape

"""### Artificial Neural Network"""

# Feature Scaling
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
X_train = sc.fit_transform(train_df)
X_test = sc.transform(test_df)

# Evaluating, Improving and Tuning the ANN

# Evaluating the ANN
from sklearn.model_selection import cross_val_score
from tensorflow.contrib.keras.api.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV
from tensorflow.contrib.keras.api.keras.models import Sequential
from tensorflow.contrib.keras.api.keras.layers import Dense, Dropout
from tensorflow.contrib.keras import backend

def build_regressor():
    regressor = Sequential()
    regressor.add(Dense(units=6, kernel_initializer='uniform', activation='relu', input_dim=11))
    regressor.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))
    regressor.add(Dense(units=1, kernel_initializer='uniform', activation='linear'))
    regressor.compile(optimizer='adam', loss='mean_squared_error')
    return regressor


regressor = KerasRegressor(build_fn=build_regressor, batch_size=10, epochs=10)
# cv = 10 is the usual number used for cross validation (it runs 10 different experiments)
accuracies = cross_val_score(estimator=regressor, X=X_train, y=target, cv=10, n_jobs=1,scoring=make_scorer(mean_squared_error))
mean = accuracies.mean()
variance = accuracies.std()

# Tuning the ANN
def build_regressor(optimizer):
    regressor = Sequential()
    regressor.add(Dense(units=6, kernel_initializer='uniform', activation='relu', input_dim=11))
    # Improving the ANN
    # Dropout Regularization to reduce overfitting if needed
    regressor.add(Dropout(0.1))
    regressor.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))
    regressor.add(Dense(units=1, kernel_initializer='uniform', activation='linear'))
    regressor.compile(optimizer=optimizer, loss='mean_squared_error')
    return regressor


regressor = KerasClassifier(build_fn=build_classifier)
parameters = {'batch_size': [25, 32],
              'epochs': [10, 50],
              'optimizer': ['adam', 'rmsprop']}
grid_search = GridSearchCV(estimator=regressor,
                           param_grid=parameters,
                           scoring='accuracy',
                           cv=10)
grid_search = grid_search.fit(X_train, target)
best_parameters = grid_search.best_params_
best_accuracy = grid_search.best_score_
backend.clear_session()