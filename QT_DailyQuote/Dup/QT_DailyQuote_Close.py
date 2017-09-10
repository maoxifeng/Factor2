#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 08:51:35 2017

@author: liushuanglong
"""

'''
#==============================================================================
# fetch close data
#==============================================================================
'''

import numpy as np
import scipy.io as sio
import pandas as pd
import Common.TimeCodeGet as tc


# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)

dataCloseTemp = pd.DataFrame([], columns=dataInnerCodeArr)

def dataCloseYear(path):   
    
    dataRaw = sio.loadmat(path)     
    dataColTol = [dataRaw['col'][0][i][0] for i in range(dataRaw['col'].shape[1])]
    useLis = [dataColTol.index(i) for i in [u'TradingDay', u'InnerCode', u'ClosePrice']]
    dataCol = [dataColTol[i] for i in useLis]
    dataArr = dataRaw['data'][:, useLis]
    
    dataDFTol = pd.DataFrame(dataArr, columns=dataCol)
    
    dataDFUse = dataDFTol[dataDFTol[u'InnerCode'].isin(dataInnerCodeArr)]
    
    dataDFUseSort = dataDFUse.sort_values(by=u'TradingDay')
    dataDFUseSort.set_index([u'TradingDay', u'InnerCode'], inplace=True)
    
    dataDF = dataDFUseSort[u'ClosePrice'].unstack()
    
    return dataDF


dataClose_1999 = dataCloseYear('/data/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_1999.mat')
dataClose_2004 = dataCloseYear('/data/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_2004.mat')
dataClose_2007 = dataCloseYear('/data/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_2007.mat')
dataClose_2011 = dataCloseYear('/data/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_2011.mat')
dataClose_2015 = dataCloseYear('/data/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_2015.mat')
dataClose_2016 = dataCloseYear('/data/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_2016.mat')
dataClose_3000 = dataCloseYear('/data/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_3000.mat')


dataClose = pd.concat([dataCloseTemp, dataClose_1999, dataClose_2004, \
                       dataClose_2007, dataClose_2011, dataClose_2015, \
                       dataClose_2016, dataClose_3000])   # 



dataClose = dataClose.sort_index()
dataCloseUse = dataClose[~dataClose.index.duplicated()]
dataCloseUse = dataCloseUse.reindex(columns = dataInnerCodeArr)

dataCloseUseDF = dataCloseUse.loc[dataDSArr]   # 
dataCloseUseArr = dataCloseUseDF.values.astype(float)

dataDic = {'colInnerCode': dataInnerCodeArr, \
           'indexDate': dataDSArr.reshape(len(dataDSArr), 1), \
           'ClosePrice': dataCloseUseArr}
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_ClosePrice_array.mat', dataDic)




