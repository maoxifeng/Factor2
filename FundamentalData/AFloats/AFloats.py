#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 13:53:38 2017

@author: liushuanglong
"""



import numpy as np
import scipy.io as sio
import pandas as pd
import cPickle as cp



# load code
pathCode = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
dataCode =  sio.loadmat(pathCode)
dataComCodeArr = dataCode['data'].T[1]   # 3415


# load income statement new data
pathST = '/home/liushuanglong/MyFiles/Data/JYDB2/LC_ShareStru/sharestru_mat.mat'
dataRaw = sio.loadmat(pathST)  
dataColTol = [dataRaw['col'][0][i][0] for i in range(dataRaw['col'].shape[1])]
#dataColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'AFloats']
dataColUseLis = [u'CompanyCode', u'EndDate', u'AFloats']
dataColUseInd = [dataColTol.index(i) for i in dataColUseLis]
dataValuesTolArr = dataRaw['data'][:, dataColUseInd]  # 171506


# dataframe, select by company code and mark
dataValuesTolDF = pd.DataFrame(dataValuesTolArr, columns=dataColUseLis)    # 
dataValuesTolDF = dataValuesTolDF[dataValuesTolDF[u'CompanyCode'].isin(dataComCodeArr)]  # 145276
#dateError = dataValuesTolDF[dataValuesTolDF[u'InfoPublDate'].isnull()]


# drop nan values
#dataValuesUseDF = dataValuesTolDF[dataValuesTolDF[u'InfoPublDate']!=1010101]  

# sort by company code, end date, mark
dataValuesUseDFSor = dataValuesTolDF.sort_values(by=[u'CompanyCode',u'EndDate'])
dataValuesUseDFSor = dataValuesUseDFSor.drop_duplicates(subset=[u'CompanyCode',u'EndDate'])
dataComCodeUse = np.unique(dataValuesUseDFSor[u'CompanyCode'])             # used company code, 3415 counts

# create  df dict of total data
dataValuesUseDFInd = dataValuesUseDFSor.set_index([u'CompanyCode',u'EndDate'])

dataValuesDic = {}
for code in dataComCodeUse:
    dataValuesDic[code] = dataValuesUseDFInd.loc[code]



# load data series
pathTS =  '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat'     
dataTSRaw = sio.loadmat(pathTS)      
dataTSArr = dataTSRaw['data'][:, 0]     # 6498
    

# create a dic contain all effective date
dataValuesUseDic = {}
for code in dataComCodeUse:
    dataOneCodeTolDF = dataValuesDic[code]
    dataOneCodeTolDF[u'EndDate'] = dataOneCodeTolDF.index
    dataOneCodeTSRaw = dataOneCodeTolDF.index.tolist()
    dataOneCodeTSTol = sorted(set(dataTSArr) | set(dataOneCodeTSRaw))
    dataOneCodeUseDF = dataOneCodeTolDF.reindex(dataOneCodeTSTol, method='ffill').loc[dataTSArr]
    dataValuesUseDic[code] = dataOneCodeUseDF




# not use, create the dict of used values
#dataValuesUseDic = {}
#for code in dataComCodeUse:
#    dataValuesOneCodeDFTemp = dataValuesDic[code]
#    dataValuesOneCodePubDateArr = np.unique(dataValuesOneCodeDFTemp.index) 
#    dataValuesOneCodeDF = pd.DataFrame([], columns=[u'EndDate', u'AFloats'])
#    for day in dataValuesOneCodePubDateArr:
#        dataValuesOneCodeArrTemp = dataValuesOneCodeDFTemp.loc[:day].sort_values(by=u'EndDate').iloc[-1].values
#        dataValuesOneCodeDF.loc[day] = dataValuesOneCodeArrTemp.reshape(len(dataValuesOneCodeArrTemp,))
#    dataValuesUseDic[code] = dataValuesOneCodeDF
    



# tol code used : dataTolComCode        
#set(dataComCode) - set(dataTolComCode)       code not contained:155

   
# save netprofit as 3D array   , total codes
itemNames = [u'AFloats', u'EndDate']
dataValuesArr = np.zeros((len(itemNames), len(dataTSArr), len(dataComCodeArr)))

dataValuesDF = pd.DataFrame([], index=dataTSArr, columns=dataComCodeArr)
dataValuesEndDateDF = pd.DataFrame([], index=dataTSArr, columns=dataComCodeArr)
for code in dataComCodeUse:
    dataValuesDF[code] = dataValuesUseDic[code][itemNames[0]]
    dataValuesEndDateDF[code] = dataValuesUseDic[code][itemNames[1]]
#
## save as pkl

#dicAFloatsPkl = {u'AFloats': dataValuesDF, u'EndDate': dataValuesEndDateDF}
#cp.dump(dicAFloatsPkl, open("/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_AFloats_2items_dic.pkl", "w")) 


    
# save AFloats in 3D array       
dataValuesArr[0] = dataValuesDF.values      # AFloats values
dataValuesArr[1] = dataValuesEndDateDF.values    # AFloats end date


itemNamesArr = np.zeros((1, len(itemNames)), dtype=object)
for i, j in enumerate(itemNames):
    itemNamesArr[0][i] = np.array([j])

dataDic = {'axis1_itemNames': itemNamesArr, \
           'axis2_indexTime': dataTSArr.reshape(len(dataTSArr), 1), \
           'axis3_colCompanyCode': dataComCodeArr, \
           'LC_AFloats': dataValuesArr}
           
sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_AFloats_arr.mat', dataDic)
                       
















