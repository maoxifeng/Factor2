#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 20:28:59 2017

@author: liushuanglong
"""

#==============================================================================
# adjusting fators * close price
#==============================================================================

import numpy as np
import scipy.io as sio
import pandas as pd
import Common.TimeCodeGet as tc

dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)


pathAdj = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_RatioAdjustingFactor_array.mat'
pathClose = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_ClosePrice_array.mat'

# load data
dataAdjRaw = sio.loadmat(pathAdj)
dataCloseRaw = sio.loadmat(pathClose)

dataAdjArr = dataAdjRaw['RatioAdjustingFactor']
dataCloseArr = dataCloseRaw['ClosePrice']

# calculate adjusted closeprice
dataCloseAdjArr = dataAdjArr * dataCloseArr

# save data
dataDic = {'colInnerCode': dataInnerCodeArr, 'indexDate': dataDSArr.reshape(len(dataDSArr), 1), 'AdjClosePrice': dataCloseAdjArr}
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_AdjClosePrice_array.mat', dataDic)












