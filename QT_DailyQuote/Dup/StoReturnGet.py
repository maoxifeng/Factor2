#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 12:10:33 2017

@author: liushuanglong
"""

'''
#==============================================================================
# every stock log daily return
#==============================================================================
'''

import numpy as np
import scipy.io as sio
import pandas as pd
import Common.TimeCodeGet as tc


dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)


pathAdjClose = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_AdjClosePrice_array.mat'

dataAdjCloseRaw = sio.loadmat(pathAdjClose)     # load adj close

dataAdjCloArr = dataAdjCloseRaw['AdjClosePrice']
dataLogReturnArr = np.zeros_like(dataAdjCloArr)
dataLogReturnArr[:] = np.nan
dataLogReturnArr[1:] = np.log(dataAdjCloArr[1:]) - np.log(dataAdjCloArr[:-1])

dataDic = {'colInnerCode': dataInnerCodeArr, 'indexDate': dataDSArr.reshape(len(dataDSArr), 1), 'StoLogReturn': dataLogReturnArr}
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_array.mat', dataDic)
