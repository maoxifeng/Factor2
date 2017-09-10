# -*- coding: utf-8 -*-


import numpy as np
import scipy.io as sio
import pandas as pd


# function
def MarketReturn(path):
    dataRaw = sio.loadmat(path)  
    dataColTol = [dataRaw['col'][0][i][0] for i in range(dataRaw['col'].shape[1])]
    dataCol = [dataColTol[i] for i in [0, 3, 5]]
    dataArr = dataRaw['data'][:, [0, 3, 5]]
    dataDF = pd.DataFrame(dataArr, columns=dataCol)
    dataDF_HS300 = dataDF[(dataDF[u'InnerCode']) == 3145]  # select HS300 data
    dataDF_HS300.reset_index(drop = True, inplace = True)    
    dataDF_HS300.fillna(method='ffill', inplace=True)
    data_HS300= dataDF_HS300[[u'TradingDay', u'ClosePrice']]
    return data_HS300


Return_HS300_3145_2009 = MarketReturn('/data/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2009_mat.mat')
Return_HS300_3145_2012 = MarketReturn('/data/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2012_mat.mat')
Return_HS300_3145_2014 = MarketReturn('/data/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2014_mat.mat')
Return_HS300_3145_2016 = MarketReturn('/data/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_2016_mat.mat')
Return_HS300_3145_3000 = MarketReturn('/data/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/QT_IndexQuote_3000_mat.mat')

Return_HS300_3145_2009_to_3000 = pd.concat([Return_HS300_3145_2009, Return_HS300_3145_2012, \
                                            Return_HS300_3145_2014, Return_HS300_3145_2016, \
                                            Return_HS300_3145_3000], ignore_index=True)


##%%
#dup = Return_HS300_3145_2009_to_3000[Return_HS300_3145_2009_to_3000['TradingDay'].duplicated()].set_index('TradingDay')
#dup2 = Return_HS300_3145_2009_to_3000.set_index('TradingDay').loc[dup.index]
#dup3 = dup2.drop_duplicates('ClosePrice')

dataCloseHS300S = Return_HS300_3145_2009_to_3000.drop_duplicates(u'TradingDay')

#dataCloseHS300N = Return_HS300_3145_2009_to_3000[Return_HS300_3145_2009_to_3000[u'ClosePrice'].notnull()]
dataCloseHS300 = dataCloseHS300S.set_index(u'TradingDay').sort_index()

pathTS =  '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat'     
dataTSRaw = sio.loadmat(pathTS)      
dataTSArr = dataTSRaw['data'][:, 0]     # 6498

benchmark_20170717 = dataCloseHS300.reindex(dataTSArr, method='ffill')


colLis = benchmark_20170717.columns.tolist()
colArr = np.zeros((1, len(colLis)), dtype=object)
for i, j in enumerate(colLis):
    colArr[0][i] = np.array([j])


indexTimeDouLis = map(lambda x: float(x),  dataTSArr)

indexTime = np.array([indexTimeDouLis]).T

dataDic = {'colNames': colArr, \
           'indexTime': indexTime, \
           'Benchmark_20170717': benchmark_20170717.values}
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/Benchmark_20170717.mat', dataDic)
    