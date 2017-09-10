# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 11:18:30 2017

@author: liusl
"""

'''
Here we calculate idiosyncratic volatility from CAPM model.

simga_e = sigma_ri - sigma_rm , r is the free risk log return


'''


import numpy as np
import scipy.io as sio
import pandas as pd
import os
import time
import statsmodels.api as sm
import Common.TimeCodeGet as tc

# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)

savePath = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/TraVol/IdioVolatility/'


#==============================================================================
# 1. calculate idiosyncratic volatility values
#==============================================================================
# load beta data, year regression data
pathBeta = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/HS300Index_Free_FMExposure_250RDs_array.mat'
dataBetaDic = sio.loadmat(pathBeta)
    
facArrKey = dataBetaDic['arrKey'][0]
dataBetaArr = dataBetaDic[facArrKey]    

# load HS300 Index free risk log return
pathMar = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/IndexQuote_HS300Free_LogReturn_arr.mat'
dataMarRetRaw = sio.loadmat(pathMar)
dataMarRetArr = dataMarRetRaw[dataMarRetRaw['arrKey'][0]]

## load stoct daily returns
pathStoLogRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_array.mat'
dataStoRetArr = sio.loadmat(pathStoLogRet)['StoLogReturn']
# load free returns

pathFreeRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Wind_Daily10YearBond_LogReturn_array.mat'
dataFreeRetArr = sio.loadmat(pathFreeRet)['TenYearBond_LogReturn']

# stock free return !
dataStoFreeRetArr = dataStoRetArr - dataFreeRetArr

def nonNanIndexFirst(arr):
    for i in xrange(len(arr)):
        if len(arr[i][~np.isnan(arr[i])]) > 0:
            break
    return i

regDays = 250
T = 250
dataIdiVolArr = np.ones_like(dataBetaArr)
dataIdiVolArr[:] = np.nan
startInd = nonNanIndexFirst(dataBetaArr)

print 'start calculate idiosyncratic volatility: ',
print time.strftime("%H:%M:%S", time.localtime())
print 'date', 'nowTime'
for d in range(startInd, len(dataDSArr)):
    stoRetTmp = dataStoFreeRetArr[d-regDays+1: d+1]
    marRetTmp = dataMarRetArr[d-regDays+1: d+1, 0]
    sigmaMar = np.var(marRetTmp[~np.isnan(marRetTmp)])
    
    for s in range(len(dataInnerCodeArr)):
        if np.isnan(dataBetaArr[d, s]):
            continue
        sigmaSto = np.var(stoRetTmp[:, s][~np.isnan(stoRetTmp[:, s])])
        dataIdiVolArr[d, s] = np.sqrt((sigmaSto - dataBetaArr[d, s]**2 * sigmaMar ) * T)
    if d%100 == 0:
        print dataDSArr[d], time.strftime("%H:%M:%S", time.localtime())
        
arrName = 'IdioVol_CAPM_250RDs'
dataDic={'colInnerCode': dataInnerCodeArr, 
         'indDate': dataDSArr.reshape(len(dataDSArr), 1),
            arrName: dataIdiVolArr, 
            'arrKey': [arrName, 'indDate', 'colInnerCode']}
sio.savemat(savePath+arrName+'_arr.mat', dataDic)

#==============================================================================
# 2. calculate Barra return
#==============================================================================

pathIdiVol = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/TraVol/IdioVolatility_CAPM/IdioVol_CAPM_250RDs_arr.mat'

import FundamentalData.FunCommon.FactorReturnGet as facret

# all stock regression
IdiVol_A_Return = facret.FactorBarraReturnGet(pathIdiVol, facName='IdioVol')


# HS300 stock regression
IdiVol_HS300_Return = facret.FactorBarraReturnGet(pathIdiVol, facName='IdioVol', pool='HS300')


ee = IdiVol_HS300_Return - dataMarRetArr

#%%
aa = IdiVol_A_Return[:, 0].copy()
bb = IdiVol_HS300_Return[:, 0].copy()
aaa = np.where(~np.isnan(aa))[0][0]

aa[:aaa] = 0
aaCum = np.cumsum(aa)

bb[:aaa] = 0
bbCum = np.cumsum(bb)

cc = dataMarRetArr[:, 0].copy()
cc[:aaa] = 0
ccCum = np.cumsum(cc)

ff = dataMarRetArr[:, 0]+dataFreeRetArr[:, 0]
gg = ff.copy()
gg[:startInd] = 0
ggCum = np.cumsum(gg)

re1 = np.corrcoef(aa, cc)
re2 = np.corrcoef(bb, cc)

re2
re1

#dd = ccCum - bbCum
#%%

import matplotlib.pylab as plt

fig = plt.figure(figsize=(10, 8))
ax1 = fig.add_subplot(111)
ax1.plot(range(len(dataDSArr)), aaCum, lw=2, color='r', label='IdioVol_A_Return')
ax1.plot(range(len(dataDSArr)), bbCum, lw=2, color='b', label='IdioVol_HS300_Return')
ax1.plot(range(len(dataDSArr)), ccCum, lw=2, color='y', label='marketFreeReturn')
#ax1.plot(range(len(dataDSArr)), ggCum, lw=2, color='g', label='marketReturn')
ax1.set_xlim(aaa, len(dataDSArr)+250)
#ax1.set_ylim(0, 2 )
ax1.set_xticks(range(aaa, len(dataDSArr), 250))
ax1.set_xticklabels([dataDSArr[i] for i in ax1.get_xticks()], rotation=30, fontsize='small')
#ax1.set_yticks(range(-0.3, 1.8, 0.2))
ax1.set_yticklabels([str((i*100))+'%' for i in ax1.get_yticks()])
ax1.set_title('IdiVol_BarraReturn')
#ax1.set_xlabel('Date')
ax1.set_ylabel('CumReturn')
ax1.legend(loc=9)
#plt.savefig(savePath+'IdiVol_BarraReturn', dpi=600)





#%%
#==============================================================================
# have a see

import matplotlib.pylab as plt


ee = dataStoRetArr.copy()
ee[:startInd] = 0
eeCum = np.cumsum(ee, axis=0)
ff = dataMarRetArr[:, 0]+dataFreeRetArr[:, 0]
gg = ff.copy()
gg[:startInd] = 0
ggCum = np.cumsum(gg)

#%%

fig = plt.figure(figsize=(20, 15))
ax1 = fig.add_subplot(221)
ax1.scatter(range(len(dataDSArr)), dataIdiVolArr[:, 0], s=5, color='r', label='0')
ax1.scatter(range(len(dataDSArr)), dataIdiVolArr[:, 1], s=5, color='b', label='1')
ax1.scatter(range(len(dataDSArr)), dataIdiVolArr[:, 4], s=5, color='g', label='4')
ax1.set_xlim(startInd-50, len(dataDSArr)+50)
#ax1.set_ylim(0.8, 1.2 )
ax1.set_xticks(range(startInd, len(dataDSArr), 250))
ax1.set_xticklabels([dataDSArr[i] for i in ax1.get_xticks()], rotation=30, fontsize='small')
ax1.set_title('IdiVol')
ax1.legend(loc=2)

ax2 = fig.add_subplot(222)
ax2.scatter(range(len(dataDSArr)), dataBetaArr[:, 0], s=5, color='r', label='0')
ax2.scatter(range(len(dataDSArr)), dataBetaArr[:, 1], s=5, color='b', label='1')
ax2.scatter(range(len(dataDSArr)), dataBetaArr[:, 4], s=5, color='g', label='4')
ax2.set_xlim(startInd-50, len(dataDSArr)+50)
#ax2.set_ylim(0.8, 1.2 )
ax2.set_xticks(range(startInd, len(dataDSArr), 250))
ax2.set_xticklabels([dataDSArr[i] for i in ax2.get_xticks()], rotation=30, fontsize='small')
ax2.legend(loc=2)
ax2.set_title('MarBeta')


ax3 = fig.add_subplot(223)

ax3.scatter(range(len(dataDSArr)), eeCum[:, 0], s=5, color='r', label='0')
ax3.scatter(range(len(dataDSArr)), eeCum[:, 1], s=5, color='b', label='1')
ax3.scatter(range(len(dataDSArr)), eeCum[:, 4], s=5, color='g', label='4')
ax3.scatter(range(len(dataDSArr)), ggCum, s=5, color='y', label='market')
ax3.set_xlim(startInd-50, len(dataDSArr)+50)
ax3.set_ylim(-1, 4 )
ax3.set_xticks(range(startInd, len(dataDSArr), 250))
ax3.set_xticklabels([dataDSArr[i] for i in ax3.get_xticks()], rotation=30, fontsize='small')
ax3.legend(loc=2)
ax3.set_title('Return')

#plt.savefig(savePath+'IdiVol.png', dpi=600)





