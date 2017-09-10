#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 14:35:01 2017

@author: liushuanglong
"""

import numpy as np
import scipy.io as sio
import pandas as pd
import math

import Common.TimeCodeGet as tc

# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)



pathB = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/bond_10y_mat.mat'
dataBRaw = sio.loadmat(pathB)
dataBArr = dataBRaw['data']    # 3780
dataCol = [dataBRaw['col'][0][i][0] for i in range(len(dataBRaw['col'][0]))]
bondDateArr = dataBArr[:, 0]

dataBondLogReturnArr =  np.zeros(dataBArr.shape[0])
dataBondLogReturnArr[:] = np.nan
dataBondLogReturnArr[1:] = np.log(dataBArr[1:, 1]) - np.log(dataBArr[:-1, 1])

dataBondLogReturnDF = pd.DataFrame(dataBondLogReturnArr, index=bondDateArr)
dataBondLogReturnUseDF = dataBondLogReturnDF.loc[dataDSArr]
dataBondLogReturn = dataBondLogReturnUseDF.values


dataDic = {'indexDate': dataDSArr.reshape(len(dataDSArr), 1), 'TenYearBond_LogReturn': dataBondLogReturn}
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Wind_Daily10YearBond_LogReturn_array.mat', dataDic)

