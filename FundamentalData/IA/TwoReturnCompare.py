# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 09:16:56 2017

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



pathOLS = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/InvestmentsToAssets/Dif_InvestmentsToAssets_OLSReturn_arr.mat'
pathFM = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/InvestmentsToAssets/LC_YearDuration_IA_3Groups_Return_arr.mat'


dataOLS = sio.loadmat(pathOLS)['IA_OLSReturn'][:, 0]
#dataOLS.keys()
dataFM = sio.loadmat(pathFM)['LC_YearDuration_IA_3Groups_Return'][:, 3]


accuOLS = np.zeros_like(dataOLS)
accuOLS[...] = np.nan
accuFM = np.zeros_like(dataFM)
accuFM[...] = np.nan

aa = np.where(np.isnan(dataOLS))[0]
bb = np.where(np.isnan(dataFM))[0]
start = max(aa[-1], bb[-1]) + 1

accuOLS[:start] = 0
accuFM[:start] = 0
#
#for ii in range(start, len(dataOLS)):
#    accuOLS[ii] = accuOLS[ii-1] + dataOLS[ii]
#    accuFM[ii] = accuFM[ii-1] + dataFM[ii]
#
#accuOLSAb = accuOLS[np.abs(dataOLS) > 2]
#am = np.max(dataOLS[~np.isnan(dataOLS)])
#am2 = np.max(accuOLS[~np.isnan(accuOLS)])
#
#iiab = np.where(dataOLS==am)[0]
#iiab2 = np.where(accuOLS==am2)[0]
#dataDSArr[iiab2]
#dataDSArr[5959]
##
#import scipy.stats as stats
#cor1, pval1 = stats.pearsonr(accuOLS[start:], accuFM[start:])   # 0.3
#cor2, pval1 = stats.spearmanr(accuOLS[start:], accuFM[start:])   # 0.6


path300OLS = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/InvestmentsToAssets/Dif_InvestmentsToAssets_HS300_OLSReturn_array.mat'
path300FM = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/InvestmentsToAssets/Dif_InvestmentsToAssets_HS300_FMReturn_array.mat'

data300OLS = sio.loadmat(path300OLS)
data300OLS.keys()
data300OLSArr = data300OLS['HS300_OLSReturn'][:, 0]
data300OLSArr.shape
data300FM = sio.loadmat(path300FM)
data300FM.keys()
data300FMArr = data300FM['Factor_FMReturn'][:, 3]

fm1 = np.where(~np.isnan(data300FMArr))[0][0]
ols1 = np.where(~np.isnan(data300OLSArr))[0][0]
fm1
ols1
start300 = ols1

data300FMArr[:start300] = 0
data300OLSArr[:start300] = 0

olsCumsum = np.zeros_like(data300FMArr)
fmCumsum = np.zeros_like(data300FMArr)

for i in range(start300, len(data300FMArr)):
    olsCumsum[i] = olsCumsum[i-1] + data300OLSArr[i]
    fmCumsum[i] = fmCumsum[i-1] + data300FMArr[i]



import scipy.stats as stats
cor1, pval1 = stats.pearsonr(olsCumsum[start300:], fmCumsum[start300:])   # 0.3
cor2, pval2 = stats.spearmanr(olsCumsum[start300:], fmCumsum[start300:])   # 0.3


import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
#ax.plot(range(len(olsCumsum[start300:])), olsCumsum[start300:], label='OLS_HS300')
ax.plot(range(len(fmCumsum[start300:])), fmCumsum[start300:], label='FM_HS300')
#ax.plot(range(len(fmCumsum[start300:])), accuOLS[start300:], label='OLS_A')
ax.plot(range(len(fmCumsum[start300:])), accuFM[start300:], label='FM_A')
ax.set_xticks(range(0, len(fmCumsum[start300:]), 200))
ax.set_xticklabels([int(i) for i in dataDSArr[start300:][range(0, len(fmCumsum[start300:]), 200)]], rotation=30)
#ax.set_xlim([1588, 2000])
ax.legend(loc='best')

#
aa = np.where(dataDSArr[start300:]==20080801)
aaa = np.where(dataDSArr==20080801)

aa
        