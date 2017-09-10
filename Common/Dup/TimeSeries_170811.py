# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 16:27:52 2017

@author: liusl
"""
import numpy as np
import scipy.io as sio
import pandas as pd


path1 = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat'
path2 = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/dateSer2017.mat'

dataRaw1 = sio.loadmat(path1)
dataRaw1.keys()
dataArr1 = dataRaw1['dateSeries']
dataRaw2 = sio.loadmat(path2)
dataArr2 = dataRaw2['dateSer2017']

dataArr_16 = dataArr1[dataArr1<20170000]

dateSeries_2017 = np.concatenate((dataArr_16, dataArr2.T[0]))

dataDic = {'dateSeries_170811': dateSeries_2017}

sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/dateSeries_170811.mat', dataDic)