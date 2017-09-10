#! /usr/bin/env python

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


os.getcwd()  # get current working directory  
os.chdir('G:\\wd.python')  # change working directory 


os.path.exists()  

# =========== fetch data =================

#time_period = (20150209, 20161130)
time_period = (20150209, 20150210)
security_list = ['510050', '000016']
# 10000625
#security_list = range(10000627,10000815)

for secu in security_list:
    secu_full = str(secu)+'.sh'
    time1 = time.time()
    data_list2 = gfd.get_day_tick(secu_full, time_period, merge=False)
    time2 = time.time()
    print time2-time1
    save_subdir = './data6/sh_'+str(secu)+'/'
    
#    if not os.path.exists('./data/'):   
#        os.mkdir('./data4/')
    os.makedirs(save_subdir)
    for data in data_list2:
        current_date = data.index[0]
        data.drop([data.columns[ii] for ii in [0, 6]], axis=1, inplace=True)     
        timeTemp = map(lambda x: int(x.strftime('%Y%m%d%H%M%S')), data.index.tolist())
        data['time'] = timeTemp
        dataArr = data.values
        col = np.zeros((1, len(data.columns)), dtype=object)
        for i, j in enumerate(data.columns):
            col[0][i] = np.array([j])
            
        dataDic = {'col': col, 'data':dataArr}
        
        save_name = save_subdir+secu_full[-2:]+'_'+secu_full[:-3]+'_'+str(current_date.year*10000+current_date.month*100+current_date.day)+'.h5'
#        save_name =secu_full[-2:]+'_'+secu_full[:-3]+'_'+str(current_date.year*10000+current_date.month*100+current_date.day)+'.h5'
        sio.savemat(save_name, dataDic)
#        data.to_hdf(save_name,'data') 




