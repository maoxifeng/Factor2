#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 15:42:10 2017

@author: liushuanglong
"""


'''
#==============================================================================
# ROE factor return function
#==============================================================================
'''




import numpy as np
import scipy.io as sio
import pandas as pd


#==============================================================================
# 1. get datetime series, code numbers we used
#==============================================================================

pathTS =  '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat'     
dataTSRaw = sio.loadmat(pathTS)      
dataTSArr = dataTSRaw['data'][:, 0]     # 6498
dataTSDic = {'dataTSArr': dataTSArr}

pathCode = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
dataCodeRaw = sio.loadmat(pathCode)
dataCodeArr = dataCodeRaw['data']
dataInnerCodeArr = dataCodeArr[:, 0]
dataComCodeArr = dataCodeArr[:, 1]
dataCodeNumDic = {'dataInnerCodeArr': dataInnerCodeArr, 'dataComCodeArr': dataComCodeArr}

pathHS300Code = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/HS300StockCode_mat.mat'
dataHS300CodeRaw = sio.loadmat(pathHS300Code)
dataHS300CodeArr = dataHS300CodeRaw['data']
dataHS300InnerCodeArr = dataHS300CodeArr[:, 0]
dataHS300ComCodeArr = dataHS300CodeArr[:, 1]
dataHS300CodeIndArr = dataHS300CodeArr[:, 2]
#==============================================================================
# 2. get netprofit data
#==============================================================================

def netprofitGet():
    # load non financial income statement_new data
    pathNFIC = '/home/liushuanglong/MyFiles/Data/JYDB2/LC_IncomeStatementNew/LC_IncomeStatementNew_mat.mat'
    dataNFICRaw = sio.loadmat(pathNFIC)  
    dataNFICColTol = [dataNFICRaw['col'][0][i][0] for i in range(dataNFICRaw['col'].shape[1])]
    dataNFICColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'NetProfit']
    dataNFICColUseInd = [dataNFICColTol.index(i) for i in dataNFICColUseLis]
    dataNFIncomeTolArr = dataNFICRaw['data'][:, dataNFICColUseInd]
    
    
    # dataframe, select by company code and mark
    dataNFIncomeTolDF = pd.DataFrame(dataNFIncomeTolArr, columns=dataNFICColUseLis)    # 923302
    dataNFIncomeUseDF = dataNFIncomeTolDF[dataNFIncomeTolDF[u'CompanyCode'].isin(dataComCodeArr)]  # 667895
    dataNFIncomeUseDF = dataNFIncomeUseDF[dataNFIncomeUseDF[u'Mark'].isin([1, 2])]      # 293845
    dataNFIncomeUseDF = dataNFIncomeUseDF[dataNFIncomeUseDF[u'NetProfit'].notnull()]    #293805 
    
    
    # load financial income statement_new data
    pathFIC = '/home/liushuanglong/MyFiles/Data/JYDB2/LC_FIncomeStatementNew/LC_FIncomeStatementNew_mat.mat'
    dataFICRaw = sio.loadmat(pathFIC)  
    dataFICColTol = [dataFICRaw['col'][0][i][0] for i in range(dataFICRaw['col'].shape[1])]
    dataFICColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'NetProfit']
    dataFICColUseInd = [dataFICColTol.index(i) for i in dataFICColUseLis]
    dataFIncomeTolArr = dataFICRaw['data'][:, dataFICColUseInd]
    
    
    # dataframe, select by company code and mark
    dataFIncomeTolDF = pd.DataFrame(dataFIncomeTolArr, columns=dataFICColUseLis)    # 25283
    dataFIncomeUseDF = dataFIncomeTolDF[dataFIncomeTolDF[u'CompanyCode'].isin(dataComCodeArr)]  # 9550
    dataFIncomeUseDF = dataFIncomeUseDF[dataFIncomeUseDF[u'Mark'].isin([1, 2])]      # 4500
    dataFIncomeUseDF = dataFIncomeUseDF[dataFIncomeUseDF[u'NetProfit'].notnull()]    #4493
    
    
    # look for duplicated companycode
    dataNFICComCodeUse = np.unique(dataNFIncomeUseDF[u'CompanyCode'])             # used company code, 3364 counts
    dataFICComCodeUse = np.unique(dataFIncomeUseDF[u'CompanyCode'])             # used company code, 61 counts
    
    
    #dataDupComCodeSet = set(dataNFComCodeUse) & set(dataFComCodeUse)
    #dataTolComCodeSet = set(dataNFComCodeUse) | set(dataFComCodeUse)
    dataDupComCode = np.unique(list(set(dataNFICComCodeUse) & set(dataFICComCodeUse)))   # duplicated code  11
    dataTolComCode = np.unique(list(set(dataNFICComCodeUse) | set(dataFICComCodeUse)))   # total code use 3414
    
    dataNFEComCode = np.unique(list(set(dataNFICComCodeUse) - set(dataFICComCodeUse)))        # NF effective code  3353
    dataFEComCode = np.unique(list(set(dataFICComCodeUse) - set(dataNFICComCodeUse)))          # F effective code  50
    
    
    
    # sort by company code , published date, end date, mark
    dataNFIncomeUseDFSor = dataNFIncomeUseDF.sort_values(by=[u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark'], 
                                                         ascending=[True, True, True, False])
    dataFIncomeUseDFSor = dataFIncomeUseDF.sort_values(by=[u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark'], \
                                                       ascending=[True, True, True, False])
    
    
    # create  a dict , contain all code data
    dataNFIncomeUseDFInd = dataNFIncomeUseDFSor.set_index([u'CompanyCode', u'InfoPublDate'])
    dataFIncomeUseDFInd = dataFIncomeUseDFSor.set_index([u'CompanyCode', u'InfoPublDate'])
    
    
    dataTolIncomeDic={}   # 3414
    for code in dataTolComCode:
        if code in dataDupComCode:
            dataNFIncomeDFTemp = dataNFIncomeUseDFInd.loc[code]
            dataFIncomeDFTemp = dataFIncomeUseDFInd.loc[code]
            dataDupIncomeDFTemp = pd.concat([dataNFIncomeDFTemp, dataFIncomeDFTemp]).sort_index()
            dataTolIncomeDic[code] = dataDupIncomeDFTemp
        elif code in dataNFEComCode:
            dataTolIncomeDic[code] = dataNFIncomeUseDFInd.loc[code]
        else:
            dataTolIncomeDic[code] = dataFIncomeUseDFInd.loc[code]


    # create a new df dict
    dataTolIncomeDicUse = {}   
    for number, code in enumerate(dataTolComCode):    
        dfIncomeOneCode = dataTolIncomeDic[code]
        pubDateArr = np.unique(dfIncomeOneCode.index)              
        pubYearArr = np.unique([int(i)/10000 for i in pubDateArr])
        dfOneCodeUse = pd.DataFrame(columns=[u'NetProfit'])
        for year in pubYearArr:
            dateIndArr = np.where((pubDateArr>(year*10000)) & (pubDateArr<(year*10000+501)))[0]
            pubDateUseArr = pubDateArr[dateIndArr]  # array
            lastYearDate = (year-1) * 10000 + 1231
            if (len(dateIndArr) > 0) & (lastYearDate in dfIncomeOneCode.loc[pubDateUseArr, u'EndDate'].values):
                dfIncomOneCodeTemp = dfIncomeOneCode.loc[pubDateUseArr]   # is a df
                dfIncomOneCodeTemp = dfIncomOneCodeTemp[dfIncomOneCodeTemp[u'EndDate'] == lastYearDate].iloc[-1] # is a series
                dfOneCodeUse.loc[year, u'NetProfit'] = dfIncomOneCodeTemp[u'NetProfit']
        dataTolIncomeDicUse[code] = dfOneCodeUse
                
                
    return dataTolIncomeDicUse
#
#netprofitGettest = netprofitGet()
#netprofitGettestCode = netprofitGettest.keys()
#
#netEmpty = []  #  77 counts
#for code in netprofitGettestCode:
#    if netprofitGettest[code].size == 0:
#        netEmpty.append(code)

#==============================================================================
# 3. get equity data
#==============================================================================

def equityGet():
    
    
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
    dataNFBalanceUseDF = dataNFBalanceTolDF[dataNFBalanceTolDF[u'CompanyCode'].isin(dataComCodeArr)]  # 544258
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
    dataFBalanceUseDF = dataFBalanceTolDF[dataFBalanceTolDF[u'CompanyCode'].isin(dataComCodeArr)]  # 7902
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
    

    # create a new df dict
    dataTolBalanceUseDic = {}   
    for number, code in enumerate(dataTolComCode):    
        dfBalanceCode = dataTolBalanceDic[code]
        pubDateArr = np.unique(dfBalanceCode.index)              
        pubYearArr = np.unique([int(i)/10000 for i in pubDateArr])
        dfOneCodeUse = pd.DataFrame(columns=[u'equity'])
        for year in pubYearArr:
            dateIndArr = np.where((pubDateArr>(year*10000)) & (pubDateArr<(year*10000+501)))[0]
            pubDateUseArr = pubDateArr[dateIndArr]
            lastYearDate = (year-1) * 10000 + 1231
            if (len(dateIndArr) > 0) & (lastYearDate in dfBalanceCode.loc[pubDateUseArr, u'EndDate'].values):
                dfBalanceOneCodeTemp = dfBalanceCode.loc[pubDateUseArr]
                dfBalanceOneCodeTemp = dfBalanceOneCodeTemp[dfBalanceOneCodeTemp[u'EndDate'] == lastYearDate].iloc[-1, 2:]
                dfOneCodeUse.loc[year, u'equity'] = dfBalanceOneCodeTemp.sum()
        dataTolBalanceUseDic[code] = dfOneCodeUse

    return dataTolBalanceUseDic

#equityGetTest = equityGet()
#equityGetTestCode = equityGetTest.keys()
#
#emptyEquity = []   # 77 counts 
#for code in equityGetTestCode:
#    if equityGetTest[code].size == 0:
#        emptyEquity.append(code)

#comCodeUseTestLis = list(set(netprofitGettest.keys()) & set(equityGetTest.keys()))


#==============================================================================
# 4. calculate ROE 
#==============================================================================

def ROEDFGet():
    netprofitDic = netprofitGet()
    print 'netprofitDic completed'
    equityDic = equityGet()
    print 'equity completed'
    comCodeUseLis = list(set(netprofitDic.keys()) & set(equityDic.keys()))
    innerCodeUseArr = np.zeros_like(comCodeUseLis)
    
    # use innercode as columns names
    for i, j in enumerate(comCodeUseLis):
        innerCodeUseArr[i] = dataInnerCodeArr[dataComCodeArr == j][0]
    dfROE = pd.DataFrame()
    
    for i, code in enumerate(comCodeUseLis):
        netOneCodeDF = netprofitDic[code]
        equityOneCodeDF = equityDic[code]
        ROEOneCodeDF = pd.concat([netOneCodeDF, equityOneCodeDF], axis=1)
        if ROEOneCodeDF.size != 0:
            innerCode = innerCodeUseArr[i]
            ROEOneCodeDF[innerCode] = ROEOneCodeDF[u'NetProfit'] / ROEOneCodeDF[u'equity']  # use innercode as columns names
            dfROE = pd.concat([dfROE, ROEOneCodeDF[[innerCode]]], axis=1)
    return dfROE

ROEDFGetTest = ROEDFGet()
ROEDFGetTest.shape

#==============================================================================
# 5. seperate three groups by ROE 
#==============================================================================
def ROEThreeGroupsDicGet(Flag=0):

#    dataROEYearUseDF = ROEDFGet().dropna(how='all')   
    dataROEYearUseDF = ROEDFGetTest.dropna(how='all')   
    
    thrNum = 100
    
    if Flag == 1:
        dataROEYearUseDF = dataROEYearUseDF[dataHS300InnerCodeArr]
        dataROEYearUseDF = dataROEYearUseDF.dropna(how='all')
        thrNum = 20
    dataYearUseLis = dataROEYearUseDF.index.tolist()       # 27

    groupLowROEDic = {}
    groupMedROEDic = {}
    groupHigROEDic = {}
    groupAllROEDic = {}

    #dfpercent2 = dataROEYearDF.quantile([0.3, 0.75], axis=1).T   #  why? !!!
    dfpercent = pd.DataFrame(index=dataYearUseLis, columns=[0.3, 0.7])
    
    
    for year in dataYearUseLis:
        dfpercent.loc[year] = dataROEYearUseDF.loc[year].quantile([0.3, 0.7])
        
    for year in dataYearUseLis:
        dataROEYearUseTemp = dataROEYearUseDF.loc[year]
        if len(dataROEYearUseTemp.dropna()) >= thrNum:  # keep stocks groups when counts >=100
            groupAllROEDic[year] = dataROEYearUseTemp.dropna().index.tolist()
            per = dfpercent.loc[year]
            groupLowROEDic[year] = dataROEYearUseTemp[dataROEYearUseTemp<=per[0.3]].index.tolist()
            groupMedROEDic[year] = dataROEYearUseTemp[(dataROEYearUseTemp>=per[0.3]) & (dataROEYearUseTemp<per[0.7])].index.tolist()
            groupHigROEDic[year] = dataROEYearUseTemp[dataROEYearUseTemp>=per[0.7]].index.tolist()

    threeGroupsDic = {'low': groupLowROEDic, 'median': groupMedROEDic, 'high':groupHigROEDic, 'all':groupAllROEDic}
    return threeGroupsDic

#ROEThreeGroupsDicGetTest = ROEThreeGroupsDicGet()
ROE_HS300ThreeGroupsDicGetTest = ROEThreeGroupsDicGet(Flag=1)

#==============================================================================
# 6. calculate the ROE value-weighted stock return
#==============================================================================

def ROEReturnGet(Flag=0):    
    
## 6.1 load 3 stock groups by ROE, stoct daily returns, stock daily volumne, stock AFloats
 
    # load 3 stock groups by ROE
#    thrGroDic = ROEThreeGroupsDic()
    thrGroDic  = ROE_HS300ThreeGroupsDicGetTest      # test
    yearGroupLis = sorted(thrGroDic['low'].keys())
    
    ## load stoct daily returns
    pathReturn = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_mat.mat'
    dataReturnRaw = sio.loadmat(pathReturn)
    dataReturnArr = dataReturnRaw['DailyQuote_LogReturn']
    
    ## load stock daily volumne
    pathVol = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_TurnoverVolume_mat.mat'
    dataVolRaw = sio.loadmat(pathVol)
    dataVolArr = dataVolRaw['DailyQuote_TurnoverVolume']  # columns: inner code
    
    ## load stock AFloats
    pathAF = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_AFloats_mat.mat'
    dataAFloatsRaw = sio.loadmat(pathAF)
    dataAFloats3DArr = dataAFloatsRaw['LC_AFloats']
    dataAFloatsArr = dataAFloats3DArr[0]
    
## 6.2 calculate grouped ROE daily return
    # keep effective data
    dataInnerCodeUseArr = dataInnerCodeArr
    
    if Flag == 1:  # HS300 stock
        dataInnerCodeUseArr = dataHS300InnerCodeArr
        dataReturnArr = dataReturnArr[:, dataHS300CodeIndArr]    
        dataVolArr = dataVolArr[:, dataHS300CodeIndArr]    
        dataAFloatsArr = dataAFloatsArr[:, dataHS300CodeIndArr]    
        
    dataVolUseArr = np.zeros((len(dataTSArr), len(dataInnerCodeUseArr)))
    dataReturnUseArr = np.zeros((len(dataTSArr), len(dataInnerCodeUseArr)))
    dataAFloatsUseArr = np.zeros((len(dataTSArr), len(dataInnerCodeUseArr)))
    dataReturnUseArr[:] = np.nan
    dataVolUseArr[:] = np.nan
    dataAFloatsUseArr[:] = np.nan
    
    #bool1Arr = np.where((~np.isnan(dataVolArr[1])) & (dataVolArr[1]!=0))
    for i in range(len(dataTSArr)):
        posUseArr = np.where((~np.isnan(dataVolArr[i])) & (dataVolArr[i]!=0))
        dataVolUseArr[i][posUseArr] = dataVolArr[i][posUseArr]
        dataReturnUseArr[i][posUseArr] = dataReturnArr[i][posUseArr]
        dataAFloatsUseArr[i][posUseArr] = dataAFloatsArr[i][posUseArr]
    
    dataReturnDF = pd.DataFrame(dataReturnUseArr, index=dataTSArr, columns=dataInnerCodeUseArr)
    dataAFloatsDF = pd.DataFrame(dataAFloatsUseArr, index=dataTSArr, columns=dataInnerCodeUseArr)
    
    # 3 groups return
    dataROEReturnDF = pd.DataFrame([], index=dataTSArr, columns=['low', 'median', 'high', 'HML'])
    
    counts = 0
    for year in yearGroupLis:
        groupTemLis = [thrGroDic[i][year] for i in ['low', 'median', 'high']]
        for date in dataTSArr[(dataTSArr>(year*10000+430)) & (dataTSArr<((year+1)*10000+501))]:
            for i, group in enumerate(groupTemLis):
                dataOGTemDF = pd.DataFrame(index=group, columns=['return', 'aFloats', 'weight', 'wReturn'])
                dataOGTemDF['return'] = dataReturnDF.loc[date][group]
                dataOGTemDF['aFloats'] = dataAFloatsDF.loc[date][group]
                dataOGTemDF['weight'] = dataOGTemDF['aFloats'] / dataOGTemDF['aFloats'].sum()
                dataOGTemDF['wReturn'] = dataOGTemDF['return'] * dataOGTemDF['weight']				
                dataROEReturnDF.loc[date].iloc[i] = dataOGTemDF['wReturn'].sum()
            counts = counts + 1    
            if counts%50 == 0:
                print date, 
    
    dataROEReturnDF['HML'] = dataROEReturnDF['high'] - dataROEReturnDF['low']
    
    return dataROEReturnDF
#    dataROEReturnDF.describe()
#    dataROEReturnDF.corr()

ROEReturnGetTest = ROEReturnGet()
ROE_HS300ReturnGetTest = ROEReturnGet(Flag=1)


#==============================================================================
# 7. save ROE return data
#==============================================================================

# save 3 groups ROE return
dataROEReturn = ROE_HS300ReturnGetTest
colArr = np.zeros((1, len(dataROEReturn.columns)), dtype=object)
for i, j in enumerate(dataROEReturn.columns):
    colArr[0][i] = np.array([j])

dataDic = {'colItems': colArr, \
           'indexTime': dataTSArr.reshape(len(dataTSArr), 1), \
           'LC_YearDuration_HS300_ROE_3Groups_Return': dataROEReturn.values}

sio.savemat('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_YearDuration_HS300_ROE_3Groups_Return_arr.mat', dataDic)




#
#import matplotlib.pyplot as plt
#
#fig = plt.figure(figsize=(20, 8))
#ax1 = fig.add_subplot(411)
#ax2 = fig.add_subplot(412)
#ax3 = fig.add_subplot(413)
#ax4 = fig.add_subplot(414)
#ax1.plot(range(len(dataROEReturn.index)), dataROEReturn['HML'].values, label='HML')
#ax2.plot(range(len(dataROEReturn.index)), dataROEReturn['low'].values, label='low')
#ax3.plot(range(len(dataROEReturn.index)), dataROEReturn['median'].values, label='median')
#ax4.plot(range(len(dataROEReturn.index)), dataROEReturn['high'].values ,label='high')
#
#tickUseInd = np.arange(600, len(dataTSArr), 600)
#ax1.set_xticks(tickUseInd)
#ax1.set_xticklabels(dataTSArr[tickUseInd], rotation=30)
##ax1.set_xlabel('Stages')
#ax2.set_xticks(tickUseInd)
#ax2.set_xticklabels(dataTSArr[tickUseInd], rotation=30)
#ax3.set_xticks(tickUseInd)
#ax3.set_xticklabels(dataTSArr[tickUseInd], rotation=30)
#ax4.set_xticks(tickUseInd)
#ax4.set_xticklabels(dataTSArr[tickUseInd], rotation=30)
#ax1.legend(loc='best')
#ax2.legend(loc='best')
#ax3.legend(loc='best')
#ax4.legend(loc='best')
#plt.savefig('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/HS300_ROEReturn.png', dpi=600)
    
    
        
    
    
    
    
    
    
    
    
    
