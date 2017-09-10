# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import scipy.io as sio

pathTS =  '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat'     
dataTSRaw = sio.loadmat(pathTS)      
dataTSArr = dataTSRaw['data'][:, 0]     # 6498

indexTimeDouLis = map(lambda x: float(x),  dataTSArr)
indexTime = np.array([indexTimeDouLis]).T

dataTDic = {'dateSeries': indexTime}
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat', dataTDic)





