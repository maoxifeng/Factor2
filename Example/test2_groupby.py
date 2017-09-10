#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:03:44 2017

@author: liushuanglong
"""

import numpy as np
import scipy.io as sio
import pandas as pd




path = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Financial/Return_HS300_3145_2005_to_3000_array.mat'

dataRaw = sio.loadmat(path)  
dataColTol = [dataRaw['colNames'][0][i][0] for i in range(dataRaw['colNames'].shape[1])]

dataReturn = pd.DataFrame(columns = dataColTol)
dataReturn[dataColTol[0]] = dataRaw['indexTime'][:, 0]
dataReturn[dataColTol[1]] = dataRaw['Return_HS300_3145_2005_to_3000'][:, 0]

dataReturn[u'Month'] = map(lambda x: round(x, 0),  dataReturn[u'TradingDay']/100)


dataReturnMonthGB = dataReturn.groupby(dataReturn[u'Month'])

for name, group in dataReturnMonthGB:
    print name;
    print group



dataReturnMonthLis = list(dataReturnMonthGB)
pieces = dict(list(dataReturnMonthGB))
   












