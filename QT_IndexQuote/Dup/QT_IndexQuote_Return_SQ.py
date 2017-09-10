#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:16:18 2017

@author: liushuanglong
"""

import numpy as np
import scipy.io as sio
import pandas as pd


# function
def MarketReturn(path):
    dataRaw = sio.loadmat(path)  
    dataColTol = [dataRaw['col'][0][i][0] for i in range(dataRaw['col'].shape[1])]
    dataCol = [dataColTol[i] for i in [0, 3, 5, 9]]
    dataArr = dataRaw['data'][:, [0, 3, 5, 9]]
    dataDF = pd.DataFrame(dataArr, columns=dataCol)
    dataDF_HS300 = dataDF[(dataDF[u'InnerCode']) == 3145]  # select HS300 data
    dataDF_HS300.reset_index(drop = True, inplace = True)
    
    print dataDF_HS300[dataDF_HS300.isnull().values].drop_duplicates()
    
    if dataDF_HS300[dataDF_HS300.isnull().values].size != 0:  # fillna

        dataDF_HS300.fillna(method='ffill', inplace=True)
        dataDF_HS300.fillna(method='bfill', inplace=True)
    
    dataDF_HS300[u'Return'] = dataDF_HS300[u'ClosePrice']/dataDF_HS300[u'PrevClosePrice'] -1
    dataReturn_HS300= dataDF_HS300[[u'TradingDay', u'Return']]
    return dataReturn_HS300


Return_HS300_3145_2009 = MarketReturn('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2009_mat.mat')
Return_HS300_3145_2012 = MarketReturn('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2012_mat.mat')
Return_HS300_3145_2014 = MarketReturn('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2014_mat.mat')
Return_HS300_3145_2016 = MarketReturn('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2016_mat.mat')
Return_HS300_3145_3000 = MarketReturn('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_3000_mat.mat')

Return_HS300_3145_2009_to_3000 = pd.concat([Return_HS300_3145_2009, Return_HS300_3145_2012, \
                                            Return_HS300_3145_2014, Return_HS300_3145_2016, \
                                            Return_HS300_3145_3000], ignore_index=True)

Return_HS300_3145_2009_to_3000[u'Return_SQ'] = Return_HS300_3145_2009_to_3000[u'Return']**2
Return_SQ_HS300_3145_2009_to_3000 = Return_HS300_3145_2009_to_3000[[u'TradingDay', u'Return_SQ']]

colLis = Return_SQ_HS300_3145_2009_to_3000.columns.tolist()
colArr = np.zeros((1, len(colLis)), dtype=object)
for i, j in enumerate(colLis):
    colArr[0][i] = np.array([j])

dataDic = {'colNames': colArr, \
           'indexTime': Return_SQ_HS300_3145_2009_to_3000[colLis[0]].values.reshape(len(Return_SQ_HS300_3145_2009_to_3000[colLis[0]].values), 1), \
           'Return_SQ_HS300_3145_2005_to_3000': Return_SQ_HS300_3145_2009_to_3000[colLis[1:]].values}
sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Financial/Return_SQ_HS300_3145_2005_to_3000_array.mat', dataDic)
    
    

    












