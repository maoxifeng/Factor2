#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 14:10:07 2017

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
    dataDF_Use = dataDF[(dataDF[u'InnerCode']) == 66456]  # select HS300 data
    dataDF_Use.reset_index(drop = True, inplace = True)
    
    print dataDF_Use[dataDF_Use.isnull().values].drop_duplicates()
    
    if dataDF_Use[dataDF_Use.isnull().values].size != 0:  # fillna

        dataDF_Use.fillna(method='ffill', inplace=True)
        dataDF_Use.fillna(method='bfill', inplace=True)
    
    dataDF_Use[u'Return'] = dataDF_Use[u'ClosePrice']/dataDF_Use[u'PrevClosePrice'] -1
    dataReturn_Use= dataDF_Use[[u'TradingDay', u'Return']]
    return dataReturn_Use


Return_50ETF_66456_2009 = MarketReturn('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2009_mat.mat')
Return_50ETF_66456_2012 = MarketReturn('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2012_mat.mat')
Return_50ETF_66456_2014 = MarketReturn('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2014_mat.mat')
Return_50ETF_66456_2016 = MarketReturn('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2016_mat.mat')
Return_50ETF_66456_3000 = MarketReturn('/home/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_3000_mat.mat')

Return_50ETF_66456_2015_to_3000 = pd.concat([Return_50ETF_66456_2009, Return_50ETF_66456_2012, \
                                            Return_50ETF_66456_2014, Return_50ETF_66456_2016, \
                                            Return_50ETF_66456_3000], ignore_index=True)


colLis = Return_50ETF_66456_2015_to_3000.columns.tolist()
colArr = np.zeros((1, len(colLis)), dtype=object)
for i, j in enumerate(colLis):
    colArr[0][i] = np.array([j])

dataDic = {'colNames': colArr, \
           'indexTime': Return_50ETF_66456_2015_to_3000[colLis[0]].values.reshape(len(Return_50ETF_66456_2015_to_3000[colLis[0]].values), 1), \
           'Return_50ETF_66456_2015_to_3000': Return_50ETF_66456_2015_to_3000[colLis[1:]].values}
sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Financial/Return_50ETF_66456_2015_to_3000_array.mat', dataDic)
    
    
# calculate market return squared
   
    












