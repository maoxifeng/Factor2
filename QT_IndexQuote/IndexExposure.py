# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 16:58:22 2017

@author: liusl
"""


import numpy as np
import scipy.io as sio
import pandas as pd
import Common.TimeCodeGet as tc

dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)




import FundamentalData.FunCommon.FactorReturnGet as facret

HS300_IndexReturnPath = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/IndexQuote_HS300_LogReturn_arr.mat'
HS300_IndexExposure = facret.FactorFMExposureGet(loadPath=HS300_IndexReturnPath, index=0, facName_Pool='HS300Index')

# free return
HS300_Index_FreeReturnPath = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/IndexQuote_HS300Free_LogReturn_arr.mat'
HS300_IndexExposure = facret.FactorFMExposureGet(loadPath=HS300_Index_FreeReturnPath, index=0, facName_Pool='HS300Index_Free')





