# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 14:19:25 2017

@author: liusl
"""


import numpy as np
import scipy.io as sio
import pandas as pd
import os
import time
import statsmodels.api as sm
import Common.TimeCodeGet as tc
import Common.SmaFun as cs
import FundamentalData.CommonData.ComDataGet as ccd

# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)


#%% AFloats
_ = ccd.AFloatsGet()

#%%
