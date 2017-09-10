# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 16:54:23 2017

@author: liusl
"""
import numpy as np
import scipy.io as sio
import pandas as pd
import os
import time
import statsmodels.api as sm
import Common.TimeCodeGet as tc

dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)



loadPath = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/TraVol/YearAllSto_ReaVol/Diff_RealizedVolatility.mat'
index=0; pool='HS300'; saveBool=True; facName='Factor'
    
    
'''
load dataDic as follows:
arrName = facName + 'Values_Three3DArray'    
dataDic = {'axis1Names_Items': np.array(itemsLis, dtype=object),
           'axis2Names_DateSeries': dataDSArr.reshape(len(dataDSArr), 1),\
           'axis3Names_ComCode': dataComCodeArr,\
           arrName: data3DArr, \
           'arrKey': [arrName, 'axis1Names_Items', 'axis2Names_DateSeries', 'axis3Names_ComCode']}
'''

# load stock log return
pathStoLogRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_arr.mat'
dataStoRetDic = sio.loadmat(pathStoLogRet)
dataStoRetDic.keys()
dataInner = dataStoRetDic['colInnerCode'][0]
dataDS = dataStoRetDic['indexDate'][:, 0]


# load free return, not use
#    pathFreeRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Wind_Daily10YearBond_LogReturn_array.mat'
#    dataFreeRet = sio.loadmat(pathFreeRet)['TenYearBond_LogReturn']

# stock free return    
#    dataStoFreeRet = dataStoRet - dataFreeRet
dataStoFreeRet = dataStoRetDic['StoLogReturn']# not need free stock return 

# load Factor values    
dataFactorValuesDic = sio.loadmat(loadPath)
#facArrKey = dataFactorValuesDic['arrKey'][0]
#dataFactorValues = dataFactorValuesDic[facArrKey]
#if dataFactorValues.ndim == 3 :
#    dataFactorValues = dataFactorValues[index]    
dataFactorValuesDic.keys()
dataFactorValues = dataFactorValuesDic['DifRealVolit']


dataCodeDF = tc.codeDFGet()
secuCode = [float(i) for i in map(lambda x:x[0],  dataCodeDF['SecuCode'].values)]

dataFactorValuesDF = pd.DataFrame(dataFactorValues, index=dataFactorValuesDic['dateSeries'][:, 0], \
                                    columns=dataFactorValuesDic['SecuCode'][0])

dataFactorValuesUseDF = dataFactorValuesDF.reindex(index=dataDSArr, columns=secuCode)
dataFactorValuesUseDF.columns = dataInnerCodeArr
dataFactorValuesUseDF = dataFactorValuesUseDF.loc[dataDS, dataInner]

dataFactorValues = dataFactorValuesUseDF.values

olsCounts = 200
# select stock pool
if pool == 'HS300':    
    print 'HS300 pool'
    # load HS300 index  0/1 sheet
    olsCounts = 20 # regression sample counts
    
    dataHS300IndexDF = tc.codeIndexDFGet(codeStr='HS300')
    dataHS300IndexDF[dataHS300IndexDF==0] = np.nan
    dataHS300IndexDF = dataHS300IndexDF.loc[dataDS, dataInner]
#        print dataHS300IndexDF
    dataStoFreeRet = dataStoFreeRet * dataHS300IndexDF.values.astype(float)
    dataFactorValues = dataFactorValues * dataHS300IndexDF.values.astype(float)

# factor values standardize
dataFactorStandArr = np.zeros_like(dataFactorValues)
dataFactorStandArr[:] = np.nan

for i in range(len(dataFactorValues)):
    dataFactorValueTemp = dataFactorValues[i][(~np.isnan(dataFactorValues[i]))&(~np.isnan(dataFactorValues[i]))]
    if len(dataFactorValueTemp) >=2:
                
        dataMeanTemp = np.mean(dataFactorValueTemp)
        dataStdTemp = np.std(dataFactorValueTemp)
        dataFactorStandArr[i] = (dataFactorValues[i] - dataMeanTemp) / dataStdTemp

# OLS   calculate cross section factor return    
    
dataFactorOLSReturn = np.zeros((len(dataFactorStandArr), 1))        
dataFactorOLSReturn[:] = np.nan



print 'start calculate Barra return'        
print time.strftime("%H:%M:%S", time.localtime())
print 'dateCounts', 'date'
for i in range(len(dataFactorStandArr)):        
    useBool = (~np.isnan(dataFactorStandArr[i])) & (~np.isnan(dataStoFreeRet[i]))
    Xuse = dataFactorStandArr[i][useBool]
    
    if len(Xuse)>olsCounts:        
        Yuse = dataStoFreeRet[i][useBool]
        X = sm.add_constant(Xuse)
        result = sm.OLS(Yuse, X).fit()
        dataFactorOLSReturn[i, 0] = result.params[1]
        if i%1000 == 0:
            print dataDSArr[i]
            
aa = dataFactorOLSReturn[~np.isnan(dataFactorOLSReturn)]            
arrName = facName + '_' + pool + '_' + 'BarraReturn'
dataDic = {'indDate': dataDSArr.reshape(len(dataDSArr), 1), \
            arrName: dataFactorOLSReturn, 'arrKey': [arrName, 'indDate']}

#%%
#if saveBool :

#    savePath = os.path.split(loadPath)[0]
#    saveName = savePath + '/' + arrName + '_arr.mat'
#    sio.savemat(saveName, dataDic)
#    print arrName + '_arr.mat', 'saved'
#return dataFactorOLSReturn


import Common.SmaFun as sf
#import Com
import matplotlib.pyplot as plt

facName_Pool = 'HS300'


corUseLis = ['lightcoral', 'red', 'gold', 'lawngreen',\
            'darkgreen', 'aquamarine', 'dodgerblue', 'blue', 'mediumorchid', 'fuchsia', 'pink']
if dataFactorOLSReturn is not None:
    dataRetRawArr = dataFactorOLSReturn
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
dataRetArr[np.isnan(dataRetArr)] = 0
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
    ax1.plot(range(len(dataDS)), dataRetCumArr[:, i], color=corUseLis[i], lw=1.5, label='Group'+str(i+1))   
    
ax1.set_xlim(startInd-250, len(dataDS)+400)

#    ax1.set_ylim(-0.5, 2.5 )
ax1.set_xticks(range(startInd, len(dataDS), 250))
ax1.set_xticklabels([dataDS[i] for i in ax1.get_xticks()], rotation=30, fontsize='small')
#ax1.set_yticks(range(-0.3, 1.8, 0.2))
ax1.set_yticklabels([str((int(i*100)))+'%' for i in ax1.get_yticks()])
titleName = facName_Pool + '_' + str(groNums) + 'Groups_ExcessReturn'
ax1.set_title(titleName)
#ax1.set_xlabel('Date')
ax1.set_ylabel('Cumulative_ExcessReturn')
ax1.legend(loc=1, fontsize='small')
#%%
#
#
aa = np.where(~np.isnan(dataRetCumArr))[0]
bb = dataRetCumArr[aa]
#    
cc = np.power((bb[-1]+1), 250./len(bb))     
#
#np.power?