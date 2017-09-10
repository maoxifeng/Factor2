# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:47:43 2017

@author: liusl
"""

import matlab.engine
import numpy as np
import scipy.io as sio
import pandas as  pd

eng = matlab.engine.start_matlab()
path1 = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/bond_10y_mat.mat'
path2 = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/bond_10y.mat'
bb = eng.load('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Benchmark_20170717.mat')
a = eng.load('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/MarVolInn_HS300_3145_2005_to_3000_array.mat')     
eng.quit()


