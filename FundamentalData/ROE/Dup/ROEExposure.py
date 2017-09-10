#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 14:15:57 2017

@author: liushuanglong
"""


import numpy as np
import scipy.io as sio
import pandas as pd
import cPickle as cp
import statsmodels.api as sm



#==============================================================================
# 1. load data, stock return, ROE return
#==============================================================================
pathTS =  '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat'     
dataTSRaw = sio.loadmat(pathTS)      
dataTSArr = dataTSRaw['data'][:, 0]     # 6498
dataTSDic = {'dataTSArr': dataTSArr}

pathCode = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
dataCodeRaw = sio.loadmat(pathCode)
dataCodeArr = dataCodeRaw['data']
dataInnerCodeArr = dataCodeArr[:, 0]    # 3415
dataComCodeArr = dataCodeArr[:, 1]
dataCodeNumDic = {'dataInnerCodeArr': dataInnerCodeArr, 'dataComCodeArr': dataComCodeArr}


# bond log return
pathBond = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/Wind_Daily_10YearBond_LogReturn_mat.mat'
dataBondRaw = sio.loadmat(pathBond)
dataBondArr = dataBondRaw['daily_10YearBond_LogReturn']


# ROE return 
pathROEReturn = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_YearDuration_ROE_3Groups_Return_2_mat.mat'
dataROEReturnRaw = sio.loadmat(pathROEReturn)
dataROEReturnRaw.keys()
dataROEReturnArr = dataROEReturnRaw['LC_YearDuration_ROE_3Groups_Return_2_mat']
dataROEReturnArr.shape


# load stock log return
pathStoReturn = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_mat.mat'
dataStoReturnRaw = sio.loadmat(pathStoReturn) 
dataStoReturnArr = dataStoReturnRaw['DailyQuote_LogReturn']
dataStoReturnArr.shape

#==============================================================================
# 2. calculate stock free return, ROE free return
#==============================================================================
effTSNumber = len(set(dataTSArr) & set(dataBondArr[:, 0]))
dataTSEffArr = dataTSArr[-effTSNumber:]  # 3764

#dataBondDF = pd.DataFrame(dataBondArr, columns=['date', 'logReturn'])
#dataBondDF.set_index('date', inplace=True)
#dataBondUseDF = dataBondDF.reindex(dataTSArr)
#dataBondUseDF.shape

dataBondUseDF = dataBondArr[:effTSNumber, [1]]

# stock free return
dataStoFreeReturnUseArr = dataStoReturnArr[-effTSNumber:, :]   
dataStoFreeReturnUseArr = dataStoFreeReturnUseArr - dataBondUseDF    
dataStoFreeReturnUseArr.shape
# ROE 
dataROEReturnUseArr = dataROEReturnArr[-effTSNumber:, :]      
dataROEReturnUseArr.shape

#==============================================================================
# calculate every stock ROE exposure
#==============================================================================

#def ROEExposureGet(day=100):
day = 100
percent = 0.4
X = sm.add_constant(dataROEReturnUseArr[:, 3])
X.shape    


dataROEBetaArr = np.ones_like(dataStoFreeReturnUseArr)
dataROEBetaArr[:] = np.nan
dataROEAlpArr = np.ones_like(dataStoFreeReturnUseArr)
dataROEAlpArr[:] = np.nan

for d in range(day-1, effTSNumber):
    arrTemp = dataStoFreeReturnUseArr[(d-day+1):(d+1)]
    Xtemp = X[(d-day+1):(d+1)]
    for s in range(len(dataInnerCodeArr)):
        useIndArr = np.where(~np.isnan(arrTemp[:, s]))[0]
        if len(useIndArr) > (day * percent):
            result = sm.OLS(arrTemp[useIndArr, s], Xtemp[useIndArr]).fit()
            dataROEAlpArr[d, s] = result.params[0]
            dataROEBetaArr[d, s] = result.params[1]
    if d%20 == 0:
        print d,
            
# save data

colArr = np.zeros((1, 1)), dtype=object))
for i, j in enumerate(['ROEBeta']):
    colArr[0][i] = np.array([j])

dataDic = {'col': colArr, 'ROEBeta':dataROEBetaArr}

dic = {'ROEBeta':  dataROEBetaArr, 'ROEAlpha': dataROEAlpArr}
#cp.dump(dic, open('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROEExposure100day.pkl', 'w'))


# save ROE exposure as .mat
import cPickle as cp
dataDic = cp.load(open('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROEExposure100day.pkl', 'r'))           


import Common.TimeCodeGet as tc

# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)

dataArr = dataDic['ROEBeta']
dataFor = np.zeros((6498, 3415))
dataFor[:] = np.nan
dataFor[-3764:] = dataArr


arrNames = 'Factor_FMExposure' + '_' + str(100) + 'regDays'
dataDic={'colInnerCode': dataInnerCodeArr, 
         'indDate': dataDSArr.reshape(len(dataDSArr), 1),
         arrNames: dataFor}

#sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE//ROE_FMExpolure_array.mat', dataDic)



#==============================================================================
# calculate ROE Exposure use HS300 ROE FM return 
#==============================================================================

pathROE300Return = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/LC_YearDuration_HS300_ROE_3Groups_Return_mat.mat'

ROEHS300RetDic = sio.loadmat(pathROE300Return)
aa = 'LC_YearDuration_HS300_ROE_3Groups_Return_mat'

import FundamentalData.FunCommon.FactorReturnGet as fr

savePathROE300 = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/'
ROEHS300Exp = fr.FactorFMExposureGet(FMReturnPath=pathROE300Return, itemsName=aa, savePath=savePathROE300, facName_Pool='ROE_HS300')

















































