#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 16:30:44 2017

@author: liushuanglong
"""

'''
#==============================================================================
# end month date time series
#==============================================================================
'''

import numpy as np
import scipy.io as sio
import pandas as pd
import cPickle as cp


# load data series
pathTS =  '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat'     
dataTSRaw = sio.loadmat(pathTS)      
dataTSArr = dataTSRaw['data'][:, 0]     # 6498



dataTSDF = pd.DataFrame(dataTSArr, columns=['endMonthDate'])
dataTSDF['endMonth'] = dataTSDF.applymap(lambda x: x/100)
dataTSDFSort = dataTSDF.sort_values(by=['endMonth', 'endMonthDate'])
dataMonthTSDF = dataTSDFSort.drop_duplicates('endMonth', keep='last') 

dataEndMonDatTSArr = dataMonthTSDF.values[:, 0]


dataDic = {'endMonthDate': dataEndMonDatTSArr.reshape(len(dataEndMonDatTSArr), 1)}
sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/endMonthDate_arr.mat', dataDic)






 