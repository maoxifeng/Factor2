# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 10:58:43 2017

@author: liusl
"""

'''
#==============================================================================
# ROE factor return function
#==============================================================================
'''
#
#import numpy as np
#import scipy.io as sio
#import pandas as pd
#import os
#import cPickle as cp
import Common.TimeCodeGet as tc
import FundamentalData.ROE.sheetDicGet as roesd
import FundamentalData.FunCommon.FactorReturnGet as facret


# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)

factName = 'ROE'
ROESavePathMain = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ReturnOnEquity/'

#%% 1. calculate ROE 

dataROEDic = roesd.ROE_FMDicGet()
#%% 2. seperate groups, and get FM returns, FM Exposure, save file 

# all stock return and exposure
#==============================================================================
ROEReturnFolderPath = facret.FactorFMReturnGet(dataROEDic, savePath=ROESavePathMain, facName=factName, pool='A')
facret.FactorFMExposureGet(ROEReturnFolderPath, facName=factName, pool='A')


#%% HS300 return and exposure
#==============================================================================
ROEHS300ReturnPath = facret.FactorFMReturnGet(dataROEDic, savePath=ROESavePathMain, pool='HS300', facName=factName)
ROE_HS300_Exposure = facret.FactorFMExposureGet(ROEHS300ReturnPath, facName=factName, pool='HS300')

    
    
    
    
    
    
    
    
