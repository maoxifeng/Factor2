# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


'''   square of market return daily difference, then do month sum, and calculate month delta  '''


import numpy as np
import scipy.io as sio
import pandas as pd




path = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Financial/Return_HS300_3145_2005_to_3000_array.mat'

dataRaw = sio.loadmat(path)  
dataColTol = [dataRaw['colNames'][0][i][0] for i in range(dataRaw['colNames'].shape[1])]

dataReturn = pd.DataFrame(columns = dataColTol)
dataReturn[dataColTol[0]] = dataRaw['indexTime'][:, 0]
dataReturn[dataColTol[1]] = dataRaw['Return_HS300_3145_2005_to_3000'][:, 0]

dataReturn[u'Month'] = map(lambda x: round(x, 0),  dataReturn[u'TradingDay']/100)

dataReturnMonth = dataReturn.set_index(u'Month')

MonthLis = dataReturn[u'Month'].drop_duplicates().tolist()
dataMVI = pd.DataFrame([], index = MonthLis, columns= ['sigma', 'deltaSigma'])


for Mon in MonthLis:
    sigVal = 0
    for j in range(len(dataReturnMonth.loc[Mon])-1):
        sigTep = (dataReturnMonth.loc[Mon, 'Return'].iloc[j+1] - dataReturnMonth.loc[Mon, 'Return'].iloc[j]) ** 2
        sigVal = sigVal + sigTep 
    dataMVI.loc[Mon, 'sigma'] = sigVal
    
for i in range(1, dataMVI.shape[0]):
    dataMVI['deltaSigma'].iloc[i] = dataMVI['sigma'].iloc[i] - dataMVI['sigma'].iloc[i-1]

        
#dataMVI.fillna(method='bfill', inplace=True)  # fill nan of the first line

dataMVI_HS300 = dataMVI.reset_index()
dataMVI_HS300.drop('sigma', axis=1, inplace=True)


colLis = dataMVI_HS300.columns.tolist()
colArr = np.zeros((1, len(colLis)), dtype=object)
for i, j in enumerate(colLis):
    colArr[0][i] = np.array([j])

dataDic = {'colNames': colArr, \
           'indexTime': dataMVI_HS300[colLis[0]].values.reshape(len(dataMVI_HS300[colLis[0]].values), 1), \
           'MarVolInn_HS300_3145_2005_to_3000': dataMVI_HS300[colLis[1:]].values}
sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Financial/MarVolInn_HS300_3145_2005_to_3000_array.mat', dataDic)
    
    












