# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 10:02:28 2017

@author: liusl
"""

import numpy as np
#import pandas as pd
import scipy.io as sio
import Common.SmaFun as cs

pathCode = '/data/liushuanglong/MyFiles/Data/Common/astock.mat'
dataDF = cs.SheetToDFGet(pathCode).set_index('InnerCode')
lastInnerCode = sio.loadmat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/ordInnerCode.mat')['ordInnerCode'][0]
newInnerCode = dataDF.index.tolist()

addInnerCode = list(set(newInnerCode) - set(lastInnerCode))
orderInnerCode = np.concatenate([lastInnerCode, addInnerCode]).astype(float)

dataDic = {'ordInnerCode': orderInnerCode}
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/ordInnerCode.mat', dataDic)





