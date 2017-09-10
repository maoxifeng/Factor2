#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 14:30:56 2017

@author: liushuanglong
"""

import h5py
import numpy as np
import pandas as pd

f = h5py.File("mytestfile.hdf5", "w")
arr1 = np.random.randn(5, 4)

#dset = f.create_dataset("mydataset", (100,), dtype='i')

dset[...] = np.arange(100, 200)
dset[0:100:10]

dset.name
f.name

grp = f.create_group("subgroup")
dset2 = grp.create_dataset("another_dataset", (50,), dtype='f')
dset2.name

dset3 = f.create_dataset('subgroup2/dataset_three', (10,), dtype='i')
dset3.name

dataset_three = f['subgroup2/dataset_three']

for name in f:
    print name

"mydataset" in f
'subgroup' in f
"another_dataset" in f
"subgroup/another_dataset" in f

dset.attrs['temperature'] = 99.5   # ???






















