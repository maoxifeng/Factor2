# -*- coding: utf-8 -*-



# ============ import modules =================
import gfunddataprocessor.gfunddataprocessor as gfd
import pandas as pd
import numpy as np
import scipy.io as sio
import os
import time
from datetime import datetime

#import pdb
#pdb.set_trace()


# import secuCode
pathCode = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/AStockCode_mat.mat'
dataCodeRaw = sio.loadmat(pathCode)
dataCodeRaw.keys()
dataSecuCodeRaw = dataCodeRaw['secuCode']
dataSecuCodeRaw.shape
dataSecuCodeArr = np.array([dataSecuCodeRaw[i][0][0] for i in range(len(dataSecuCodeRaw))])
dataMarRaw = dataCodeRaw['data'][:, 2]

data90Arr = dataSecuCodeArr[dataMarRaw==90]   # 2064 counts

data90_1Arr = data90Arr[:300]
data90_2Arr = data90Arr[300: 600]
data90_3Arr = data90Arr[600:900]
data90_4Arr = data90Arr[900:1200]
data90_5Arr = data90Arr[1200:1500]
data90_6Arr = data90Arr[1500:1800]
data90_7Arr = data90Arr[1800:]   # 264 counts

data83Arr = dataSecuCodeArr[dataMarRaw==83]    # 1378 counts
data83_1Arr = data83Arr[:300]         # 600008 interupt
data83_2Arr = data83Arr[300:600]     # 600351 interupt
data83_3Arr = data83Arr[600:900]     # 600699 interupt
data83_4Arr = data83Arr[900:1200]     # 601106 interupt
data83_5Arr = data83Arr[1200:]     # 178 counts  # completed
