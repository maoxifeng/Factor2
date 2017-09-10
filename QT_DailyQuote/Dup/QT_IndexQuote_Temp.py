#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 16:03:38 2017

@author: liushuanglong
"""

import numpy as np
import scipy.io as sio
import pandas as pd
import h5py
import cPickle as cp

path= '/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2009_mat.mat'
  
dataRaw_IQ_2009 = sio.loadmat(path)  

#dic1 = {'__globals__': [], '__header__': 'MATLAB 5.0 MAT-file, Platform: GLNXA64,\
#        Created on: Thu Jul 20 16:00:24 2017', '__version__': '1.0'}


dataCol = [dataRaw_IQ_2009['col'][0][i][0] for i in range(dataRaw_IQ_2009['col'].shape[1])]
#dataCol = [str(i) for i in dataCol]
#dataColArr = np.array(dataCol)


#dataInd = []
#if dataRow_IQ_2009['ind'].size != 0:
#    dataInd = [dataRaw_IQ_2009['ind'][0][i][0] for i in range(dataRaw_IQ_2009['ind'].shape[1])]
#dataIndArr = np.array(dataInd)

colArr = dataRaw_IQ_2009['col']
colArr0 = colArr[0]
colArr00 = colArr0[0]


arr1 = np.zeros((1, 3))

colArrTest = np.zeros((1, 13), dtype=object)
for i, j in enumerate(dataCol):
    colArrTest[0][i] = np.array([j])

dataDic = {'colArrTest': colArrTest, 'dataArr': dataArr}
sio.savemat('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/test4.mat', dataDic)

dataRaw_IQ_2009_Test = sio.loadmat('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/test4.mat')  

#fs = h5py.File('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/test4.h5','w')
#fs.create_dataset('dataArr', data = dataArr)
#fs.create_dataset('dataCol', data =  [str(i) for i in dataCol])
#fs.close()
#
#fr = h5py.File('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/test4.h5','r')

#f2s = h5py.File('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/test_col.h5','w')
#f2s.create_dataset('dataCol', data = np.array(dataCol))
#f2s.close()





dataArr = dataRaw_IQ_2009['data']

dataDF_all = pd.DataFrame(dataArr, columns = dataCol)

col_use = [dataCol[i] for i in [0, 3, 5, 9]]
dataDF = dataDF_all[col_use]

#d1 = dataDF[u'TradingDay'].head(10)
#dataDF.loc[:, u'TradingDay'] = (map(lambda x: int(x), dataDF[u'TradingDay']))
#dataDF.loc[:, u'InnerCode'] = (map(lambda x: int(x), dataDF[u'InnerCode']))

#dataDF.loc[:, u'InnerCode'] = (map(lambda x: str(x), dataDF[u'InnerCode']))
#df = df.sort(columns=['tradeDate', 'secID'], ascending=[False, True])

dataDF_HS300 = dataDF[(dataDF[u'InnerCode']) == 3145]
dataDF_HS300.reset_index(drop = True, inplace = True)

#look for nan values
#dataDF_HS300.isnull().any()
#ataDF_HS300[ataDF_HS300.isnull().values==True]

dataDF_HS300[u'Return'] = dataDF_HS300[u'ClosePrice']/dataDF_HS300[u'PrevClosePrice'] -1
Return_HS300_3145_2009 = dataDF_HS300[[u'TradingDay', u'Return']]


#==============================================================================
# # save files by iPickle

# cp.dump(Return_HS300_3145_2009, open('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Common/MarketReturn/\
#                                      Return_HS300_3145_2009.pkl', 'w'))
# cpData= cp.load(open('/home/liushuanglong/My files/Data/Factors/HLZ/Common/MarketReturn/Return_HS300_3145_2009.pkl', 'r'))
#==============================================================================


#==============================================================================
# # save files by scipy.io
# 
# fs = h5py.File('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Common/MarketReturn/Return_HS300_3145_2009.h5','w')
# #fs.create_dataset('Return_HS300_3145_2009_values', data = Return_HS300_3145_2009)
# fs.create_dataset('Return_HS300_3145_2009_columns', data = Return_HS300_3145_2009.columns.tolist())
# fs.create_dataset('Return_HS300_3145_2009_colum', data =  ['TradingDay', 'Return'])
# #fs.create_dataset('Return_HS300_3145_2009_index', data = Return_HS300_3145_2009.index)
# fs.close()
# 
# fr = h5py.File('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Common/MarketReturn/Return_HS300_3145_2009.h5','r')
# fr.close()
#==============================================================================












