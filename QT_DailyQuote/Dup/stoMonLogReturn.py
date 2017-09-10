#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 09:04:06 2017

@author: liushuanglong
"""

'''
#==============================================================================
# log month end return
#==============================================================================
'''

import numpy as np
import scipy.io as sio
import pandas as pd
import cPickle as cp
import math



pathMon = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/endMonthDate_mat.mat'
pathAdjClose = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_AdjClosePriceReal_mat.mat'

MonEndRaw = sio.loadmat(pathMon)
dataAdjCloseRaw = sio.loadmat(pathAdjClose)     # load adj close

MonEndTSArr = MonEndRaw['endMonthDate'][:, 0]   # 320
#MonEndTSArr = MonEndTSArr[:-1]   # 319
dataAdjCloArr = dataAdjCloseRaw['AdjClosePriceReal']
dataTSArr = dataAdjCloseRaw['indexTimeReal'][:, 0]   # 6498
dataInnerCodeArr = dataAdjCloseRaw['colInnerCode'][0]  # 3415

dataAdjCloDF = pd.DataFrame(dataAdjCloArr, index =dataTSArr, columns=dataInnerCodeArr)

# calculate month log return
dataAdjCloLogDF = dataAdjCloDF.applymap(lambda x: math.log(x))
dataAdjCloMonDF = dataAdjCloLogDF.loc[MonEndTSArr]       # 320 * 3415

# create a new mon return dataframe
dataLogReturnMonDF = pd.DataFrame([], index=MonEndTSArr[1:], columns=dataInnerCodeArr)  # 319 * 3415
for i in range(1, len(MonEndTSArr)):
    dataLogReturnMonDF.iloc[i-1] = dataAdjCloMonDF.iloc[i] - dataAdjCloMonDF.iloc[i-1]
    

# save as pkl
cp.dump(dataLogReturnMonDF, open('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/dataLogReturnMonDF.pkl', 'w'))

















