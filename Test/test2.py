# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:03:13 2017

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




data_list2 = gfd.get_day_tick('000502.sz', (20160101, 20161231), merge=True)

data1 = gfd.get_day_tick('000100.sz', (20110101, 20111231), merge=True)

dataDicEmp = {'dataError':np.array([[np.array(['dataError'])]], dtype= object)}



time_period = [(20110101, 20111231), (20120101, 20121231), (20130101, 20131231), (20140101, 20141231), 
               (20150101, 20151231), (20160101, 20161231), (20170101, 20171231)]

for tt, timeper in enumerate(time_period):
    print tt, timeper                      

time2 = time.time()
time1 = time.time()

time.ctime()

time.localtime()
time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time1)) 
time.strftime("%H:%M:%S", time.localtime()) 
date1 = datetime.now()

type(time.asctime(time.localtime(time.time())))

type(time.localtime(time.time()))

date1.strftime('%Y%m%d%H:%M:%S')
str(date1)

print '%.2fs used'%(time1-time2),
print 'ee'


os.makedirs('./1011/' + '600009')
os.mkdir('./1013/' + '600010')


os.listdir('./1011/' + '600001')

os.path.exists('./1011/' + '600005')


print str((2, 3))

aa = os.path.split('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/ROEExposure100day.pkl')

aa[0]
aa[1]








