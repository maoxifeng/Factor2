# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 10:28:43 2017

@author: liusl
"""

import numpy as np
import pandas as pd
import scipy.io as sio
import Common.SmaFun as cs

def codeDFGet(use=True): 
    pathCode = '/data/liushuanglong/MyFiles/Data/Common/astock.mat'
    dataDF = cs.SheetToDFGet(pathCode).set_index('InnerCode', drop=False)    
    ordInnerCode = sio.loadmat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/ordInnerCode.mat')['ordInnerCode'][0]
    ordCodeDF = dataDF.reindex(ordInnerCode)
    ordCodeDF.reset_index(drop=True, inplace=True)        
    if use:        
        ordCodeDF = ordCodeDF.iloc[:, [0, 1, 2, 4]]
    return ordCodeDF
    

def dateSerArrGet():
    path = '/data/liushuanglong/MyFiles/Data/Common/alltdays.mat'
    dataRawDF = cs.SheetToDFGet(path)
    dsArr = dataRawDF.values.astype(float)[:, 0]
    DSArr = np.zeros((len(dsArr), 4))
    DSArr[:, 0]= dsArr
    DSArr[:, 1]= np.floor(dsArr/100)
    for imon in np.unique(DSArr[:, 1]):
        useInd = np.where(DSArr[:, 1]==imon)[0]
        DSArr[useInd[0], 2] = 1
        DSArr[useInd[-1], 3] = 1
    return DSArr
    
def codeIndexDFGet(codeStr='HS300', saveBool=False):
    
    '''formative sheet, values are 0 or 1 '''
    # depend on the order of the code, the same order with the code
    codeDic={'HS300': 3145, 'ZZ800': 4982}
    codeInt = codeDic[codeStr]
    pathInd = '/data/liushuanglong/MyFiles/Data/JYDB2/LC_IndexComponent/idxcomponent.mat'
    dataRawDF = cs.SheetToDFGet(pathInd)
    
    dataColUseLis = [u'IndexInnerCode', u'SecuInnerCode', u'InDate', u'OutDate']
    dataUseArr = dataRawDF[dataColUseLis].values.astype(float)
    dataIndArr = dataUseArr[dataUseArr[:, 0]==codeInt]
    
    dataIndArr[dataIndArr[:, 3]==1010101.0, 3] = 90000000.0
        
    dataDSArr = dateSerArrGet()[:, 0]
    
    dataInnerCodeArr = codeDFGet().iloc[:, 0].values.astype(float)   # default value is 0
    
    # formative index array
    # 
    forIndexArr = np.zeros((len(dataDSArr), len(dataInnerCodeArr)))
    dataInnerCodeUseArr = np.unique(dataIndArr[:, 1])  #  use codes belong to index sheet 
    for iicode, icode in enumerate(dataInnerCodeUseArr):
        arrTemp = dataIndArr[dataIndArr[:, 1]==icode, 2:]   # select one code indate, outdate data
        for ilen in range(len(arrTemp)):          #  
            useBool = (dataDSArr>=arrTemp[ilen, 0]) & (dataDSArr<arrTemp[ilen, 1])
            forIndexArr[useBool, dataInnerCodeArr==icode] = 1     #  if the code is in the pool, the value is 1
            
    if saveBool:            
        arrName = codeStr + '_IndexCode'
        dataDic={'colInnerCode': dataInnerCodeArr, 
                 'indDate': dataDSArr.reshape(len(dataDSArr), 1),
                 arrName: forIndexArr, \
                 'arrKey': [arrName, 'indDate', 'colNames']}
        
        savePath ='/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/'
        saveName = savePath + '/' + arrName + '_array.mat'
        sio.savemat(saveName, dataDic)
        print 'file saved ~'                    
    forIndexDF = pd.DataFrame(forIndexArr, index=dataDSArr, columns=dataInnerCodeArr)                
    return forIndexDF
    

    
    

    