#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:32:22 2017

@author: liushuanglong
"""

'''
#==============================================================================
# divide three groups: low(30), media(40), high(30), by ROE values(fical yearend data)
#==============================================================================
'''


import numpy as np
import scipy.io as sio
import pandas as pd
import cPickle as cp

#==============================================================================
# 1. calculate yearend ROE values
#==============================================================================

# load ROE 3D array data
pathROE = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_Total_ROE_YearDuration_mat.mat'
dataRaw = sio.loadmat(pathROE)
dataRaw.keys()
dataItemsArr = [dataRaw['axis1_itemNames'][0][i][0] for i in range(dataRaw['axis1_itemNames'].shape[1])]

# use ROE and ROE enddate
dataROEArr = dataRaw['LC_Total_ROE_YearDuration'][0]
dataROEEndDateArr = dataRaw['LC_Total_ROE_YearDuration'][1]

# time and companycode
dataTSArr = dataRaw['axis2_indexTime'][:, 0]   # 6498
dataComCodeArr = dataRaw['axis3_colCompanyCode'][0]   #3415


# create ROE and ROE enddate
dataROEDF = pd.DataFrame(dataROEArr, index=dataTSArr, columns=dataComCodeArr)
dataROEEndDateDF = pd.DataFrame(dataROEEndDateArr, index=dataTSArr, columns=dataComCodeArr)


# divide three groups
dataYearDupArr = map(lambda x: int(x)/10000, dataTSArr)
dataYearArr = np.unique(dataYearDupArr)  # total year


dataROEYearDF = pd.DataFrame(index=dataYearArr, columns=dataComCodeArr)
for year in dataYearArr:
    yearEndDate = (year-1)*10000+1231
    dateUseBool = (dataROEEndDateDF.index>(year*10000)) & (dataROEEndDateDF.index<=(year*10000+430))
    for code in dataComCodeArr:
        dataEndDateOCUseDF = dataROEEndDateDF[code][dateUseBool]
        if yearEndDate in set(dataEndDateOCUseDF):
            pubDateUse = dataEndDateOCUseDF[dataEndDateOCUseDF==yearEndDate].index[-1]
            dataROEYearDF.loc[year][code] = dataROEDF[code].loc[pubDateUse]
        else:
            dataROEYearDF.loc[year][code] = np.nan
    print year,

## save ROE yearend data
#cp.dump(dataROEYearDF, open('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROEYearEndDF.pkl', 'w'))


#==============================================================================
# 2. divide three groups
#==============================================================================

#dataROEYearDF = cp.load(open('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROEYearEndDF.pkl', 'r'))

dataROEYearUseDF = dataROEYearDF.dropna(how='all')   
dataYearUseLis = dataROEYearUseDF.index.tolist()       # 27


groupLowROEDic = {}
groupMedROEDic = {}
groupHigROEDic = {}
#groupSumROEDic = {}

groupAllROEDic = {}
#groupDifROEDic = {}
#dataROEYearDF.iloc[:10].quantile([0.3, 0.75], axis=1)
#dataROEYearDF.iloc[1].quantile([0.3, 0.75])
#
#dfpercent2 = dataROEYearDF.quantile([0.3, 0.75], axis=1).T   #  why? !!!
dfpercent = pd.DataFrame(index=dataYearUseLis, columns=[0.3, 0.7])
for year in dataYearUseLis:
    dfpercent.loc[year] = dataROEYearUseDF.loc[year].quantile([0.3, 0.7])
    
for year in dataYearUseLis:
    dataROEYearUseTemp = dataROEYearUseDF.loc[year]
    if len(dataROEYearUseTemp.dropna()) >= 100:  # keep stocks groups when counts >=100
        groupAllROEDic[year] = dataROEYearUseTemp.dropna().index.tolist()
        per = dfpercent.loc[year]
        groupLowROEDic[year] = dataROEYearUseTemp[dataROEYearUseTemp<=per[0.3]].index.tolist()
        groupMedROEDic[year] = dataROEYearUseTemp[(dataROEYearUseTemp>=per[0.3]) & (dataROEYearUseTemp<per[0.7])].index.tolist()
        groupHigROEDic[year] = dataROEYearUseTemp[dataROEYearUseTemp>=per[0.7]].index.tolist()
#    groupSumROEDic[year] = groupLowROEDic[year] + groupMedROEDic[year] + groupHigROEDic[year]
#    groupDifROEDic[year] = list(set(groupAllROEDic[year]) ^ set(groupSumROEDic[year]))

dataYearUseKeepLis = sorted(groupAllROEDic.keys())
threeGroupsDic = {'low': groupLowROEDic, 'median': groupMedROEDic, 'high':groupHigROEDic, 'year':dataYearUseKeepLis}

#cp.dump(threeGroupsDic, open('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/stoThreeGroupsByROE_Dic.pkl', 'w'))












