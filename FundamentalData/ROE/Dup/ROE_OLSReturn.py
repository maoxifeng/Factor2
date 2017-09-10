#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 09:05:03 2017

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


# ROR values
pathROEValue = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_Total_ROE_YearDuration_mat.mat'
dataROEValueRaw = sio.loadmat(pathROEValue)
dataROEValueRaw.keys()
dataROEValueArr = dataROEValueRaw['LC_Total_ROE_YearDuration'][0]
dataROEValueArr.shape

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


# ROE standardize 
#dataROEReturnUseArr = dataROEReturnArr[-effTSNumber:, :]      
#dataROEReturnUseArr.shape
dataROEValueUseArr = dataROEValueArr[-effTSNumber:, :]
dataROEStandArr = np.zeros_like(dataROEValueUseArr)
dataROEStandArr[:] = np.nan

for i in range(len(dataROEValueUseArr)):
    dataROEValueTemp = dataROEValueUseArr[i][~np.isnan(dataROEValueUseArr[i])]
    dataMeanTemp = np.mean(dataROEValueTemp)
    dataStdTemp = np.std(dataROEValueTemp)
    dataROEStandArr[i] = (dataROEValueUseArr[i] - dataMeanTemp) / dataStdTemp

#==============================================================================
# calculate cross section ROE return
#==============================================================================

#def ROEExposureGet(day=100):
        
dataROEOLSReturn = np.zeros((effTSNumber, 1))        
dataROEOLSReturn[:] = np.nan
dataCounts = []

for i in range(len(dataROEStandArr)):
    useBool = (~np.isnan(dataROEStandArr[i])) & (~np.isnan(dataStoFreeReturnUseArr[i]))
    Xuse = dataROEStandArr[i][useBool]
    dataCounts.append(len(Xuse))
    Yuse = dataStoFreeReturnUseArr[i][useBool]
    X = sm.add_constant(Xuse)
    result = sm.OLS(Yuse, X).fit()
    dataROEOLSReturn[i, 0] = result.params[1]
    if i%100 == 0:
        print i,
    
# save data
dataROEReturnDF = pd.DataFrame(columns=['OLSReturn', 'HMLReturn'])
dataROEReturnDF['OLSReturn'] = dataROEOLSReturn[:, 0]
dataROEReturnDF['HMLReturn'] = dataROEReturnArr[-effTSNumber:, 3]




import scipy.stats as stats
cor1, pval1 = stats.pearsonr(dataROEReturnDF['OLSReturn'].values, dataROEReturnDF['HMLReturn'].values)
cor2, pval2 = stats.spearmanr(dataROEReturnDF['OLSReturn'].values, dataROEReturnDF['HMLReturn'].values)



colArr = np.zeros((1, len(dataROEReturnDF.columns)), dtype=object)
for i, j in enumerate(dataROEReturnDF.columns):
    colArr[0][i] = np.array([j])

dataDic = {'col': colArr, 'index':dataTSRaw['data'][-effTSNumber:], 'ROEReturn': dataROEReturnDF.values}
sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROEReturn_TwoMethods_arr.mat', dataDic)


cor1
cor2







#dic = {'ROEBeta':  dataROEBetaArr, 'ROEAlpha': dataROEAlpArr}
#cp.dump(dic, open('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROEExposure100day.pkl', 'w'))


           





















































