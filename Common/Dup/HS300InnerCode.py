#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 19:49:28 2017

@author: liushuanglong
"""


import numpy as np
import scipy.io as sio
import pandas as pd


# load index component sheet
pathHS300 = '/home/liushuanglong/MyFiles/Data/JYDB2/LC_IndexComponent/idxcomponent_mat.mat'
dataRaw = sio.loadmat(pathHS300)
dataColTol = [dataRaw['col'][0][i][0] for i in range(dataRaw['col'].shape[1])]
dataColUseLis = [u'IndexInnerCode', u'SecuInnerCode', u'Flag', u'SecuMarket', u'OutDate']
dataColIndUseLis = [dataColTol.index(i) for i in dataColUseLis]
dataUseArr = dataRaw['data'][:, dataColIndUseLis]

dataIndexDF = pd.DataFrame(dataUseArr, columns=dataColUseLis)

boolArr = (dataIndexDF[u'IndexInnerCode'] == 3145) & (dataIndexDF[u'Flag'] == 1)
bool2Arr = (dataIndexDF[u'IndexInnerCode'] == 3145) & (dataIndexDF[u'Flag'] == 1) & (dataIndexDF[u'OutDate'] != 1010101)

dataHS300DF =  dataIndexDF[boolArr]

# HS300 stock inner code 
dataHS300InnerCodeArr = np.unique(dataHS300DF[u'SecuInnerCode'])
#len(dataHS300InnerCodeArr)
#dataHS300InnerCodeArr.shape

# load total stock code
pathCode = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
dataCodeRaw = sio.loadmat(pathCode)
dataCodeArr = dataCodeRaw['data']
dataCodeRaw.keys()

dataCodeColTol = [dataCodeRaw['col'][0][i][0] for i in range(dataCodeRaw['col'].shape[1])]

dataCodeDF = pd.DataFrame(dataCodeArr, columns=dataCodeColTol)
dataHS300CodeDF = dataCodeDF[dataCodeDF[dataCodeColTol[0]].isin(dataHS300InnerCodeArr)]
dataHS300CodeDF['CodeIndex'] = dataHS300CodeDF.index.tolist()
#dataHS300CodeDF.shape



colLis = dataHS300CodeDF.columns.tolist()
colArr = np.zeros((1, len(colLis)), dtype=object)
for i, j in enumerate(colLis):
    colArr[0][i] = np.array([j])
dataDic = {'col': colArr, 'data': dataHS300CodeDF.values}

sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/HS300StockCode_arr.mat', dataDic)


