#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 18:11:19 2017

@author: liushuanglong
"""


import numpy as np
import pandas as pd
import scipy.io as sio
import cPickle as cp



# load code
pathCode = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
dataCode =  sio.loadmat(pathCode)
dataComCode = dataCode['data'].T[1]   # 3415



# load non financial balance statement_new data
pathNF = '/home/liushuanglong/MyFiles/Data/JYDB2/LC_BalanceSheetNew/LC_BalanceSheetNew_mat.mat'
dataNFRaw = sio.loadmat(pathNF)  
dataNFColTol = [dataNFRaw['col'][0][i][0] for i in range(dataNFRaw['col'].shape[1])]
dataNFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'TotalShareholderEquity', u'DeferredTaxAssets', \
                   u'EPreferStock']
dataNFColUseInd = [dataNFColTol.index(i) for i in dataNFColUseLis]
dataNFBalanceTolArr = dataNFRaw['data'][:, dataNFColUseInd]


# dataframe, select by company code and mark
dataNFBalanceTolDF = pd.DataFrame(dataNFBalanceTolArr, columns=dataNFColUseLis)    # 789264
dataNFBalanceUseDF = dataNFBalanceTolDF[dataNFBalanceTolDF[u'CompanyCode'].isin(dataComCode)]  # 544258
dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceUseDF[u'Mark'].isin([1, 2])]      # 287129
dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceUseDF[u'TotalShareholderEquity'].notnull()]    #287097
dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceUseDF[u'TotalShareholderEquity']!=0]    #287075


# load financial balance statement_new data
pathF = '/home/liushuanglong/MyFiles/Data/JYDB2/LC_FBalanceSheetNew/LC_FBalanceSheetNew_mat.mat'
dataFRaw = sio.loadmat(pathF)  
dataFColTol = [dataFRaw['col'][0][i][0] for i in range(dataFRaw['col'].shape[1])]
dataFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'TotalShareholderEquity', u'DeferredTaxAssets', \
                  u'EPreferStock']
dataFColUseInd = [dataFColTol.index(i) for i in dataFColUseLis]
dataFBalanceTolArr = dataFRaw['data'][:, dataFColUseInd]


# dataframe, select by company code and mark
dataFBalanceTolDF = pd.DataFrame(dataFBalanceTolArr, columns=dataFColUseLis)    # 23090
dataFBalanceUseDF = dataFBalanceTolDF[dataFBalanceTolDF[u'CompanyCode'].isin(dataComCode)]  # 7902
dataFBalanceUseDF = dataFBalanceUseDF[dataFBalanceUseDF[u'Mark'].isin([1, 2])]      # 4438
dataFBalanceUseDF = dataFBalanceUseDF[dataFBalanceUseDF[u'TotalShareholderEquity'].notnull()]    #4428
dataFBalanceUseDF = dataFBalanceUseDF[dataFBalanceUseDF[u'TotalShareholderEquity']!=0]    #4428





# look for duplicated companycode
dataNFComCodeUse = np.unique(dataNFBalanceUseDF[u'CompanyCode']) # used company code, income:3364 counts  banlenc:3363
dataFComCodeUse = np.unique(dataFBalanceUseDF[u'CompanyCode'])   # used company code, income:61 counts, balence: 61


#dataDupComCodeSet = set(dataNFComCodeUse) & set(dataFComCodeUse)
#dataTolComCodeSet = set(dataNFComCodeUse) | set(dataFComCodeUse)
dataDupComCode = sorted(set(dataNFComCodeUse) & set(dataFComCodeUse))   # duplicated code  income:11,  balence: 10
dataTolComCode = sorted(set(dataNFComCodeUse) | set(dataFComCodeUse))   # total code use income:3414, balence:3414

dataNFEComCode = sorted(set(dataNFComCodeUse) - set(dataFComCodeUse))   # NF effective code income:3353, balence:3353    
dataFEComCode = sorted(set(dataFComCodeUse) - set(dataNFComCodeUse))    # F effective code  income:50, balence:51




# sort by company code , published date, end date, mark
dataNFBalanceUseDFSor = dataNFBalanceUseDF.sort_values(by=[u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark'], \
                                                     ascending=[True, True, True, False])
dataFBalanceUseDFSor = dataFBalanceUseDF.sort_values(by=[u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark'], \
                                                   ascending=[True, True, True, False])


# conbine financial and non financial balance data to one dic 
dataNFBalanceUseDFInd = dataNFBalanceUseDFSor.set_index([u'CompanyCode', u'InfoPublDate'])
dataFBalanceUseDFInd = dataFBalanceUseDFSor.set_index([u'CompanyCode', u'InfoPublDate'])

dataTolBalanceDic={}   # 3414
for code in dataTolComCode:
    if code in dataDupComCode:
        dataNFBalanceDFTemp = dataNFBalanceUseDFInd.loc[code]
        dataFBalanceDFTemp = dataFBalanceUseDFInd.loc[code]
        dataDupBalanceDFTemp = pd.concat([dataNFBalanceDFTemp, dataFBalanceDFTemp]).sort_index()
        dataTolBalanceDic[code] = dataDupBalanceDFTemp
    elif code in dataNFEComCode:
        dataTolBalanceDic[code] = dataNFBalanceUseDFInd.loc[code]
    else:
        dataTolBalanceDic[code] = dataFBalanceUseDFInd.loc[code]



# load single code income data , already calculated net profit
dataTolIncomeDic = cp.load(open("/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalData/LC_IncomeStatementNew_Total_NetProfit_YearDuration_DicUse.pkl", "r")) 



                
# create a dic contains the ROE data,  calculate the ROE
dataTolROEDic = {}
for number, code in enumerate(dataTolComCode):
    dfIncomeOneCode = dataTolIncomeDic[code]                              # df one code    
    dfBalanceOneCode = dataTolBalanceDic[code]                              # df one code    
    
    pubDateOneCodeIncomeLis = np.unique(dfIncomeOneCode.index).tolist()
    pubDateOneCodeBalanceLis = np.unique(dfBalanceOneCode.index).tolist()
    pubDateOneCodeLis = np.unique(pubDateOneCodeIncomeLis + pubDateOneCodeBalanceLis).tolist()
    pubDateFirstInd = pubDateOneCodeLis.index(pubDateOneCodeIncomeLis[0])
    dfROEOneCode = pd.DataFrame([], columns=[u'EndDate', u'IncomeMark', u'BalanceMark',  u'ReturnOnEquity'])    # contain the data we used
    
    for day in pubDateOneCodeLis[pubDateFirstInd:]:
        dfBalanceOneCodeDaySort = dfBalanceOneCode.loc[:day].sort_values(by=[u'EndDate', u'Mark'], ascending=[True, False])
        dfIncomeOneCodeUse = dfIncomeOneCode.loc[:day]
        if dfIncomeOneCodeUse.iloc[-1][u'EndDate'] in dfBalanceOneCodeDaySort[u'EndDate'].values:
            dfBalanceOneCodeDay = dfBalanceOneCodeDaySort[dfBalanceOneCodeDaySort[u'EndDate']\
                                                          ==dfIncomeOneCodeUse.iloc[-1][u'EndDate']].drop_duplicates('EndDate', keep='last') 
            dfBalanceOneCodeDay = dfBalanceOneCodeDay.fillna(0)   # fillna by 0
            dfROEOneCode.loc[day, u'EndDate'] = dfIncomeOneCodeUse.iloc[-1][u'EndDate']  # save enddate
            dfROEOneCode.loc[day, u'IncomeMark'] = dfIncomeOneCodeUse.iloc[-1][u'Mark']  # save income mark
            dfROEOneCode.loc[day, u'BalanceMark'] = dfBalanceOneCodeDay.iloc[-1][u'Mark'] # save balance mark

            dfROEOneCode.loc[day, u'ReturnOnEquity'] = dfIncomeOneCodeUse.iloc[-1][u'NetProfit'] / (dfBalanceOneCodeDay.iloc[-1][u'TotalShareholderEquity'] \
                            + dfBalanceOneCodeDay.iloc[-1][u'DeferredTaxAssets'] - \
                            dfBalanceOneCodeDay.iloc[-1][u'EPreferStock'])
    if number%10 ==0:
        print (number, code), 
        
    dataTolROEDic[code] = dfROEOneCode
    
# end for loop, and save ROE dic
cp.dump(dataTolROEDic, open("/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_Total_ROE_YearDuration_Dic.pkl", "w")) 


#==============================================================================
# save as 3 dimensional array            
#==============================================================================
        

# load data series
pathTS =  '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat'     
dataTSRaw = sio.loadmat(pathTS)      
dataTSArr = dataTSRaw['data'][:, 0]     # 6498
    

# load tol code pond
# already loaded : dataComCode

# tol code used : dataTolComCode        
#set(dataComCode) - set(dataTolComCode)       code not contained:155

# create a dic contain all effective date
dataROEDicTolTime = {}
for code in dataTolComCode:
    dataOneCodeTolDF = dataTolROEDic[code].sort_index()
    dataOneCodeTSRaw = dataOneCodeTolDF.index.tolist()
    dataOneCodeTSTol = sorted(set(dataTSArr) | set(dataOneCodeTSRaw))
    dataOneCodeUseDF = dataOneCodeTolDF.reindex(dataOneCodeTSTol, method='ffill').loc[dataTSArr]   # use effective time data
    dataROEDicTolTime[code] = dataOneCodeUseDF
    
   
# save netprofit as 3D array   , total codes
itemNames = [u'ReturnOnEquity', u'EndDate', u'IncomeMark', u'BalanceMark']
dataROEArr = np.zeros((len(itemNames), len(dataTSArr), len(dataComCode)))

dataROEValueDF = pd.DataFrame([], index=dataTSArr, columns=dataComCode)
dataROEEndDateDF = pd.DataFrame([], index=dataTSArr, columns=dataComCode)
dataROEIncomeMarkDF = pd.DataFrame([], index=dataTSArr, columns=dataComCode)
dataROEBalanceMarkDF = pd.DataFrame([], index=dataTSArr, columns=dataComCode)
for code in dataTolComCode:
    dataROEValueDF[code] = dataROEDicTolTime[code][itemNames[0]]
    dataROEEndDateDF[code] = dataROEDicTolTime[code][itemNames[1]]
    dataROEIncomeMarkDF[code] = dataROEDicTolTime[code][itemNames[2]]
    dataROEBalanceMarkDF[code] = dataROEDicTolTime[code][itemNames[3]]
#
## save as pkl
#
#dicROEPkl = {u'ReturnOnEquity': dataROEValueDF, u'EndDate': dataROEEndDateDF, u'IncomeMark':dataROEIncomeMarkDF, u'BalanceMark':dataROEBalanceMarkDF}
#cp.dump(dicROEPkl, open("/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_Total_ROE_YearDuration_4items_dic.pkl", "w")) 


    
# save netprofit in 3D array       
dataROEArr[0] = dataROEValueDF.values      # ROE values
dataROEArr[1] = dataROEEndDateDF.values    # end date
dataROEArr[2] = dataROEIncomeMarkDF.values      # income mark
dataROEArr[3] = dataROEBalanceMarkDF.values      # balance mark


itemNamesArr = np.zeros((1, len(itemNames)), dtype=object)
for i, j in enumerate(itemNames):
    itemNamesArr[0][i] = np.array([j])

dataDic = {'axis1_itemNames': itemNamesArr, \
           'axis2_indexTime': dataTSArr.reshape(len(dataTSArr), 1), \
           'axis3_colCompanyCode': dataComCode, \
           'LC_Total_ROE_YearDuration': dataROEArr}
           
sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_Total_ROE_YearDuration_arr.mat', dataDic)
                       




























