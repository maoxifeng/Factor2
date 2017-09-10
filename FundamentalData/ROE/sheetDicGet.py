# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 16:35:35 2017

@author: liusl
"""


import numpy as np
import scipy.io as sio
import pandas as pd
import time
import Common.TimeCodeGet as tc
import Common.SmaFun as cs

# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)

'''may be packaged to one function'''

#==============================================================================
# 1. get netprofit data
#==============================================================================


def NetprofitDicGet():
    
    # load non financial income statement_new data
    pathNFIC = '/data/liushuanglong/MyFiles/Data/JYDB2/LC_IncomeStatementNew/LC_IncomeStatementNew.mat'
    dataNFICRaw = cs.SheetToDFGet(pathNFIC)  
    dataNFICColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'NetProfit']
    dataNFIncomeTolArr = dataNFICRaw[dataNFICColUseLis]
    # dataframe, select by company code and mark
    dataNFIncomeTolDF = pd.DataFrame(dataNFIncomeTolArr, columns=dataNFICColUseLis)    # 923302
    dataNFIncomeUseDF = dataNFIncomeTolDF[dataNFIncomeTolDF[u'CompanyCode'].isin(dataComCodeArr)]  # 667895
    dataNFIncomeUseDF = dataNFIncomeUseDF[dataNFIncomeUseDF[u'Mark'].isin([1, 2])]      # 293845
    dataNFIncomeUseDF = dataNFIncomeUseDF[dataNFIncomeUseDF[u'NetProfit'].notnull()]    #293805 
    
    # load financial income statement_new data
    pathFIC = '/data/liushuanglong/MyFiles/Data/JYDB2/LC_FIncomeStatementNew/LC_FIncomeStatementNew.mat'
    dataFICRaw = cs.SheetToDFGet(pathFIC)  
    dataFICColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'NetProfit']
    dataFIncomeTolArr = dataFICRaw[dataFICColUseLis]
    
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
#    dataFEComCode = np.unique(list(set(dataFICComCodeUse) - set(dataNFICComCodeUse)))          # F effective code  50
    
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

    return dataTolIncomeDic

#==============================================================================
# 2. get equity data
#==============================================================================

def EquityDicGet():
    
    # load non financial balance statement_new data
    pathNF = '/data/liushuanglong/MyFiles/Data/JYDB2/LC_BalanceSheetNew/LC_BalanceSheetNew.mat'
    dataNFRaw = cs.SheetToDFGet(pathNF)  
    dataNFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'TotalShareholderEquity', u'DeferredTaxAssets', \
                       u'EPreferStock']
    dataNFBalanceTolArr = dataNFRaw[dataNFColUseLis]
    
    # dataframe, select by company code and mark
    dataNFBalanceTolDF = pd.DataFrame(dataNFBalanceTolArr, columns=dataNFColUseLis)    # 789264
    dataNFBalanceUseDF = dataNFBalanceTolDF[dataNFBalanceTolDF[u'CompanyCode'].isin(dataComCodeArr)]  # 544258
    dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceUseDF[u'Mark'].isin([1, 2])]      # 287129
    dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceUseDF[u'TotalShareholderEquity'].notnull()]    #287097
    dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceUseDF[u'TotalShareholderEquity']!=0]    #287075
    
    # load financial balance statement_new data
    pathF = '/data/liushuanglong/MyFiles/Data/JYDB2/LC_FBalanceSheetNew/LC_FBalanceSheetNew.mat'
    dataFRaw = cs.SheetToDFGet(pathF)  
    dataFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'TotalShareholderEquity', u'DeferredTaxAssets', \
                      u'EPreferStock']
    dataFBalanceTolArr = dataFRaw[dataFColUseLis]
    
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
#    dataFEComCode = sorted(set(dataFComCodeUse) - set(dataNFComCodeUse))    # F effective code  income:50, balence:51
    
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
    
    return dataTolBalanceDic


#==============================================================================
# 3. ROE_FMDicGet
#==============================================================================
def ROE_FMDicGet():
    
#    ROESavePath = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/'
    # 1. calculate ROE 
    # start calculate FM year duration ROE value 
    
    print 'start:', time.strftime('%H:%M:%S', time.localtime())
    dataTolIncomeDic = NetprofitDicGet()
    print 'netprofit dic got'
    
    dataTolBalanceDic = EquityDicGet()
    print 'equity dic got'
    
    #    # create a new df dict
    
    netprofitDic = {}   
    for number, code in enumerate(dataTolIncomeDic.keys()):    
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
        netprofitDic[code] = dfOneCodeUse
    
    equityDic = {}   
    for number, code in enumerate(dataTolBalanceDic.keys()):    
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
        equityDic[code] = dfOneCodeUse
    
    
    comCodeUseLis = list(set(netprofitDic.keys()) & set(equityDic.keys()))
    dataROEDic = {}
    for i, code in enumerate(comCodeUseLis):
        netOneCodeDF = netprofitDic[code]
        equityOneCodeDF = equityDic[code]
        ROEOneCodeDF = pd.concat([netOneCodeDF, equityOneCodeDF], axis=1)
        if ROEOneCodeDF.size != 0:
            ROETempDF = pd.DataFrame(columns=['ROE'])
            ROETempDF['ROE'] = ROEOneCodeDF[u'NetProfit'] / ROEOneCodeDF[u'equity']  # use innercode as columns names
            dataROEDic[code] = ROETempDF
    print 'ROE_FM dic completed.', time.strftime('%H:%M:%S', time.localtime())
    
    return dataROEDic
    

#==============================================================================
# 4.     
#==============================================================================
def ROE_BarraDFGet():
    
    '''
    This function is to calculate ROE values for subsequent barra return.
    
    Netprofit is calculated as the year duration data at the newest date.
    '''
    
    # working path
#    pathROE = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/'
    
    # load balance, income sheet data, and calculate year duration ROE
    dataTolBalanceDic= EquityDicGet()
    print 'equity dic got'
    
    dataTolIncomeDic = NetprofitDicGet()
    print 'netprofit dic got' 
    
    # 
    dataTolNetDic = {}   
    print 'begin calculate netprofit value: '
    print time.strftime("%H:%M:%S", time.localtime())
    print 'codeCounts', 'code' 
    for number, code in enumerate(dataTolIncomeDic.keys()):    
        dfOneCode = dataTolIncomeDic[code]                              # df one code
        pubDateOneCodeArr = np.unique(dfOneCode.index)
        
        dfOneCodeUse = pd.DataFrame([], columns=[u'EndDate', u'Mark', u'NetProfit'])    # contain the data we used
        for day in pubDateOneCodeArr:
            dfOneCodeUseTolRaw = dfOneCode.loc[:day]
            dfOneCodeUseTolRaw = dfOneCodeUseTolRaw.sort_values(u'EndDate')
            arrEndDate = np.unique(dfOneCodeUseTolRaw[u'EndDate'])
            
            arrEndDateDiv = np.array([(int(date)/10000, int(date)%10000) for date in arrEndDate])
            EndDateYearLis = arrEndDateDiv[:, 0]        # year arr
            EndDateDayLis = arrEndDateDiv[:, 1]        # day arr
    
            if 1231 not in EndDateDayLis:
                dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate'] ==\
                                                      arrEndDate[-1]].drop_duplicates(u'EndDate', keep='last')
            
                dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
            else:
                yearEndDayInd = [i for i in range(len(EndDateDayLis)) if EndDateDayLis[i] == 1231]           # yearend day index 
                yearEndDayInd = np.array([yearEndDayInd]).reshape(np.array([yearEndDayInd]).size).tolist()  # dup?
                yearEnd = EndDateYearLis[yearEndDayInd]              # yearend list
                yearEndDaylist = EndDateDayLis[yearEndDayInd]         # yearend day list
    #            if len(yearEndDayInd) == 1:                                    # if only one yearend data ,use it
    #                
    #                
    #                dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
    #                                                      arrEndDate[yearEndDayInd]].drop_duplicates('EndDate', keep='last')
    #                dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values   
                if yearEndDayInd[-1] == len(arrEndDate)-1:     # if there have >=1 yearend and the last yearend is new,  use it                
                    dfOneCodeUseTemp  = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                           arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', keep='last')
                    dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
                elif len(yearEndDayInd) == 1 :
                    theyearEnd= EndDateYearLis[yearEndDayInd[0]]    # only one year end 
                    pastYear = EndDateYearLis[: yearEndDayInd[0]][::-1]    # past year end year
                    pastYearDay = EndDateDayLis[: yearEndDayInd[0]][::-1]  #past year end day
                    recentYear = EndDateYearLis[yearEndDayInd[0]+1:][::-1] #recent year end year
                    recentYearDay = EndDateDayLis[yearEndDayInd[0]+1:][::-1]  # recent year end day
                    
                    if len(set(pastYearDay) & set(recentYearDay)) !=0:
    #                    dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
    #                                                          arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', keep='last')
    ##                    dayUse = dfOneCodeUseTemp.index
    #                    dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values
                        count = 0
                        for recentday in recentYearDay:
                            if recentday in pastYearDay:
                                pastYearUse = pastYear[pastYearDay == recentday][0]
                                pastDateUse = pastYearUse*10000 + recentday
                                recentYearUse = recentYear[recentYearDay == recentday][0]
                                recentDateUse = recentYearUse*10000 + recentday
                                if recentYearUse == pastYearUse+1:
                                    pastDateNet = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  pastDateUse].drop_duplicates('EndDate', \
                                                                     keep='last')[u'NetProfit'].values
                                    
                                    recentDateNet = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  recentDateUse].drop_duplicates('EndDate', \
                                                                       keep='last')[u'NetProfit'].values
                                    yearEndNet = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                           arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', \
                                                                    keep='last')[u'NetProfit'].values
                                    
                                    dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  recentDateUse].drop_duplicates('EndDate', keep='last')
                                    dfOneCodeUseTemp.iloc[0][u'NetProfit'] = recentDateNet + yearEndNet - pastDateNet
            #                    dayUse = dfOneCodeUseTemp.index
                                    dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
                                    break
                            count = count + 1
                        if count == len(recentYearDay):                        
                            dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', \
                                                                  keep='last')
                            dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
                    else:
                        dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                              arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', \
                                                              keep='last')
                        dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
                                                                
                else:   
                    newestYearEndDayInd = yearEndDayInd[-1]
                    lastYearEndDayInd = yearEndDayInd[-2]                
                    
                    newestYearDay = EndDateDayLis[newestYearEndDayInd+1:][::-1]
                    newestYear = EndDateYearLis[newestYearEndDayInd+1:][::-1]
                    lastYearDay = EndDateDayLis[lastYearEndDayInd+1: newestYearEndDayInd][::-1]
                    lastYear = EndDateYearLis[lastYearEndDayInd+1: newestYearEndDayInd][::-1]
                    if len(set(lastYearDay) & set(newestYearDay))==0:
                        dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                              arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', keep='last')
    #                    dayUse = dfOneCodeUseTemp.index
                        dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
                    else:
                        count = 0
                        for newestday in  newestYearDay:
                            if newestday in lastYearDay:
                                lastYearUse = lastYear[lastYearDay == newestday][0]
                                lastDateUse = lastYearUse*10000 + newestday
                                newestYearUse = newestYear[newestYearDay == newestday][0]
                                newestDateUse = newestYearUse*10000 + newestday
                                if newestYearUse == lastYearUse+1:
                                    lastDateNet = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  lastDateUse].drop_duplicates('EndDate', \
                                                                     keep='last')[u'NetProfit'].values
                                    
                                    newestDateNet = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  newestDateUse].drop_duplicates('EndDate', \
                                                                       keep='last')[u'NetProfit'].values
                                    
                                    yearEndNet = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                           arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', \
                                                                    keep='last')[u'NetProfit'].values
                                    dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  newestDateUse].drop_duplicates('EndDate', keep='last')
                                    dfOneCodeUseTemp.iloc[0][u'NetProfit'] = newestDateNet + yearEndNet - lastDateNet
            #                    dayUse = dfOneCodeUseTemp.index
                                    dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
                                    break
                            count = count + 1
                        if count == len(newestYearDay):
                            dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', \
                                                                  keep='last')
                            dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
        if number%100 == 0:                   
            print number, code                    
        dataTolNetDic[code] = dfOneCodeUse                       
    
                    
    # create a dic contains the ROE data,  calculate the ROE
    dataTolROEDic = {}
    dataTolComCode = list(set(dataTolNetDic.keys()) & set(dataTolBalanceDic.keys()))
    for number, code in enumerate(dataTolComCode):
        dfIncomeOneCode = dataTolNetDic[code]                              # df one code    
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
        if number%100 ==0:
            print (number, code)
        
#        dfROEOneCode = dfROEOneCode.reindex(columns=[u'ReturnOnEquity', u'EndDate', u'IncomeMark', u'BalanceMark'])
        dataTolROEDic[code] = dfROEOneCode
        
        
    dataFormatDF = pd.DataFrame(index=dataDSArr, columns=dataComCodeArr)        
    
    for iicode, icode in enumerate(dataTolComCode):
        if dataTolROEDic[icode].size==0:
            continue        
        pubDateLis = dataTolROEDic[icode].index.tolist()
        pubDateLis.extend(list(dataDSArr))
        allDateArr = np.unique(pubDateLis)
        # famative date process
        icodeDF = dataTolROEDic[icode].reindex(index=allDateArr, method='ffill')
        icodeDefDF = icodeDF.loc[dataDSArr]
        dataFormatDF[icode] = icodeDefDF[u'ReturnOnEquity']
    dataFormatDF.columns = dataInnerCodeArr
    
    
    print 'ROE_Barra DF completed'
    
    return dataFormatDF
    
    
    





































