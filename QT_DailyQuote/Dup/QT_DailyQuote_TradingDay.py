#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 10:17:14 2017

@author: liushuanglong
"""


import numpy as np
import scipy.io as sio
import pandas as pd

pathDayA = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/alltdays_mat.mat'
pathDayL = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_TradingDayRaw_mat.mat'
pathWind = '/home/liushuanglong/MyFiles/Wind/datelist/datelist.mat'

dataTraDayRawA = sio.loadmat(pathDayA)
dataTraDayRawL = sio.loadmat(pathDayL)
dataTraDayRawW = sio.loadmat(pathWind)


dataTraDayArrA = dataTraDayRawA['data'][:, 0]
dataTraDayArrL = dataTraDayRawL['indexTime'][:, 0]
dataTraDayArrW = dataTraDayRawW['datelist'][:, 0]


dataTraDaySetA = set(dataTraDayArrA)
dataTraDaySetL = set(dataTraDayArrL)
dataTraDaySetW = set(dataTraDayArrW)

dataTraDaySetA.issubset(dataTraDaySetL)   # True
dataTraDaySetA.issubset(dataTraDaySetW)



dataTraDayDif = dataTraDaySetL - dataTraDaySetA
dataTraDayDifW = dataTraDaySetW - dataTraDaySetA


dataTraDayDifLis = sorted(list(dataTraDayDif))

dataTraDayDifLisInd = [(i, day) for i , day in enumerate(dataTraDayDifLis)]

dataTraDayDifLisStr = [str(day) for day in dataTraDayDifLis]
























