# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:37:47 2017

@author: liusl
"""


import numpy as np
import scipy.io as sio
import pandas as pd
import cPickle as cp
import time
import Common.TimeCodeGet as tc
import FundamentalData.IA.IADicGet as idg
import FundamentalData.FunCommon.FactorReturnGet as facret
# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)

factName = 'IA'
savePathMain = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/InvestmentsToAssets/'

#%% IA data dic
dataIADic = idg.IAFMDicGet()


#%% all stocks return and exposure
IAReturnFolderPath = facret.FactorFMReturnGet(dataIADic, savePath=savePathMain, facName=factName, pool='A')
facret.FactorFMExposureGet(IAReturnFolderPath, facName=factName, pool='A')


#%% HS300 return and exposure
IAHS300ReturnPath = facret.FactorFMReturnGet(dataIADic, savePath=savePathMain, pool='HS300', facName=factName)
IA_HS300_Exposure = facret.FactorFMExposureGet(IAHS300ReturnPath, facName=factName, pool='HS300')




