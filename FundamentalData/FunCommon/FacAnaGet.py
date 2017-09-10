# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 10:13:53 2017

@author: liusl
"""



import numpy as np
import scipy.io as sio
import pandas as pd
import os
import time
import statsmodels.api as sm
import matplotlib.pylab as plt
import Common.TimeCodeGet as tc
import Common.SmaFun as sf



# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)

def DivGroRetGet(loadPath, divGroNum=10, divPer='1M', pool='A', facName='Factor', saveBool=False, arrDimIndex=0):
    #==============================================================================
    # 1. load data
    #==============================================================================
    ## load factor exposure data
    dataFactorExpDic = sio.loadmat(loadPath)
    facArrKey = dataFactorExpDic['arrKey'][0]
    dataFactorExpArr = dataFactorExpDic[facArrKey]
    if dataFactorExpArr.ndim == 3 :
        dataFactorExpArr = dataFactorExpArr[arrDimIndex]    
    
    dataFactorExpDF = pd.DataFrame(dataFactorExpArr, index=dataDSArr, columns=dataInnerCodeArr)
    
    ## load stoct daily returns
    pathStoLogRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_array.mat'
    dataStoRetArr = sio.loadmat(pathStoLogRet)['StoLogReturn']
    
    ## load stock daily volumne
    pathVol = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_TurnoverVolume_array.mat'
    dataVolRaw = sio.loadmat(pathVol)
    dataVolArr = dataVolRaw[u'TurnoverVolume']  # columns: inner code
    
    ## load stock AFloats
    pathAF = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/Afloats/LC_AFloats_mat.mat'
    dataAFloatsRaw = sio.loadmat(pathAF)
    dataAFloats3DArr = dataAFloatsRaw['LC_AFloats']
    dataAFloatsArr = dataAFloats3DArr[0]

     # constant
    thrNum = 100
    if pool == 'HS300':
        print 'HS300 pool'
        thrNum = 15
        
        # load HS300 index  0/1 sheet
        dataHS300IndexDF = tc.codeIndexDFGet(codeStr='HS300')
        dataHS300IndexDF[dataHS300IndexDF==0] = np.nan
        dataFactorExpDF = dataHS300IndexDF * dataFactorExpDF
        dataFactorExpArr = dataFactorExpDF.values.astype(float)
        
        dataHS300IndexArr = dataHS300IndexDF.values.astype(float)
        dataStoRetArr = dataStoRetArr * dataHS300IndexArr
        dataVolArr = dataVolArr * dataHS300IndexArr
        dataAFloatsArr = dataAFloatsArr * dataHS300IndexArr
        
    dataVolUseArr = np.zeros((len(dataDSArr), len(dataInnerCodeArr)))
    dataReturnUseArr = np.zeros((len(dataDSArr), len(dataInnerCodeArr)))
    dataAFloatsUseArr = np.zeros((len(dataDSArr), len(dataInnerCodeArr)))
    dataReturnUseArr[:] = np.nan
    dataVolUseArr[:] = np.nan
    dataAFloatsUseArr[:] = np.nan
    
    #bool1Arr = np.where((~np.isnan(dataVolArr[1])) & (dataVolArr[1]!=0))
    for i in range(len(dataDSArr)):
        posUseArr = np.where((~np.isnan(dataVolArr[i])) & (dataVolArr[i]!=0))[0]
        if len(posUseArr) == 0:
            continue
        dataVolUseArr[i][posUseArr] = dataVolArr[i][posUseArr]
        dataReturnUseArr[i][posUseArr] = dataStoRetArr[i][posUseArr]
        dataAFloatsUseArr[i][posUseArr] = dataAFloatsArr[i][posUseArr]
    
    dataStoRetDF = pd.DataFrame(dataReturnUseArr, index=dataDSArr, columns=dataInnerCodeArr)
    dataAFloatsDF = pd.DataFrame(dataAFloatsUseArr, index=dataDSArr, columns=dataInnerCodeArr)
    #==============================================================================
    # 2. seperate groups and calculate groups returns
    #==============================================================================
    colNames = ['group'+str(i+1) for i in range(divGroNum)]
    dataFacGroReturnDF = pd.DataFrame(index=dataDSArr, columns=colNames)
    
    staInd = sf.nonNanFirIndGet(dataFactorExpArr)
    
    dataDSAllEffArr = tc.dateSerArrGet()[staInd:]
    monEndDateArr = dataDSAllEffArr[dataDSAllEffArr[:, 3]==1, 0]
    
    print 'start divide', str(divGroNum) + 'groups:', time.strftime("%H:%M:%S", time.localtime())
    percentNumAllArr = np.linspace(0, 1, divGroNum+1)
    for iimonendDate, imonendDate in enumerate(monEndDateArr[:-1]):
        dataFactorMonUseTemp = dataFactorExpDF.loc[imonendDate]
        if len(dataFactorMonUseTemp.dropna()) >= thrNum:  # keep stocks groups when counts >=100
            perFactorExpArr = np.zeros_like(percentNumAllArr)            
            perFactorExpArr[-1] = dataFactorMonUseTemp.max()
            perFactorExpArr[0] = dataFactorMonUseTemp.min()
            perFactorExpArr[1:-1] = dataFactorMonUseTemp.quantile(percentNumAllArr[1:-1]).values
            dsTemp = dataDSArr[(dataDSArr>monEndDateArr[iimonendDate]) & (dataDSArr<=monEndDateArr[iimonendDate+1])]
#            print dsTemp
            for iigro in range(divGroNum):
                igroupLis = dataFactorMonUseTemp[(dataFactorMonUseTemp>perFactorExpArr[iigro])\
                                                & (dataFactorMonUseTemp<=perFactorExpArr[iigro+1])].index.tolist()
                for iidate, idate in enumerate(dsTemp):
                    dataOGTemDF = pd.DataFrame(index=igroupLis, columns=['return', 'aFloats', 'weight', 'wReturn'])
                    dataOGTemDF['return'] = dataStoRetDF.loc[idate][igroupLis]
                    dataOGTemDF['aFloats'] = dataAFloatsDF.loc[idate][igroupLis]
                    dataOGTemDF['weight'] = dataOGTemDF['aFloats'] / dataOGTemDF['aFloats'].sum()
                    dataOGTemDF['wReturn'] = dataOGTemDF['return'] * dataOGTemDF['weight']				
                    dataFacGroReturnDF.loc[idate].iloc[iigro] = dataOGTemDF['wReturn'].sum()
            print imonendDate, 'Done' , time.strftime("%H:%M:%S", time.localtime())
    dataFacGroReturnArr = dataFacGroReturnDF.values.astype(float)
    arrName = facName + '_' + pool + '_' + str(divGroNum) + 'Groups' + 'Return'
    dataDic={'colNames': np.array(colNames, dtype=object), 
             'indDate': dataDSArr.reshape(len(dataDSArr), 1),
             arrName: dataFacGroReturnArr, \
             'arrKey': [arrName, 'indDate', 'colNames']}
             
    if saveBool :
        savePath = os.path.split(loadPath)[0]
        saveName = savePath + '/' + arrName + '_arr.mat'
        sio.savemat(saveName, dataDic)
        print arrName + '_array.mat', 'saved ~'
    
    return dataFacGroReturnArr
                

def DivGroExcRetGraphGet(loadArr=None, loadPath=None, facName_Pool='Factor'):
    
    corUseLis = ['lightcoral', 'red', 'gold', 'lawngreen',\
                'darkgreen', 'aquamarine', 'dodgerblue', 'blue', 'mediumorchid', 'fuchsia', 'pink']
    if loadArr is not None:
        dataRetRawArr = loadArr
    else:
        dataRawDic = sio.loadmat(loadPath)
        facArrKey = dataRawDic['arrKey'][0]
        dataRetRawArr = dataRawDic[facArrKey]
        
    pathMar = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/IndexQuote_HS300_LogReturn_arr.mat'
    dataMarRetRaw = sio.loadmat(pathMar)
    dataMarRetArr = dataMarRetRaw[dataMarRetRaw['arrKey'][0]]
    
    
    dataRetArr = dataRetRawArr.copy()   
    startGroInd = sf.nonNanFirIndGet(dataRetArr)
    startMarInd = sf.nonNanFirIndGet(dataMarRetArr)
    startInd = max(startGroInd, startMarInd)
    dataRetArr[:startInd] = 0
    dataRetCumArr = np.cumsum(dataRetArr, axis=0)
    dataRetCumArr[:startInd] = np.nan
    dataMarRetArr[:startInd] = 0
    dataMarRetCumArr = np.cumsum(dataMarRetArr, axis=0)
    dataMarRetCumArr[:startInd] = np.nan
    #re2 = np.corrcoef(bb, cc)

    groNums = dataRetCumArr.shape[1]
    dataRetCumArr = dataRetCumArr - dataMarRetCumArr
    fig = plt.figure(figsize=(15, 10))
    ax1 = fig.add_subplot(211)
    for i in range(groNums):
        ax1.plot(range(len(dataDSArr)), dataRetCumArr[:, i], color=corUseLis[i], lw=1.5, label='Group'+str(i+1))   
        
    ax1.set_xlim(startInd-250, len(dataDSArr)+400)
    
#    ax1.set_ylim(-0.5, 2.5 )
    ax1.set_xticks(range(startInd, len(dataDSArr), 250))
    ax1.set_xticklabels([dataDSArr[i] for i in ax1.get_xticks()], rotation=30, fontsize='small')
    #ax1.set_yticks(range(-0.3, 1.8, 0.2))
    ax1.set_yticklabels([str((int(i*100)))+'%' for i in ax1.get_yticks()])
    titleName = facName_Pool + '_' + str(groNums) + 'Groups_ExcessReturn'
    ax1.set_title(titleName)
    #ax1.set_xlabel('Date')
    ax1.set_ylabel('Cumulative_ExcessReturn')
    ax1.legend(loc=1, fontsize='small')
    
    ax2 = fig.add_subplot(212)
    ax2.bar((np.arange(1, groNums+1)), dataRetCumArr[-1], width=0.8,  align="center", color=corUseLis)
    ax2.set_xlim(0, 12)
    ax2.set_xticks(np.arange(1, groNums+1))
    ax2.set_xticklabels(['Group'+str(int(i)) for i in ax2.get_xticks()])
    ax2.set_yticklabels([str((int(i*100)))+'%' for i in ax2.get_yticks()])
    ax2.set_ylabel('Cumulative_ExcessReturn')
#    ax2.legend(loc=1)
    if loadPath is not None:        
        savePath = os.path.split(loadPath)[0]
        saveName = savePath + '/' + titleName + '.png'
        plt.savefig(saveName, dpi=400)    
        print titleName + '.png saved~'
    return dataRetCumArr
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    