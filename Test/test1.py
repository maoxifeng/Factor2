#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 15:02:09 2017

@author: liushuanglong
"""

#import pymssql
import numpy as np
import scipy.io as sio
import pandas as pd
import cPickle as cp
import os
import time

aa = time.localtime()
time.sleep(10)
bb = time.localtime()


aa = time.time()
time.sleep(10)
bb = time.time()
cc = time.localtime(bb-aa)

time.strftime("%H:%M:%S", bb-aa)


a= 2; b=3
def aa(a=1, b=2):
    print 'a', a, 'b', b
    return None     
        
        
f = aa(a=b, b=a)
aa(a=a, b=b)

os.path.exists('./1011/600000/2011_600006.mat')

os.path.isdir('./1011/600000/')
os.path.isfile('./1011/600000/2011_600000.mat')


print 'aew%.2fs\n'%2.3
print 'aew%.2fs\n\n,'%2.3,

print 'efs\tllll'   # 制表
print 'efs       \tllll'   # 制表

print '\n'            # 换行
print  'efwpppp'    # 回车

print  'efw\rpppp',    # 回车
print '\nddd'
print 'ddd','e'


a=np.array([3,2,1])
a=np.array([4,0,5])
b=np.array([[11,22,33]])
c=np.array([44,55,66])

print 'a', a, 'b', b



#pathNF = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ReturnOnEquity/ROE_HS300_FMReturn_array.mat'
#dataNFRaw = sio.loadmat(pathNF)  
#dataNFColTol = [dataNFRaw['colNames'][0][i][0] for i in range(dataNFRaw['colNames'].shape[1])]
#dataNFColTol = [i[0] for i in dataNFRaw['colNames'][0]]
#dataNFRaw['colNames'][0, 1][0]


a=np.array([[1,2,3]])
b=np.array([[11,22,33]])
c=np.array([[44,55,66]])
d = np.vstack((a, b, c))


cha = 'awwwwwwwfwfwfwwfwfwfw'
a = np.random.randn(4, 3)
#
#col1 = ['TradingDay','XGRQ','ChangePCT','ClosePrice']
#col2 = ['TradingDay','XGRQ','ChangePCT','ClosePrice','HighPrice']
#
aa = np.random.randn(3, 2, 4)
dicaa = {3: [1, 2], 2: 'a'}
dicaa = {3: [1, 2]}
cc = np.array(['a', 'b', 'c'])
aa = np.array([1,2,3,5,5,5]) 
bb = np.array([[1,2,3,5,5,5], [1,1,1,2,2,2]])
aa = np.arange(20)
cc = np.ones((3, 4, 5))
df1 = pd.DataFrame(np.random.randn(5, 4), index=[1., 1., 3., 3., 5.])
df2 = pd.DataFrame(np.random.randn(5, 4))
df3 = pd.Series(range(5))
arr1 = np.array([])
df4 = pd.DataFrame(np.random.randn(5, 4), index=[5., 5., 3., 3., 1.], columns=[1, 15, 7, 9])
df5 = pd.DataFrame(np.random.randn(3, 6), index=[2,7,9], columns=[20, 4, 10, 0, 7, 1])
df5 = pd.Series(range(10, 6, -1), index=[5., 5., 3., 1.])
arr6 = np.array([[7,2,3,4,6,5], [1,2,8,0,2,3], [3,3,7,1,0,4]])
df6 = pd.DataFrame(np.array([[7,2,3,4,6,5], [1,2,8,0,2,3], [3,3,7,1,0,4]]).T, index = [6, 3, 1, 2,2,4], columns=[u'Y', u'M', u'N'])
df8 = pd.DataFrame(columns=[u'Y', u'M', u'N'])
df7 = pd.DataFrame(index = [2, 3, 6, 9])

df5 = pd.DataFrame(columns=['A'])
arr2 = np.array([[np.nan, 2, np.nan, 0], [3, 4, np.nan, 1], [np.nan, np.nan, np.nan, 5]])
df1 = pd.DataFrame(np.array([[np.nan, 2, np.nan, 0], [3, 4, np.nan, 1], [np.nan, np.nan, np.nan, 5]]), index = [6, 3, 1], columns=['A','B', 'C','D'])
df2 = pd.DataFrame(np.array([[np.nan, 2, np.nan, 0], [3, 4, np.nan, 1], [np.nan, np.nan, np.nan, 5]]), index = [10, 11, 9], columns=['A','E', 'C','D'])
df3 = pd.DataFrame(columns=[u'E', u'M', u'N'])
df2 = pd.DataFrame(np.array([[1, 3]]).T, columns=[u'E'])
df4 = pd.DataFrame(columns=[u'A'])
df7 = pd.DataFrame([[6, 3, 1]], columns=[u'E', u'M', u'N'])
df8 = pd.DataFrame([[2, 4, 6]],columns=[3, 5, 7])
df8

cc = np.array([[np.nan, 2, np.nan, 0], [3, 4, np.nan, 1], [np.nan, np.nan, np.nan, 5]])
df8 = pd.DataFrame()
#df2 = pd.DataFrame([1, 3, 3, 3, 5], index=[1., 1., 3., 3., 5.])
#
#a = np.random.randn(4, 1)
#b = np.random.randn(5, 1)
#df1 = pd.DataFrame(index = a[:, 0], columns=b[:, 0])
#df2 = pd.DataFrame(index=col2, columns=col1)
#
#a = np.array([[1, 2], [3, 3]])
#b = np.array([[2, 2], [1, 3]])
#
#
#
#df3 = pd.concat([df1, df2])
#
#
#arr1 = np.random.randn(4, 6)
#df1 = pd.DataFrame(arr1)
#
#df1.iloc[[0, 3], [1, 4]] = np.nan
#
#df1.iloc[[1, 3]][[2, 4]]
#
#df1[df1.isnull().values == True].drop_duplicates()
#
#
#arr2 = np.random.randn(5, 5)
#
#df2 = pd.DataFrame(arr2)
#
#
#arr3 = np.random.randn(4, 7)
#
#df3 = pd.DataFrame(arr3)
#




#
#
#
#net = cp.load(open("/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalData/LC_IncomeStatementNew_Total_NetProfit_YearDuration_DicUse.pkl", "r")) 
#net2 = cp.load(open("/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalData/LC_IncomeStatementNew_NetProfit_YearDuration_Dic.pkl", "r")) 
#net32 = cp.load(open("/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_Total_ROE_YearDuration_Dic.pkl", "r")) 
#
#
#

#aa = dataNetProfitDic[3]


def test1(a, b, c=(1,'e'), d='a'):
    print a, b, c, d


def test2(a, b, c=(1,'e'), d=[2,3]):
    d.append('d')
    print a, b, c, d


def test3(a, b, c=(1,'e'), d='a', *args):
    print a, b, c, d, args


def test4(a, b, c=(1,'e'), d='a', *args, **kw):
    print a, b, c, d, args, kw


test1('a', 2, 3)
test1('a', 2, 'b', 3)

lis1 = [['a'], 2, 'b', 'e', [1, 3]]
lis2 = (['a'], 2, 'b', 'e', [1, 3])
test3(*lis1)
test3(*lis2)
test3(['a'], 2, 'b', 'e', [1, 3], (3, 4))
test4(['a'], 2, 'b', 'e', f = [1, 3], u = (3, 4))
lis4 = {'a':'aa', 'b': 'bb', 'g': 'dd', 'h':'ff'}
test4(*lis4)
test4(**lis4)

c = [(2,1)]
c.append(0)



def char2num(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]

map(char2num, '63432')


aa = 1
if aa>0:
    aa = 2
c = aa + 1

import statsmodels.api as sm

xx = np.array([[1, 2, np.nan, 4, 5, np.nan, 7]]).T
xx = np.array([[1, 2, 3, 4, 5, 6, 7]]).T
yy = 2 * np.arange(1,8)
yy = 2 * np.arange(1,8).reshape(7, 1)
xx = sm.add_constant(xx)

model = sm.OLS(yy,xx)
results = model.fit()
results.params

#
#dataROEYearDF = cp.load(open('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROEYearEndDF.pkl', 'r'))
#dfpercent2 = dataROEYearDF.quantile([0.3], axis=1)  #  why? !!!
#
#







