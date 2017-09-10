#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:42:42 2017

@author: liushuanglong
"""


import numpy as np
import scipy.io as sio
import pandas as pd
import Common.TimeCodeGet as tc

pathAJ = '/data/liushuanglong/MyFiles/Data/JYDB2/QT_AdjustingFactor/QT_AdjustingFactor.mat'

#  adjusting factors data   
dataRaw = sio.loadmat(pathAJ)     
dataColTol = [dataRaw['col'][0][i][0] for i in range(dataRaw['col'].shape[1])]
useLis = [dataColTol.index(i) for i in [u'ExDiviDate', u'RatioAdjustingFactor', u'InnerCode']]
dataCol = [dataColTol[i] for i in useLis]
dataArr = dataRaw['data'][:, useLis]
dataDFTol = pd.DataFrame(dataArr, columns=dataCol)


# load total time and InnerCode of closeprice
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)

# transpose and fillna
dataDFUse = dataDFTol[dataDFTol[u'InnerCode'].isin(dataInnerCodeArr)]
dataDFUseSort = dataDFUse.sort_values(by=[u'ExDiviDate', u'InnerCode'])
dataDFUseSta = dataDFUseSort.set_index([u'ExDiviDate', u'InnerCode'])[u'RatioAdjustingFactor'].unstack()
dataDFUseFil = dataDFUseSta.fillna(method='ffill')
dataDFUseFilTol = dataDFUseFil.fillna(1.)


# total time fillna\
dataUseTolTime = dataDFUseFilTol.loc[dataDSArr]      # this way may be good~
dataUseTolTimeFil = dataUseTolTime.fillna(method='ffill')
dataUseTolTimeFil = dataUseTolTimeFil.fillna(1.)

# total InnerCode fillna
dataUseTolFil = dataUseTolTimeFil.reindex(columns=dataInnerCodeArr, fill_value=1.)

# calculate adjusting factors
dataAdFactors = dataUseTolFil / dataUseTolFil.iloc[-1]

# save data
dataDic = {'colInnerCode': np.array(dataAdFactors.columns), \
           'indexDate': np.array(dataAdFactors.index).reshape(len(dataAdFactors.index), 1), \
           'RatioAdjustingFactor': dataAdFactors.values}
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_RatioAdjustingFactor_array.mat', dataDic)




