#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 13:37:11 2017

@author: liushuanglong
"""

'''
#==============================================================================
# daily quote tradevolumes
#==============================================================================
'''



import numpy as np
import scipy.io as sio
import pandas as pd



pathCode = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
dataCode =  sio.loadmat(pathCode)
dataInnerCode = dataCode['data'].T[0]   # 3415
dataTraVolTemp = pd.DataFrame([], columns=dataInnerCode)

def dataTraVolYear(path):   
    
    dataRaw = sio.loadmat(path)     
    dataColTol = [dataRaw['col'][0][i][0] for i in range(dataRaw['col'].shape[1])]
    useLis = [dataColTol.index(i) for i in [u'TradingDay', u'InnerCode', u'TurnoverVolume']]
    dataCol = [dataColTol[i] for i in useLis]
    dataArr = dataRaw['data'][:, useLis]
    
    dataDFTol = pd.DataFrame(dataArr, columns=dataCol)
    
    dataDFUse = dataDFTol[dataDFTol[u'InnerCode'].isin(dataInnerCode)]
    
    dataDFUseSort = dataDFUse.sort_values(by=u'TradingDay')
    dataDFUseSort.set_index([u'TradingDay', u'InnerCode'], inplace=True)
    
    dataDF = dataDFUseSort[u'TurnoverVolume'].unstack()
    
    return dataDF


dataTraVol_1999 = dataTraVolYear('/home/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_1999_mat.mat')
dataTraVol_2004 = dataTraVolYear('/home/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_2004_mat.mat')
dataTraVol_2007 = dataTraVolYear('/home/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_2007_mat.mat')
dataTraVol_2011 = dataTraVolYear('/home/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_2011_mat.mat')
dataTraVol_2015 = dataTraVolYear('/home/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_2015_mat.mat')
dataTraVol_2016 = dataTraVolYear('/home/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_2016_mat.mat')
dataTraVol_3000 = dataTraVolYear('/home/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_3000_mat.mat')


dataTraVolTol = pd.concat([dataTraVolTemp, dataTraVol_1999, dataTraVol_2004, \
                       dataTraVol_2007, dataTraVol_2011, dataTraVol_2015, \
                       dataTraVol_2016, dataTraVol_3000])

    
    
# drop non tradingday data
# load data series
pathTS =  '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat'     
dataTSRaw = sio.loadmat(pathTS)      
dataTSArr = dataTSRaw['data'][:, 0]     # 6498


dataTraVol = dataTraVolTol.loc[dataTSArr].sort_index()

    
dataDic = {'colInnerCode': np.array(dataTraVol.columns), \
           'indexTime': np.array(dataTraVol.index).reshape(len(dataTraVol.index), 1), \
           'DailyQuote_TurnoverVolume': dataTraVol.values}
sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_TurnoverVolume_array.mat', dataDic)












