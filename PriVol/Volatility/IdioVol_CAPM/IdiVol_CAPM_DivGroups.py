# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 09:53:14 2017

@author: liusl
"""


import numpy as np
import scipy.io as sio
import pandas as pd
import os
import time
import statsmodels.api as sm
import Common.TimeCodeGet as tc
import Common.SmaFun as sf

# load time and code 
#dataDSArr = tc.dateSerArrGet()[:, 0]
#dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
#dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)

#savePath = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/TraVol/IdioVolatility_CAPM/'
pathIdiVol = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/TraVol/IdioVolatility_CAPM/IdioVol_CAPM_250RDs_arr.mat'

import FundamentalData.FunCommon.FacAnaGet as facana

facName='IdiVol_CAPM'


#%%
IdiVol_HS300_GroReturn, IdiVol_HS300_GroReturnPath = facana.DivGroRetGet(loadPath=pathIdiVol, facName=facName, divGroNum=10, pool='HS300')
facana.DivGroRetGraphGet(loadPath=IdiVol_HS300_GroReturnPath, facName_Pool=facName+'_HS300')


#%%

IdiVol_A_GroReturn, IdiVol_A_GroReturnPath = facana.DivGroRetGet(loadPath=pathIdiVol, facName=facName, divGroNum=10, pool='A')
facana.DivGroRetGraphGet(loadPath=IdiVol_A_GroReturnPath, facName_Pool=facName+'_A')


