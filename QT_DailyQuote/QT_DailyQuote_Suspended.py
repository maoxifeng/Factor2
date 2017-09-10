# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import scipy.io as sio




pathVol = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_TurnoverVolume_mat.mat'
dataVolRaw = sio.loadmat(pathVol)
dataVolRaw.keys()
dataVolArr = dataVolRaw['DailyQuote_TurnoverVolume']  # columns: inner code
dataVolArr.shape

dataSuspendArr = np.zeros_like(dataVolArr)
dataSuspendArr[:] = np.nan

for i in range(len(dataSuspendArr)):
    dataSuspendArr[i][dataVolArr[i] == 0] = 1
    dataSuspendArr[i][dataVolArr[i] > 0] = 0

colInnerCodeDouLis = map(lambda x: float(x),  dataVolRaw['colInnerCode'][0])
indexTimeDouLis = map(lambda x: float(x),  dataVolRaw['indexTime'][:, 0])

colInnerCode = np.array([colInnerCodeDouLis])
indexTime = np.array([indexTimeDouLis]).T

dataDic = {'colInnerCode': colInnerCode, 'indexTime': indexTime, 'Suspended_20170714': dataSuspendArr}
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/Suspended_20170714.mat', dataDic)


#float(dataSuspendArr[np.where(dataSuspendArr==1)].size) / dataSuspendArr[np.where(~np.isnan(dataSuspendArr))].size