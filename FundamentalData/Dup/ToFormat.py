# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 16:26:31 2017

@author: liusl
"""

import numpy as np
import scipy.io as sio
import pandas as pd
import time
import Common.TimeCodeGet as tc
import FundamentalData.IA.IADicGet as idg

# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)


''' single code data to all code, all date formative data dic '''
def FunFacToFormatGet(dataRawDic):    
    comCodeLis = dataRawDic.keys()
    itemsLis = dataRawDic[comCodeLis[0]].columns.tolist()
    dataFormatDic = {}
    for iitem in itemsLis:
        dataFormatDic[iitem] = pd.DataFrame(index=dataDSArr, columns=dataComCodeArr)        
    
    for iicode, icode in enumerate(comCodeLis):
        if dataRawDic[icode].size==0:
            continue        
        pubDateLis = dataRawDic[icode].index.tolist()
        pubDateLis.extend(list(dataDSArr))
        allDateArr = np.unique(pubDateLis)
        # famative date process
        icodeDF = dataRawDic[icode].reindex(index=allDateArr, method='ffill')
        icodeDefDF = icodeDF.loc[dataDSArr]
        for iitem in icodeDefDF.columns:
            dataFormatDic[iitem][icode] = icodeDefDF[iitem]
            
        if  (iicode+1)%100 == 0:
            print time.strftime("%H:%M:%S", time.localtime()),   
            print iicode, icode
                
    return dataFormatDic
        
        
def DefDicTo3DArrDicGet(formatDic, path='', fileName=''):
    items = formatDic.keys()
    data3DArr = np.zeros((len(items), len(dataDSArr), len(dataComCodeArr)))
    data3DArr[:] = np.nan
    for iiitem, iitem in enumerate(items):
        arrTemp = formatDic[iitem].values.astype(float)
        data3DArr[iiitem] = arrTemp
    dataDic = {'axis1Names_Items': np.array(items, dtype=object),
               'axis2Names_DateSeries': dataDSArr.reshape(len(dataDSArr), 1),\
               'axis3Names_ComCode': dataComCodeArr,\
               'ThreeDArray': data3DArr, \
               'DataKey': 'ThreeDArray'}
               
    if path != '':
        pathPlusName = path + fileName
        sio.savemat(pathPlusName, dataDic)
    return dataDic
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


        