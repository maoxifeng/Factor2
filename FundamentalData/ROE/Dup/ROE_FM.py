# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 16:04:58 2017

@author: liusl
"""

'''
#==============================================================================
# ROE factor return function
#==============================================================================
'''

import numpy as np
import scipy.io as sio
import pandas as pd
import cPickle as cp
import Common.TimeCodeGet as tc

# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)

ROESavePath = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/'

#==============================================================================
# 1. calculate ROE 
#==============================================================================

import FundamentalData.ROE.sheetDicGet as sd

dataTolIncomeDic = sd.netprofitGet()
print 'netprofitDic completed'

dataTolBalanceDic = sd.equityGet()
print 'equity completed'


#    # create a new df dict

netprofitDic = {}   
for number, code in enumerate(dataTolIncomeDic.keys()):    
    dfIncomeOneCode = dataTolIncomeDic[code]
    pubDateArr = np.unique(dfIncomeOneCode.index)              
    pubYearArr = np.unique([int(i)/10000 for i in pubDateArr])
    dfOneCodeUse = pd.DataFrame(columns=[u'NetProfit'])
    for year in pubYearArr:
        dateIndArr = np.where((pubDateArr>(year*10000)) & (pubDateArr<(year*10000+501)))[0]
        pubDateUseArr = pubDateArr[dateIndArr]  # array
        lastYearDate = (year-1) * 10000 + 1231
        if (len(dateIndArr) > 0) & (lastYearDate in dfIncomeOneCode.loc[pubDateUseArr, u'EndDate'].values):
            dfIncomOneCodeTemp = dfIncomeOneCode.loc[pubDateUseArr]   # is a df
            dfIncomOneCodeTemp = dfIncomOneCodeTemp[dfIncomOneCodeTemp[u'EndDate'] == lastYearDate].iloc[-1] # is a series
            dfOneCodeUse.loc[year, u'NetProfit'] = dfIncomOneCodeTemp[u'NetProfit']
    netprofitDic[code] = dfOneCodeUse

equityDic = {}   
for number, code in enumerate(dataTolBalanceDic.keys()):    
    dfBalanceCode = dataTolIncomeDic[code]
    pubDateArr = np.unique(dfBalanceCode.index)              
    pubYearArr = np.unique([int(i)/10000 for i in pubDateArr])
    dfOneCodeUse = pd.DataFrame(columns=[u'equity'])
    for year in pubYearArr:
        dateIndArr = np.where((pubDateArr>(year*10000)) & (pubDateArr<(year*10000+501)))[0]
        pubDateUseArr = pubDateArr[dateIndArr]
        lastYearDate = (year-1) * 10000 + 1231
        if (len(dateIndArr) > 0) & (lastYearDate in dfBalanceCode.loc[pubDateUseArr, u'EndDate'].values):
            dfBalanceOneCodeTemp = dfBalanceCode.loc[pubDateUseArr]
            dfBalanceOneCodeTemp = dfBalanceOneCodeTemp[dfBalanceOneCodeTemp[u'EndDate'] == lastYearDate].iloc[-1, 2:]
            dfOneCodeUse.loc[year, u'equity'] = dfBalanceOneCodeTemp.sum()
    equityDic[code] = dfOneCodeUse


comCodeUseLis = list(set(netprofitDic.keys()) & set(equityDic.keys()))
dataROEDic = {}
for i, code in enumerate(comCodeUseLis):
    netOneCodeDF = netprofitDic[code]
    equityOneCodeDF = equityDic[code]
    ROEOneCodeDF = pd.concat([netOneCodeDF, equityOneCodeDF], axis=1)
    if ROEOneCodeDF.size != 0:
        ROETempDF = pd.DataFrame(columns=['ROE'])
        ROETempDF['ROE'] = ROEOneCodeDF[u'NetProfit'] / ROEOneCodeDF[u'equity']  # use innercode as columns names
        dataROEDic[code] = ROETempDF
#%% 
#cp.dump(dataROEDic, open('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/ROE_FiscalYearValuesDic.pkl', 'w'))
#==============================================================================
# 2. seperate groups, and get FM returns, FM Exposure, save file
#==============================================================================
import FundamentalData.FunCommon.FactorReturnGet as facret

#==============================================================================
# all stock return and exposure
#==============================================================================
ROEReturnArr, ROEReturnPath = facret.FactorFMReturnGet(dataROEDic, savePath=ROESavePath, facName='ROE')
ROE_AExposure = facret.FactorFMExposureGet(ROEReturnPath, facName_Pool='ROE_A_StoFree')

#==============================================================================
# HS300 return and exposure
#==============================================================================
ROEHS300ReturnArr, ROEHS30ReturnPath = facret.FactorFMReturnGet(dataROEDic, savePath=ROESavePath, pool='HS300', facName='ROE')
ROE_HS300_Exposure = facret.FactorFMExposureGet(ROEHS30ReturnPath, facName_Pool='ROE_HS300_StoFree')

    
    
    
    
    
    
    
    
