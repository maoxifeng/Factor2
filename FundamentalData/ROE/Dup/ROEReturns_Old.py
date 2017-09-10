#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 13:32:02 2017

@author: liushuanglong
"""


'''
#==============================================================================
# calculate the ROE return: High minus Low 
#==============================================================================
'''


import numpy as np
import scipy.io as sio
import pandas as pd
import cPickle as cp


#==============================================================================
# 1. load 3 stock groups by ROE, stoct daily returns, stock daily volumne, stock AFloats
#==============================================================================


## load code number
pathCode = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
dataCodeRaw = sio.loadmat(pathCode)
dataCodeArr = dataCodeRaw['data']
dataInnerCodeArr = dataCodeArr[:, 0]
dataComCodeArr = dataCodeArr[:, 1]


## load 3 stock groups by ROE
pathGroups = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/stoThreeGroupsByROE_Dic.pkl'
thrGroComCodeDic = cp.load(open(pathGroups, 'r'))   # company code 
#lowGroupDic = thrGroComCodeDic['low'] 
#medGroupDic = thrGroComCodeDic['median'] 
#higGroupDic = thrGroComCodeDic['high'] 
yearGroupLis = thrGroComCodeDic['year'] 
#
#aaaa = [thrGroComCodeDic[i][1996] for i in ['low', 'median', 'high']]

## load stoct daily returns
pathReturn = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_mat.mat'
dataReturnRaw = sio.loadmat(pathReturn)

dataTSArr = dataReturnRaw['indexTime'][:, 0]   # 6498
#dataInnerCodeArr = dataReturnRaw['colInnerCode'][0]   #3415
dataReturnArr = dataReturnRaw['DailyQuote_LogReturn']


## load stock daily volumne
pathVol = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_TurnoverVolume_mat.mat'
dataVolRaw = sio.loadmat(pathVol)
#dataVolRaw.keys()
dataVolArr = dataVolRaw['DailyQuote_TurnoverVolume']  # columns: inner code


## load stock AFloats
pathAF = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_AFloats_mat.mat'
dataAFloatsRaw = sio.loadmat(pathAF)
dataAFloats3DArr = dataAFloatsRaw['LC_AFloats']
#dataAFloatsRaw.keys()
dataAFloatsArr = dataAFloats3DArr[0]


#==============================================================================
# 2. calculate grouped ROE daily return
#==============================================================================

# keep effective data
dataVolUseArr = np.zeros((len(dataTSArr), len(dataComCodeArr)))
dataReturnUseArr = np.zeros((len(dataTSArr), len(dataComCodeArr)))
dataAFloatsUseArr = np.zeros((len(dataTSArr), len(dataComCodeArr)))
dataReturnUseArr[:] = np.nan
dataVolUseArr[:] = np.nan
dataAFloatsUseArr[:] = np.nan

#bool1Arr = np.where((~np.isnan(dataVolArr[1])) & (dataVolArr[1]!=0))
for i in range(len(dataTSArr)):
    posUseArr = np.where((~np.isnan(dataVolArr[i])) & (dataVolArr[i]!=0))
    dataVolUseArr[i][posUseArr] = dataVolArr[i][posUseArr]
    dataReturnUseArr[i][posUseArr] = dataReturnArr[i][posUseArr]
    dataAFloatsUseArr[i][posUseArr] = dataAFloatsArr[i][posUseArr]
    if i%100 == 0:
        print i,


#dataVolDF = pd.DataFrame(dataVolUseArr, index=dataTSArr, columns=dataComCodeArr)
dataReturnDF = pd.DataFrame(dataReturnUseArr, index=dataTSArr, columns=dataComCodeArr)
dataAFloatsDF = pd.DataFrame(dataAFloatsUseArr, index=dataTSArr, columns=dataComCodeArr)

# 3 groups return
dataROEReturnDF = pd.DataFrame([], index=dataTSArr, columns=['low', 'median', 'high', 'HML'])

counts = 0
for year in yearGroupLis:
    groupTemLis = [thrGroComCodeDic[i][year] for i in ['low', 'median', 'high']]
    for date in dataTSArr[(dataTSArr>(year*10000+430)) & (dataTSArr<((year+1)*10000+501))]:
        
        for i, gr in enumerate(groupTemLis):
            
            dataOGTemDF = pd.DataFrame(index=gr, columns=['return', 'aFloats', 'weight', 'wReturn'])
            dataOGTemDF['return'] = dataReturnDF.loc[date][gr]
            dataOGTemDF['aFloats'] = dataAFloatsDF.loc[date][gr]
            dataOGTemDF['weight'] = dataOGTemDF['aFloats'] / dataOGTemDF['aFloats'].sum()
            dataOGTemDF['wReturn'] = dataOGTemDF['return'] * dataOGTemDF['weight']				
            dataROEReturnDF.loc[date].iloc[i] = dataOGTemDF['wReturn'].sum()
        counts = counts + 1    
        if counts%50 == 0:
            print date, 

dataROEReturnDF['HML'] = dataROEReturnDF['high'] - dataROEReturnDF['low']

dataROEReturnDF.describe()
dataROEReturnDF.corr()

# save 3 groups ROE return
colArr = np.zeros((1, len(dataROEReturnDF.columns)), dtype=object)
for i, j in enumerate(dataROEReturnDF.columns):
    colArr[0][i] = np.array([j])

dataDic = {'colItems': colArr, \
           'indexTime': dataTSArr.reshape(len(dataTSArr), 1), \
           'LC_YearDuration_ROE_3Groups_Return': dataROEReturnDF.values}
           
sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_YearDuration_ROE_3Groups_Return_arr.mat', dataDic)


#import matplotlib.pyplot as plt
#
#fig = plt.figure(figsize=(20, 8))
#ax1 = fig.add_subplot(411)
#ax2 = fig.add_subplot(412)
#ax3 = fig.add_subplot(413)
#ax4 = fig.add_subplot(414)
#ax1.plot(range(len(dataROEReturnDF.index)), dataROEReturnDF['HML'].values, label='HML')
#ax2.plot(range(len(dataROEReturnDF.index)), dataROEReturnDF['low'].values, label='low')
#ax3.plot(range(len(dataROEReturnDF.index)), dataROEReturnDF['median'].values, label='median')
#ax4.plot(range(len(dataROEReturnDF.index)), dataROEReturnDF['high'].values ,label='high')
#ax1.legend(loc='best')
#ax2.legend(loc='best')
#ax3.legend(loc='best')
#ax4.legend(loc='best')
#
#plt.savefig('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROEReturn.png', dpi=800)



















