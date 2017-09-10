# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 11:15:03 2017

@author: liusl
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



import os

dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)

itemsLis = [u'TradingDay',
             u'XGRQ',
             u'ChangePCT',
             u'ClosePrice',
             u'HighPrice',
             u'InnerCode',
             u'LowPrice',
             u'NegotiableMV',
             u'OpenPrice',
             u'PrevClosePrice',
             u'TurnoverDeals',
             u'TurnoverValue',
             u'TurnoverVolume']
             
def IndexQuoteGet(mar='HS300', items=[u'PrevClosePrice', u'ClosePrice'], saveBool=False):
    
    '''do not save as file, just as a function'''
    pathQTDaily = '/data/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/'
    fileLis = os.listdir(pathQTDaily)   
    dailyLis = []
    codeDic={'HS300': 3145, 'ZZ800': 4982}
    for ifileName in fileLis:   
        ifilePath = pathQTDaily + ifileName
        dataRaw = sio.loadmat(ifilePath)     
        dataColTol = [dataRaw['col'][0][i][0] for i in range(dataRaw['col'].shape[1])]
        dataCol = [u'TradingDay', u'InnerCode'] + items
        useLis = [dataColTol.index(i) for i in dataCol]
        dataArr = dataRaw['data'][:, useLis]
        
        dataDFTol = pd.DataFrame(dataArr, columns=dataCol)
        
        dataDFUse = dataDFTol[dataDFTol[u'InnerCode']==codeDic[mar]]
        
        dataDFUseSort = dataDFUse.sort_values(by=u'TradingDay')
        dataDFUseSort = dataDFUseSort.drop([u'InnerCode'], axis=1)
        dataIndexDF = dataDFUseSort.set_index('TradingDay')
        
        dailyLis = dailyLis + [dataIndexDF]
    
    
    dataItemAllDF = pd.concat(dailyLis)
    dataItemAllSortDF = dataItemAllDF.sort_index()
        
    dataItemAllUse = dataItemAllSortDF[~dataItemAllSortDF.index.duplicated()]
    
    dataItemAllUseDF = dataItemAllUse.loc[dataDSArr]   # 
    dataItemAllUseArr = dataItemAllUseDF.values.astype(float)
    if saveBool:
        savePath='/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/'
        arrName = 'IndexQuote_' + mar
        dataDic = {'colNames': np.array(items, dtype=object), \
                   'indexDate': dataDSArr.reshape(len(dataDSArr), 1), \
                   arrName: dataItemAllUseArr, 
                   'arrKey':[arrName, 'indexDate', 'colNames']}
        fileSavePathName = savePath + '/' + arrName + '_arr.mat'
        sio.savemat(fileSavePathName, dataDic)
        print arrName + '_arr.mat', 'saved'
    return dataItemAllUseDF


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


dataClose = dataClose.sort_index()
dataCloseUse = dataClose[~dataClose.index.duplicated()]
dataCloseUse = dataCloseUse.reindex(columns = dataInnerCodeArr)

dataCloseUseDF = dataCloseUse.loc[dataDSArr]   # 
dataCloseUseArr = dataCloseUseDF.values.astype(float)

dataDic = {'colInnerCode': dataInnerCodeArr, \
           'indexDate': dataDSArr.reshape(len(dataDSArr), 1), \
           'ClosePrice': dataCloseUseArr}
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_ClosePrice_array.mat', dataDic)

