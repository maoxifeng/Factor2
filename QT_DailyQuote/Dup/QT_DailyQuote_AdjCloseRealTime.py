#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 13:16:54 2017

@author: liushuanglong
"""


import numpy as np
import scipy.io as sio
import pandas as pd



pathDayA = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/alltdays_mat.mat'


dataTraDayRawA = sio.loadmat(pathDayA)
dataTraDayArrA = dataTraDayRawA['data'][:, 0]
dataTraDayLisA = dataTraDayArrA.tolist()

#pathClose = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_ClosePrice_mat.mat'
#dataCloseRaw = sio.loadmat(pathClose)
#dataColInnerCode = dataCloseRaw['colInnerCode'][0]
#dataIndexTime = dataCloseRaw['indexTime'][:, 0]
#dataClosePrice = dataCloseRaw['DailyQuote_ClosePrice_mat']
#
#dataDFCloseTol = pd.DataFrame(dataClosePrice, index=dataIndexTime, columns=dataColInnerCode)
#
#dataDFCloseReal = dataDFCloseTol.loc[dataTraDayLisA]
#
#
## save data
#dataDic = {'colInnerCode': np.array(dataDFCloseReal.columns), \
#           'indexTimeReal': np.array(dataDFCloseReal.index).reshape(len(dataDFCloseReal.index), 1), \
#           'DailyQuote_ClosePriceReal': dataDFCloseReal.values}
#sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_ClosePriceReal_array.mat', dataDic)



##
#pathAdFactor = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_RatioAdjustingFactor_mat.mat'
#
#dataAdFactorRaw = sio.loadmat(pathAdFactor)
#dataColInnerCode = dataAdFactorRaw['colInnerCode'][0]
#dataIndexTime = dataAdFactorRaw['indexTime'][:, 0]
#dataAdFactor = dataAdFactorRaw['RatioAdjustingFactor']
#
#dataAdFactorTol = pd.DataFrame(dataAdFactor, index=dataIndexTime, columns=dataColInnerCode)
#
#dataAdFactorReal = dataAdFactorTol.loc[dataTraDayArrA]
#
## save data
#dataDic = {'colInnerCode': np.array(dataAdFactorReal.columns), \
#           'indexTimeReal': np.array(dataAdFactorReal.index).reshape(len(dataAdFactorReal.index), 1), \
#           'RatioAdjustingFactorReal': dataAdFactorReal.values}
#sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_RatioAdjustingFactorReal_array.mat', dataDic)
#


pathAdjClosePrice = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_AdjClosePrice_mat.mat'


dataAdjClosePriceRaw = sio.loadmat(pathAdjClosePrice)
dataColInnerCode = dataAdjClosePriceRaw['colInnerCode'][0]
dataIndexTime = dataAdjClosePriceRaw['indexTime'][:, 0]
dataAdjClosePrice = dataAdjClosePriceRaw['DailyQuote_AdjClosePrice']

dataAdjClosePriceTol = pd.DataFrame(dataAdjClosePrice, index=dataIndexTime, columns=dataColInnerCode)

dataAdjClosePriceReal = dataAdjClosePriceTol.loc[dataTraDayArrA]   # drop wrong data, keep trading day close data

# save data
dataDic = {'colInnerCode': np.array(dataAdjClosePriceReal.columns), \
           'indexTimeReal': np.array(dataAdjClosePriceReal.index).reshape(len(dataAdjClosePriceReal.index), 1), \
           'AdjClosePriceReal': dataAdjClosePriceReal.values}
sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_AdjClosePriceReal_array.mat', dataDic)
















