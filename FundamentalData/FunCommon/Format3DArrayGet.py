# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 12:53:03 2017

@author: liusl
"""

import numpy as np
import scipy.io as sio
import pandas as pd
import time
import Common.TimeCodeGet as tc


# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)

''' single code data to all code, all date formative data dic '''
def FacDicTo3DArrDicGet(dataRawDic, facName='Factor'):
    comCodeLis = dataRawDic.keys()
    itemsLis = dataRawDic[comCodeLis[0]].columns.tolist()  # item order !
    dataFormatDic = {}
    for iitem in itemsLis:
        dataFormatDic[iitem] = pd.DataFrame(index=dataDSArr, columns=dataComCodeArr)        
    
    
    print 'start convert to 3D form array: ',
    print time.strftime("%H:%M:%S", time.localtime())
    print 'code counts', 'code'
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
            
        if iicode%100 == 0:
            print iicode, icode

    data3DArr = np.zeros((len(itemsLis), len(dataDSArr), len(dataComCodeArr)))
    data3DArr[:] = np.nan
    for iiitem, iitem in enumerate(itemsLis):
        arrTemp = dataFormatDic[iitem].values.astype(float)
        data3DArr[iiitem] = arrTemp
        
    arrName = facName + '_3DValues'    
    dataDic = {'axis1Names_Items': np.array(itemsLis, dtype=object),
               'axis2Names_DateSeries': dataDSArr.reshape(len(dataDSArr), 1),\
               'axis3Names_ComCode': dataComCodeArr,\
               arrName: data3DArr, 
               'arrKey': [arrName, 'axis1Names_Items', 'axis2Names_DateSeries', 'axis3Names_ComCode']}
    return dataDic
    
    