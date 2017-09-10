# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 09:56:49 2017

@author: liusl
"""
'''
#==============================================================================
# calculate Investments to Assets formative values
#==============================================================================
'''
import numpy as np
import scipy.io as sio
import cPickle as cp
import pandas as pd
import time
import Common.TimeCodeGet as tc
import FundamentalData.IA.IADicGet as idg
import Common.UpdateDataGet as cu
# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)

factName = 'IA'
savePathMain = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/InvestmentsToAssets/'

#%% to formative values, save to 3D array

IADF = idg.IABarraExposureGet()
cu.UpdateFormDataGet(IADF, savePath=savePathMain, facName=factName+'_BarraExposure')


#%% Barra Return
import FundamentalData.FunCommon.FactorReturnGet as facret

# all stock return
IA_A_BarraReturn = facret.FactorBarraReturnGet(loadDF=IADF, facPath=savePathMain, facName=factName, pool='A')


# HS300 return
IA_HS300_BarraReturn = facret.FactorBarraReturnGet(loadDF=IADF, facPath=savePathMain, facName=factName, pool='HS300')



