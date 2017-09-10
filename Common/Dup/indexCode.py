# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 15:30:57 2017

@author: liusl
"""

import numpy as np
import scipy.io as sio
import pandas as pd
import time
import Common.TimeCodeGet as tc


dataDSArr = tc.dateSerArrGet()[:, 0]
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)




def codeIndexDFGet(codeStr='HS300', saveBool=False):

    codeDic={'HS300': 3145, 'ZZ800': 4982}
    codeInt = codeDic[codeStr]
    pathInd = '/data/liushuanglong/MyFiles/Data/JYDB2/LC_IndexComponent/idxcomponent.mat'
    dataRaw = sio.loadmat(pathInd)
    dataColTol = [dataRaw['col'][0][i][0] for i in range(dataRaw['col'].shape[1])]
    dataColUseLis = [u'IndexInnerCode', u'SecuInnerCode', u'InDate', u'OutDate']
    dataColIndUseLis = [dataColTol.index(i) for i in dataColUseLis]
    dataUseArr = dataRaw['data'][:, dataColIndUseLis]
    
    dataIndArr = dataUseArr[dataUseArr[:, 0]==codeInt]
    
    dataIndArr[dataIndArr[:, 3]==1010101.0, 3] = 90000000.0
    
    # formative index array
    forIndexArr = np.zeros((len(dataDSArr), len(dataInnerCodeArr)))
    dataInnerCodeUseArr = np.unique(dataIndArr[:, 1])
    for iicode, icode in enumerate(dataInnerCodeUseArr):
        arrTemp = dataIndArr[dataIndArr[:, 1]==icode, 2:]
        for ilen in range(len(arrTemp)):
            useBool = (dataDSArr>=arrTemp[ilen, 0]) & (dataDSArr<arrTemp[ilen, 1])
            forIndexArr[useBool, dataInnerCodeArr==icode] = 1     
            
    if saveBool:            
        arrName = codeStr + '_IndexCode'
        dataDic={'colInnerCode': dataComCodeArr, 
                 'indDate': dataDSArr.reshape(len(dataDSArr), 1),
                 arrName: forIndexArr, \
                 'arrKey': [arrName, 'indDate', 'colNames']}
        
        savePath ='/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/'
        saveName = savePath + '/' + arrName + '_array.mat'
        sio.savemat(saveName, dataDic)
        print 'file saved ~'                    
    return forIndexArr
    
    
#HS300CodeDic = codeIndexDFGet(saveBool=True)
    
#HS300Arr = HS300CodeDic[HS300CodeDic['arrKey'][0]]
#
#HS300Counts = np.sum(HS300Arr, axis=1)
#
#aa = np.where((HS300Counts!=0) & (HS300Counts!=300))
#
#dataDSArr[aa]
#HS300Counts



for300DF = pd.DataFrame(forIndexArr, index=dataDSArr, columns=dataInnerCodeArr)

for300DF[for300DF==0] = np.nan
for300UseDF = for300DF.dropna(how='all')

dd, cc = tc.codeIndexDFGet()

dd[dd==0] = np.nan
dd1 = dd.dropna(how='all')
ee = dd1.sum(axis=1)

ff = ee[ee!=300]






