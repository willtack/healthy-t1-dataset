#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:37:13 2021

@author: seburke
some modifications by willtack
"""

import pandas as pd
import numpy as np
import os
import glob

os.chdir('/media/will/My Passport/Ubuntu/cortical_thickness_maps/stats')
files = glob.glob('*schaefer.csv')

##optional create id list from filenames for importing predictor variables
id_list=[]
for j in range(0,len(files)):
    ids=files[j].split("_")
    id_list.append(ids[0])

#read in csv with extracted thickness/volume values per label and combine
combined_ct=pd.concat([pd.read_csv(f) for f in files])

#filter for atlas system and for measures of interest
temp_vals=combined_ct[combined_ct.type=="mean"]
temp_vals=temp_vals.reset_index(drop=True)

#read in age data - or whatever demos to be used as predictor variables
age_vals=pd.read_excel('/home/will/Projects/healthy-t1-dataset/metadata.xlsx')

#read in atlas labels key and create index of label id #s
atlas=pd.read_csv('/home/will/Projects/healthy-t1-dataset/labels/Schaefer2018_200Parcels_17Networks_order.csv')
wblabs=atlas["label_number"]

#define function needed to calculate standard error of regressors
import math
def RSE(y_true, y_predicted):
    y_true = np.array(y_true)
    y_predicted=np.array(y_predicted)
    RSS=np.sum(np.square(y_true-y_predicted))

    rse=math.sqrt(RSS / (len(y_true)-2))
    return rse


#loop through each label and plug data into linear model
tmpB1=pd.DataFrame()
for ind in range(0,len(wblabs)):
  i=wblabs[ind]
  tmplabs=temp_vals[temp_vals['label_number'] == i]
  df=pd.DataFrame(tmplabs.value)
  df=pd.concat([df.reset_index(drop=True), age_vals], axis=1)

#loop through each label and plug data into linear model
from sklearn.linear_model import LinearRegression

tmpB1=pd.DataFrame()
int_coff=[]
target_coff=[]
rse=[]
ilabs=[]
for ind in range(0,len(wblabs)):
  i=wblabs[ind]
  tmplabs=temp_vals[temp_vals['label_number'] == i]
  df=pd.DataFrame(tmplabs.value)
  df=pd.concat([df.reset_index(drop=True), age_vals], axis=1)
  X= df['Age'].values.reshape(-1,1)
  Y= df['value'].values.reshape(-1,1)
  linear_regressor = LinearRegression()  # create object for the class
  linear_regressor.fit(X, Y)  # perform linear regression
  Y_pred=linear_regressor.predict(X)  # make predictions
  int_coff.append(linear_regressor.intercept_[0])
  target_coff.append(linear_regressor.coef_[0][0])
  rse.append(RSE(Y,Y_pred))
  ilabs.append(i)

wsCoffs = pd.DataFrame.from_dict({
    'label_number':ilabs,
    'intercept':int_coff,
    'age_coefficient':target_coff,
    'residual_se':rse,
    })


wsCoffs.to_csv('/home/will/Projects/healthy-t1-dataset/ws_coeffs.csv', index=False)