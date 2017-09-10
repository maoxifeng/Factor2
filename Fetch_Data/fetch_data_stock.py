# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 15:21:03 2017

@author: liusl
"""


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
def groupGet():
    
    pathCode = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
    dataCodeRaw = sio.loadmat(pathCode)
    dataCodeRaw.keys()
    dataCodeArr = dataCodeRaw['data']
    dataInnerCodeArr = dataCodeArr[:, 0]
    dataComCodeArr = dataCodeArr[:, 1] # 3415
    dataComCodeArr.shape
    dataCodeArr.shape
    # import secuCode
    pathCode = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/AStockCode_mat.mat'
    dataCodeRaw = sio.loadmat(pathCode)
    dataCodeRaw.keys()
    dataSecuCodeRaw = dataCodeRaw['secuCode']
    dataSecuCodeRaw.shape
    dataSecuCodeArr = np.array([dataSecuCodeRaw[i][0][0] for i in range(len(dataSecuCodeRaw))])
    dataMarRaw = dataCodeRaw['data'][:, 2]
    data90Arr = dataSecuCodeArr[dataMarRaw==90]   # 2064 counts
    data83Arr = dataSecuCodeArr[dataMarRaw==83]    # 1378 counts
    dataCodeRaw['data'].shape
    
    df1 = pd.DataFrame(dataCodeArr, columns = ['inner', 'com'])
    df2 = pd.DataFrame(dataCodeRaw['data'], columns = ['inner', 'com', 'market'])
    df2['secu'] = dataSecuCodeArr
    df3 = df2[df2['inner'].isin(dataInnerCodeArr)]
    df4 = df3.sort_values('secu')
    
    df_83 = df4[df4['market']==83]
    df_90 = df4[df4['market']==90]
    groDic = {'90': df_90['secu'].values, '83': df_83['secu'].values   }
    return groDic

data90Arr = groupGet()['90']   # 2051 counts

data90_1Arr = data90Arr[:300]
data90_2Arr = data90Arr[300: 600]
data90_3Arr = data90Arr[600:900]
data90_4Arr = data90Arr[900:1200]
data90_5Arr = data90Arr[1200:1500]
data90_6Arr = data90Arr[1500:1800]
data90_7Arr = data90Arr[1800:]   # 

data83Arr = groupGet()['83']   # 1364 counts
data83_1Arr = data83Arr[:300]         # 
data83_2Arr = data83Arr[300:600]     # 
data83_3Arr = data83Arr[600:900]     # 
data83_4Arr = data83Arr[900:1200]     # 
data83_5Arr = data83Arr[1200:]     # 


# =========== fetch data =================


#
#time_period = [(20110101, 20111231), (20120101, 20121231), (20130101, 20131231), (20140101, 20141231), 
#               (20150101, 20151231), (20160101, 20161231)]
time_period = [(20170101, 20171231)]

 
#%%              
#security_list = range(10000627,10000815)
def dataGet(dataarray):
    
    if set(dataarray).issubset(set(data83Arr)):
        dataFullLis = map(lambda x: x+'.sh', dataarray)    # 83 shanghai, 1011
        print 'sh_1011'
    else:
        dataFullLis = map(lambda x: x+'.sz', dataarray)    # 90 shenzhen, 1012
        print 'sz_1012'
    for ss, secu_full in enumerate(dataFullLis):
        secu = secu_full[:-3]
        print secu,
        
        if secu_full[-2:] == 'sh':
            save_subdir = './1011/' + secu + '/'
        else:
            save_subdir = './1012/' + secu + '/'
            
        if not os.path.exists(save_subdir):
            os.makedirs(save_subdir)
            
        time1 = time.time()
        for tt, timeper in enumerate(time_period):
            save_name = save_subdir + str(timeper[0]/10000) + '_' + secu + '.mat'
            
            if os.path.exists(save_name):
                continue                            
#            print time.asctime(time.localtime(time.time()))[11:19],        
            print time.strftime("%H:%M:%S", time.localtime()),     
            data = gfd.get_day_tick(secu_full, timeper, merge=True)
            print (tt+1, timeper[0]/10000),    
            
            if data is not None:
                timeTemp = map(lambda x: int(x.strftime('%Y%m%d%H%M%S')), data.index.tolist())
                data.reset_index(inplace=True)
                data.drop(data.columns[[1, 7]], axis=1, inplace=True)        
                data.iloc[:, 0] = timeTemp
                dataArr = data.values
                col = np.zeros((1, len(data.columns)), dtype=object)
                for i, j in enumerate(data.columns):
                    col[0][i] = np.array([j])
                
                dataDic = {'col': col, 'data':dataArr}
                
                sio.savemat(save_name, dataDic)
                print 'done',
        if tt == (len(time_period)-1):
            
            time2 = time.time()
            print '\n',
            print '%.2fs used'%(time2-time1),
            print secu + 'completed\n'
    if ss == len(dataFullLis) - 1:
        print 'group completed'
    #        data.to_hdf(save_name,'data') 
    

# 83  1011
#dataGet(data83_1Arr) #  completed
#dataGet(data83_2Arr) # completed
#dataGet(data83_3Arr)  # completed
#dataGet(data83_4Arr)   # completed
#dataGet(data83_5Arr) # already completed


# 90 1012

#dataGet(data90_1Arr)   # completed
#dataGet(data90_2Arr)   # completed
#dataGet(data90_3Arr)   # cs5 doing
#dataGet(data90_4Arr)   # completed
#dataGet(data90_5Arr)   # completed
#dataGet(data90_6Arr)   # completed
#dataGet(data90_7Arr)   # completed




#%%
# data get erro list

#dataDicEmp_000100_2011 = {'dataGetError':np.array([[np.array(['dataGetError'])]], dtype= object)}  # got it
#sio.savemat('./1012/000100/2011_000100.mat', dataDicEmp_000100_2011)  # got it




    

