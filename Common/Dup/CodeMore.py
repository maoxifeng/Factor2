# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import scipy.io as sio
import os
import time



pathCode = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
dataCodeRaw = sio.loadmat(pathCode)
dataCodeRaw.keys()
dataCodeArr = dataCodeRaw['data']
dataInnerCodeArr = dataCodeArr[:, 0]
dataComCodeArr = dataCodeArr[:, 1] # 3415
dataComCodeArr.shape
dataCodeArr.shape
# import secuCode
pathCode = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/AStockCode_mat.mat'
dataCodeRaw = sio.loadmat(pathCode)
dataCodeRaw.keys()
dataSecuCodeRaw = dataCodeRaw['secuCode']
dataSecuCodeRaw.shape
dataSecuCodeArr = np.array([dataSecuCodeRaw[i][0][0] for i in range(len(dataSecuCodeRaw))])
dataMarRaw = dataCodeRaw['data'][:, 2]
data90Arr = dataSecuCodeArr[dataMarRaw==90]   # 2064 counts
data83Arr = dataSecuCodeArr[dataMarRaw==83]    # 1378 counts
dataCodeRaw['data'].shape

df1 = pd.DataFrame(dataCodeArr, columns = ['inner', 'com'])
df2 = pd.DataFrame(dataCodeRaw['data'], columns = ['inner', 'com', 'market'])
df2['secu'] = dataSecuCodeArr

df3 = df2[~df2['inner'].isin(dataInnerCodeArr)]
df4 = df3.sort_values('secu')

df_1011 = df4[df4['market']==83]
df_1012 = df4[df4['market']==90]




