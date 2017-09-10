# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 10:26:16 2017

@author: liusl
"""


import numpy as np
import scipy.io as sio
import pandas as pd
import os

def SheetToDFGet(path):
    dataRaw = sio.loadmat(path)
    dataSt = dataRaw['dataStruct'][0, 0]
    col = dataSt.dtype.names
    dataArr = np.hstack(dataSt)
    dataDF = pd.DataFrame(dataArr, columns=col)
    return dataDF

def ForArrToDFGet(path):
    dataRawDic = sio.loadmat(path)
    arrKey = dataRawDic['arrKey']
    arrKey = [key.split()[0] for key in arrKey]
    dataDSAllArr = dataRawDic[arrKey[1]][:, 0]
    dataInnerCodeAllArr = dataRawDic[arrKey[2]][0]
    dataAllArr = dataRawDic[arrKey[0]]
    dataAllDF = pd.DataFrame(dataAllArr, index=dataDSAllArr, 
                             columns=dataInnerCodeAllArr)
    return dataAllDF
    
    
def AllArrToDFGet(path):
    '''depend on the file name which has digits'''
    fileNameLis = os.listdir(path)
    fileNameDic = {float(filter(str.isdigit, ifile)): ifile for ifile in fileNameLis}
    fileYearLis = sorted(fileNameDic.keys())    
    dfLis = []
    for ifileYear in fileYearLis:
        ifilePath = path + '/' + fileNameDic[ifileYear]
        dfTemp = ForArrToDFGet(ifilePath)
        dfLis = dfLis + [dfTemp]
        if ifileYear == fileYearLis[-1]:
            dataInnerCode = dfTemp.columns
    
    dataDF = pd.concat(dfLis)
    dataDF = dataDF.reindex(columns=dataInnerCode)
    dataDF = dataDF.sort_index()
    return dataDF

    
def ItemArrToDFGet(path):
    dataRawDic = sio.loadmat(path)
    arrKey = dataRawDic['arrKey']
    arrKey = [key.split()[0] for key in arrKey]
    dataDSAllArr = dataRawDic[arrKey[1]][:, 0]
    dataItemsLis = [i[0] for i in dataRawDic[arrKey[2]][0]]
    dataAllArr = dataRawDic[arrKey[0]]
    dataAllDF = pd.DataFrame(dataAllArr, index=dataDSAllArr, 
                             columns=dataItemsLis)
                             
    return dataAllDF
    
    
def ItemAllArrToDFGet(path):
    fileNameLis = os.listdir(path)
    fileNameDic = {float(filter(str.isdigit, ifile)): ifile for ifile in fileNameLis}
    fileYearLis = sorted(fileNameDic.keys())    
    dfLis = []
    for ifileYear in fileYearLis:
        ifilePath = path + '/' + fileNameDic[ifileYear]
        dfTemp = ItemArrToDFGet(ifilePath)
        dfLis = dfLis + [dfTemp]
    dataDF = pd.concat(dfLis)
    dataDF = dataDF.sort_index()
    return dataDF
    

def nonNanFirIndGet(arr):
    
    '''return the index of the first non nan row of the load array'''
    for i in xrange(len(arr)):
        if len(arr[i][~np.isnan(arr[i])]) > 0:
            break
    return i

