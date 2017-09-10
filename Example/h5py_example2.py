# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 16:36:41 2017

@author: liusl
"""

import h5py
import numpy as np
import pandas as pd
import scipy.io as sio


aa = sio.loadmat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/ROE_HS300_StoFree_FMExposure_250RDs_array.mat')
aa.keys()
key = aa['arrKey']

key
file1 = h5py.File('exa1.hdf5', 'w')

df6 = pd.DataFrame(aa[key[0]], index=aa[key[1].strip()][:, 0], columns=aa[key[2].strip()][0])
df7 = df6.head()
df6.to_hdf('df6.h5py', 'df6')

file2 = h5py.File('df6.h5py', 'r')
file2.keys()
file2.close()

aa = file2['df6']
type(aa)

df9   = pd.read_hdf('df6.h5py')

df8

file4 = h5py.File('df6.h5py', 'r+')
file4.keys()


ff = file4['df6']
file4['df6'] = 
type(ff)
file4.create_group('/df0/')
df77 = file4.create_group('df77')
type(df77)
df77.keys()
df77.create_dataset('df777', data=df7)

file4['df999'] = df6.iloc[:, :5]

type(file4['df999'])

gg = file4['df0']
type(gg)
file4.close()
#cp.dump(df6, open('df6.pkl', 'w'))



bb = aa[key[1].strip()]
co=aa[key[2].strip()]


file1.create_dataset('arr', data=aa[key[1]])
file1.create_dataset('inde', data=aa[key[0]])
file1.create_dataset('colcode', data=aa[key[4]])
file1.create_dataset('key', data=['aa', 'bb', 'cc'])
file1.keys()
file1.close()


file3 = h5py.File('exa1.hdf5', 'r+')
file3.keys()
file3.create_dataset('df6', data=df6)
file3['df66'] = df6




df7 = file3['df66'][:]
type(df7)
type(file3['key'])
file3['colcode'][:]

file3.close()


type(cc)
import cPickle as cp

cp.dump(aa, open('exa1.pkl', 'w'))




#aaa = cp.load(open('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/ROE_FormatValuesDic.pkl', 'r'))


bb = sio.loadmat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/ROE_FormatValues_3DArray_arr.mat')
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/ROE_FormatValues_3DArray_arr.mat', bb)

cp.dump(bb, open('aawfwf.pkl', 'w'))


df2 = pd.DataFrame(np.array([[np.nan, 2, np.nan, 0], [3, 4, np.nan, 1], [np.nan, np.nan, np.nan, 5]]), index = [2, 1, 1], columns=['A','E', 'C','D'])


df2.to_hdf('df2.h5', 'afw')

df3 = h5py.File('df2.h5', 'r')
df3.close()
df3.keys()

df5 = pd.read_hdf('df2.h5')
df4 = df3['afw']

df4[()]