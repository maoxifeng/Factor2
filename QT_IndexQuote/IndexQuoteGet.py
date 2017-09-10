# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 12:59:28 2017

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
import Common.SmaFun as cs
import os
import Common.UpdateDataGet as cu

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
             
def IndexQuoteGet(mar='HS300', facName='ClosePrice', items=[u'PrevClosePrice', u'ClosePrice']):
    
    '''save file'''
    pathQTDaily = '/data/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/'
    savePathMain = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/'
    indexSavePath = savePathMain + mar + '/'
    if not os.path.exists(indexSavePath):
        os.mkdir(indexSavePath)
    facName = mar + '_' + facName    
    facSavePath = indexSavePath + facName + '/'
    if not os.path.exists(facSavePath):
        os.mkdir(facSavePath)
    
    
    fileLis = os.listdir(pathQTDaily)   
    dailyLis = []
    codeDic={'HS300': 3145, 'ZZ800': 4982}
    for ifileName in fileLis:   
        ifilePath = pathQTDaily + ifileName
        dataRaw = cs.SheetToDFGet(ifilePath)     
        dataCol = [u'TradingDay', u'InnerCode'] + items
        dataDFTol = dataRaw[dataCol]
        
        dataDFUse = dataDFTol[dataDFTol[u'InnerCode']==codeDic[mar]]
        dataDFUseSort = dataDFUse.sort_values(by=u'TradingDay')
        dataDFUseSort = dataDFUseSort.drop([u'InnerCode'], axis=1)
        dataIndexDF = dataDFUseSort.set_index('TradingDay')
        
        dailyLis = dailyLis + [dataIndexDF]
    
    
    dataItemAllDF = pd.concat(dailyLis)
    dataItemAllSortDF = dataItemAllDF.sort_index()
        
    dataItemAllUse = dataItemAllSortDF[~dataItemAllSortDF.index.duplicated()]
    
    dataItemAllUseDF = dataItemAllUse.loc[dataDSArr]   # 
    cu.UpdateItemDataGet(dataItemAllUseDF,  facSavePath, facName)        
    
    return None
    

def IndexLogReturnGet(mar='HS300'):
    dicPath = {'HS300': '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/HS300/HS300_ClosePrice'}
    closePath = dicPath[mar]
    indexPath = os.path.split(closePath)[0]
        
    facName = mar + '_Return'
    savePath = indexPath + '/' + facName + '/'
    if not os.path.exists(savePath):
        os.mkdir(savePath)
    
    indexDataDF = cs.ItemAllArrToDFGet(closePath)
    IndexLogReturnDF = pd.DataFrame(index=indexDataDF.index, columns=[facName])
    IndexLogReturnDF.iloc[:, 0] = np.log(indexDataDF[u'ClosePrice']) - np.log(indexDataDF[u'PrevClosePrice'])
#    if Free:
#            pathFreeRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Wind_Daily10YearBond_LogReturn_array.mat'
#            dataFreeRetArr = sio.loadmat(pathFreeRet)['TenYearBond_LogReturn']
#            IndexLogReturnArr = IndexLogReturnArr - dataFreeRetArr
#            mar = mar + 'Free'            
    cu.UpdateItemDataGet(IndexLogReturnDF, savePath, facName)
    return None
    


    
def BondReturnGet():
    '''from wind 10 years bond '''
    savePathMain = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/'
    facName = 'BondReturn'
    facSavePath = savePathMain + facName + '/'

    if not os.path.exists(facSavePath):
        os.mkdir(facSavePath)
        
    path = '/data/liushuanglong/MyFiles/Data/Common/bond_10y.mat'
    dataRawDF = cs.SheetToDFGet(path)
    dataDF = dataRawDF.set_index('date')
    dataDSArr = tc.dateSerArrGet()[:, 0]
    dataDF = dataDF.reindex(dataDSArr)
    dataPrice = dataDF.values.astype(float)
    dataReturn = pd.DataFrame(index=dataDSArr, columns=['Return'])
    dataReturn.iloc[1:] = np.log(dataPrice[1:]) - np.log(dataPrice[:-1])  # log return
    
    cu.UpdateItemDataGet(dataReturn, facSavePath, facName)        
    return None
    
    
    




  