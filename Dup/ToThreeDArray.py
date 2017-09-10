#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 10:44:36 2017

@author: liushuanglong
"""


import numpy as np
import pandas as pd
import scipy.io as sio



# load data series
pathTS =  '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat'     
dataTSRaw = sio.loadmat(pathTS)      
dataTSArr = dataTSRaw['data'][:, 0]     # 6498
    


# load code
pathCode = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
dataCode =  sio.loadmat(pathCode)
dataComCodeTol = dataCode['data'].T[1]   # 3415

# load  NetProfit data
pathNetProfit = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalData/LC_IncomeStatementNew_Total_NetProfit_YearDuration_DicUse.pkl'
dataNetProfitDic = cp.load(open(pathNetProfit, 'r'))

dataComCodeUse = sorted(dataNetProfitDic.keys())   # 3414   companies





# create a dic contain all effective date
dataNetProfitDicTolTime = {}
for code in dataComCodeUse:
    dataOneCodeTolDF = dataNetProfitDic[code].sort_index()
    dataOneCodeTSRaw = dataOneCodeTolDF.index.tolist()
    dataOneCodeTSTol = sorted(set(dataTSArr) | set(dataOneCodeTSRaw))
    dataOneCodeUseDF = dataOneCodeTolDF.reindex(dataOneCodeTSTol, method='ffill').loc[dataTSArr]
    dataNetProfitDicTolTime[code] = dataOneCodeUseDF
    
    
# save netprofit as 3D array   , total codes
dataTolNetProfitArr = np.zeros((3, len(dataTSArr), len(dataComCodeTol)))           # use not financial codes
itemNames = [u'NetProfit', u'EndDate', u'Mark']

dataNetProfitValueDF = pd.DataFrame([], index=dataTSArr, columns=dataComCodeTol)
dataNetProfitEndDateDF = pd.DataFrame([], index=dataTSArr, columns=dataComCodeTol)
dataNetProfitMarkDF = pd.DataFrame([], index=dataTSArr, columns=dataComCodeTol)
for code in dataComCodeUse:
    dataNetProfitValueDF[code] = dataNetProfitDicTolTime[code][itemNames[0]]
    dataNetProfitEndDateDF[code] = dataNetProfitDicTolTime[code][itemNames[1]]
    dataNetProfitMarkDF[code] = dataNetProfitDicTolTime[code][itemNames[2]]
#
## save as pkl
#dicNetProfitPkl = {u'NetProfit': dataNetProfitValueDF, u'EndDate': dataNetProfitEndDateDF, u'Mark': dataNetProfitMarkDF}
#cp.dump(dicNetProfitPkl, open("/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalData/LC_IncomeStatementNew_Total_NetProfit_YearDuration_3items.pkl", "w")) 


    
# save netprofit in 3D array       
dataTolNetProfitArr[0] = dataNetProfitValueDF.values      # net profit
dataTolNetProfitArr[1] = dataNetProfitEndDateDF.values    # end date
dataTolNetProfitArr[2] = dataNetProfitMarkDF.values      # mark


itemNamesArr = np.zeros((1, len(itemNames)), dtype=object)
for i, j in enumerate(itemNames):
    itemNamesArr[0][i] = np.array([j])

dataDic = {'axis1_itemNames': itemNamesArr, \
           'axis2_indexTime': dataTSArr.reshape(len(dataTSArr), 1), \
           'axis3_colCompanyCode': dataComCodeTol, \
           'LC_IncomeStatementNew_Total_NetProfit_YearDuration': dataTolNetProfitArr}
           
sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalData/LC_IncomeStatementNew_Total_NetProfit_YearDuration_arr.mat', dataDic)

























