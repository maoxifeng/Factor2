#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 15:33:17 2017

@author: liushuanglong
"""

import cPickle as cp



data = range(100)

cp.dump(data, open("data.pkl", "w")) 
data1 = cp.load(open('data.pkl', 'r'))


data_string = cp.dumps(data)
data2 = cp.loads(data_string)















