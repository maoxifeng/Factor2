# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 10:58:23 2017

@author: liusl
"""


'''
This program is to calculate ROE formative values and then barra return.

Netprofit is calculated as the year duration data at the newest date.

'''


#import numpy as np
#import pandas as pd
#import scipy.io as sio
#import cPickle as cp
#import time
import Common.UpdateDataGet as cu
import Common.TimeCodeGet as tc
import FundamentalData.ROE.sheetDicGet as roesd

dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)

factName = 'ROE'
ROESavePathMain = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ReturnOnEquity/'

#%% 1. calculate ROE 

dataROEDF = roesd.ROE_BarraDicGet()
cu.UpdateFormDataGet(dataROEDF, savePath=ROESavePathMain, facName=factName+'_BarraExposure')

#%% 2. Barra Return

import FundamentalData.FunCommon.FactorReturnGet as facret

# all stock return
ROE_A_BarraReturn = facret.FactorBarraReturnGet(loadDF=dataROEDF, facPath=ROESavePathMain, facName=factName, pool='A')

# HS300 return
ROEHS300_BarraReturn = facret.FactorBarraReturnGet(loadDF=dataROEDF, facPath=ROESavePathMain, facName=factName, pool='HS300')































