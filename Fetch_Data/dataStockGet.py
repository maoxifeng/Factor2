# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 09:50:50 2017

@author: liusl
"""


# ============ import modules =================
import gfunddataprocessor.gfunddataprocessor as gfd
import pandas as pd
import numpy as np
import scipy.io as sio
import os
import time
#from datetime import datetime

#import pdb
#pdb.set_trace()


# import secuCode
pathCode = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/AStockCode_mat.mat'
dataCodeRaw = sio.loadmat(pathCode)
dataCodeRaw.keys()
dataSecuCodeRaw = dataCodeRaw['secuCode']
dataSecuCodeRaw.shape
dataSecuCodeArr = np.array([dataSecuCodeRaw[i][0][0] for i in range(len(dataSecuCodeRaw))])
dataMarRaw = dataCodeRaw['data'][:, 2]

data90Arr = dataSecuCodeArr[dataMarRaw==90]   # 2064 counts

data90_1Arr = data90Arr[:300]
data90_2Arr = data90Arr[300: 600]
data90_3Arr = data90Arr[600:900]
data90_4Arr = data90Arr[900:1200]
data90_5Arr = data90Arr[1200:1500]
data90_6Arr = data90Arr[1500:1800]
data90_7Arr = data90Arr[1800:]   # 264 counts

data83Arr = dataSecuCodeArr[dataMarRaw==83]    # 1378 counts
data83_1Arr = data83Arr[:300]         # 
data83_2Arr = data83Arr[300:600]     # 
data83_3Arr = data83Arr[600:900]     # 
data83_4Arr = data83Arr[900:1200]     # 
data83_5Arr = data83Arr[1200:]     # 178 counts  # completed


# =========== fetch data =================

time_period = [(20110101, 20111231), (20120101, 20121231), (20130101, 20131231), (20140101, 20141231), 
               (20150101, 20151231)]
#time_period2 = [(20160101, 20161231), (20170101, 20171231)]

 
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


def dataGroupGet(groupstr):
    if groupstr == '90_1':
        dataGet(data90_1Arr)
    elif groupstr == '90_2':
        dataGet(data90_2Arr)
    elif groupstr == '90_3':
        dataGet(data90_3Arr)
    elif groupstr == '90_4':
        dataGet(data90_4Arr)
    elif groupstr == '90_5':
        dataGet(data90_5Arr)
    elif groupstr == '90_6':
        dataGet(data90_6Arr)
    elif groupstr == '90_7':
        dataGet(data90_7Arr)
    elif groupstr == '83_1':
        dataGet(data83_1Arr)
    elif groupstr == '83_2':
        dataGet(data83_2Arr)
    elif groupstr == '83_3':
        dataGet(data83_3Arr)
    elif groupstr == '83_4':
        dataGet(data83_4Arr)
    elif groupstr == '83_5':
        dataGet(data83_5Arr)


    



    

