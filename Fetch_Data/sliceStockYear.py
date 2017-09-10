# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 10:43:35 2017

@author: liusl
"""

import numpy as np
import pandas as pd
import os
import time
import scipy.io as sio

pathSto = '/data/liushuanglong/MyFiles/Data/1012/000055/2012_000055.mat'
dataRaw = sio.loadmat(pathSto)
dataRaw.keys()
dataRaw['col']
dataArr = dataRaw[:, 1]

dataArrUse = np.zeros_like(dataArr)
dataArrUse[:, 0] = []

tp1 = [93000, 113000]
timeArr = np.zeros



