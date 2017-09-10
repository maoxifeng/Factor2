# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 16:21:31 2017

@author: liusl
"""


'''
#==============================================================================
# fetch index daily data
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
    

def IndexLogReturnGet(mar='HS300', Free=False, savePath='/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/'):
    indexDataDF = IndexQuoteGet(mar=mar, saveBool=False)
    IndexLogReturnDF = np.log(indexDataDF[u'ClosePrice']) - np.log(indexDataDF[u'PrevClosePrice'])
    IndexLogReturnArr = IndexLogReturnDF.values.astype(float).reshape(len(IndexLogReturnDF), 1)
    if Free:
            pathFreeRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Wind_Daily10YearBond_LogReturn_array.mat'
            dataFreeRetArr = sio.loadmat(pathFreeRet)['TenYearBond_LogReturn']
            IndexLogReturnArr = IndexLogReturnArr - dataFreeRetArr
            mar = mar + 'Free'            
            
    arrName = 'IndexQuote_' + mar + '_LogReturn'
    dataDic = {'colNames': np.array([u'LogReturn'], dtype=object), \
               'indexDate': dataDSArr.reshape(len(dataDSArr), 1), \
               arrName: IndexLogReturnArr, 
               'arrKey':[arrName, 'indexDate', 'colNames']}
    fileSavePathName = savePath + '/' + arrName + '_arr.mat'
    sio.savemat(fileSavePathName, dataDic)
    print arrName + '_arr.mat', 'saved'
    return IndexLogReturnArr
    
    
    
    


#HS300Close = IndexQuoteGet(mar='HS300', items=[u'PrevClosePrice', u'ClosePrice'])    
#    
#HS300LogReturnArr = IndexLogReturnGet()
#HS300_FreeLogReturnArr = IndexLogReturnGet(Free=True)


