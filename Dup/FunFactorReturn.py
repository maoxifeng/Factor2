#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 15:30:27 2017

@author: liushuanglong
"""

'''
#==============================================================================
# factor return function
#==============================================================================
'''




import numpy as np
import scipy.io as sio
import pandas as pd


#==============================================================================
# 1. get datetime series, code numbers we used
#==============================================================================

def dataTimeSeriesDicGet():
    pathTS =  '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat'     
    dataTSRaw = sio.loadmat(pathTS)      
    dataTSArr = dataTSRaw['data'][:, 0]     # 6498
    dataTSDic = {'dataTSArr': dataTSArr}
    return dataTSDic

def dataCodeNumDicGet():
    pathCode = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
    dataCodeRaw = sio.loadmat(pathCode)
    dataCodeArr = dataCodeRaw['data']
    dataInnerCodeArr = dataCodeArr[:, 0]
    dataComCodeArr = dataCodeArr[:, 1]
    dataCodeNumDic = {'dataInnerCodeArr': dataInnerCodeArr, 'dataComCodeArr': dataComCodeArr}
    return dataCodeNumDic

    
#==============================================================================
# 2. calculate ROE values
#==============================================================================



## 2.1 get income data from LC_IncomeStatementNew

def dataIncomeItemValueGet(item):  # item: u'NetProfit'

    
### 2.1.1 load non financial income data and financial income data
    # load code
    dataComCodeArr = dataCodeNumDicGet()['dataComCodeArr']   # 3415

    # itemscolumns list we used     
    dataColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark']
    dataColUseLis.append(item)
    
    # load non financial income statement_new data
    pathNF = '/home/liushuanglong/MyFiles/Data/JYDB2/LC_IncomeStatementNew/LC_IncomeStatementNew_mat.mat'
    dataNFRaw = sio.loadmat(pathNF)  
    dataNFColTol = [dataNFRaw['col'][0][i][0] for i in range(dataNFRaw['col'].shape[1])]

    dataNFColUseInd = [dataNFColTol.index(i) for i in dataColUseLis]  # items index
    dataNFIncomeTolArr = dataNFRaw['data'][:, dataNFColUseInd]      
        
    # dataframe, data selected by company code and mark
    dataNFIncomeTolDF = pd.DataFrame(dataNFIncomeTolArr, columns=dataColUseLis)    # 923302rows
    dataNFIncomeUseDF = dataNFIncomeTolDF[dataNFIncomeTolDF[u'CompanyCode'].isin(dataComCodeArr)]  # 667895rows left
    dataNFIncomeUseDF = dataNFIncomeUseDF[dataNFIncomeUseDF[u'Mark'].isin([1, 2])]      # 293845rows left
    dataNFIncomeUseDF = dataNFIncomeUseDF[dataNFIncomeUseDF[item].notnull()]    # drop na rows, 293805rows left
    
    
    # load financial income statement_new data
    pathF = '/home/liushuanglong/MyFiles/Data/JYDB2/LC_FIncomeStatementNew/LC_FIncomeStatementNew_mat.mat'
    dataFRaw = sio.loadmat(pathF)  
    dataFColTol = [dataFRaw['col'][0][i][0] for i in range(dataFRaw['col'].shape[1])]
    dataFColUseInd = [dataFColTol.index(i) for i in dataColUseLis]   # items index
    dataFIncomeTolArr = dataFRaw['data'][:, dataFColUseInd]    
    
    
    # dataframe, select by company code and mark
    dataFIncomeTolDF = pd.DataFrame(dataFIncomeTolArr, columns=dataColUseLis)    # 25283
    dataFIncomeUseDF = dataFIncomeTolDF[dataFIncomeTolDF[u'CompanyCode'].isin(dataComCodeArr)]  # 9550
    dataFIncomeUseDF = dataFIncomeUseDF[dataFIncomeUseDF[u'Mark'].isin([1, 2])]      # 4500
    dataFIncomeUseDF = dataFIncomeUseDF[dataFIncomeUseDF[item].notnull()]    #4493

    
### 2.1.2 combine non financial income data with financial income data    
    # look for duplicated companycode
    dataNFComCodeUse = np.unique(dataNFIncomeUseDF[u'CompanyCode'])      # NF used company code, 3364 counts
    dataFComCodeUse = np.unique(dataFIncomeUseDF[u'CompanyCode'])       # F used company code, 61 counts
    
    
    dataDupComCode = np.unique(list(set(dataNFComCodeUse) & set(dataFComCodeUse)))   # duplicated code  11
    dataTolComCode = np.unique(list(set(dataNFComCodeUse) | set(dataFComCodeUse)))   # total code use 3414
    
    dataNFEComCode = np.unique(list(set(dataNFComCodeUse) - set(dataFComCodeUse)))        # NF effective code  3353
    dataFEComCode = np.unique(list(set(dataFComCodeUse) - set(dataNFComCodeUse)))          # F effective code  50
    
    
    # sort by company code , published date, end date, mark
    dataNFIncomeUseDFSor = dataNFIncomeUseDF.sort_values(by=[u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark'], \
                                                         ascending=[True, True, True, False])
    dataFIncomeUseDFSor = dataFIncomeUseDF.sort_values(by=[u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark'], \
                                                       ascending=[True, True, True, False])
    
    dataNFIncomeUseDFInd = dataNFIncomeUseDFSor.set_index([u'CompanyCode', u'InfoPublDate'])
    dataFIncomeUseDFInd = dataFIncomeUseDFSor.set_index([u'CompanyCode', u'InfoPublDate'])

    
    # create  a dict , contain all code data
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
 
    
### 2.1.3 calculate item yearend value    
    # create a new df dict
    dataTolIncomeDicUse = {}   
    for number, code in enumerate(dataTolComCode):    
        dfOneCode = dataTolIncomeDic[code]                              # df one code
        pubDateOneCodeArr = np.unique(dfOneCode.index)
        
        dfOneCodeUse = pd.DataFrame([], columns=[u'EndDate', u'Mark', item])    # contain the data we used
        for day in pubDateOneCodeArr:
            dfOneCodeUseTolRaw = dfOneCode.loc[:day]
            dfOneCodeUseTolRaw = dfOneCodeUseTolRaw.sort_values(u'EndDate')
            arrEndDate = np.unique(dfOneCodeUseTolRaw[u'EndDate'])
            
            arrEndDateDiv = np.array([(int(date)/10000, int(date)%10000) for date in arrEndDate])
            EndDateYearArr = arrEndDateDiv[:, 0]        # year arr
            EndDateDayArr = arrEndDateDiv[:, 1]        # day arr
    
            if 1231 in EndDateDayArr:

                yearEndDayInd = [i for i in range(len(EndDateDayArr)) if EndDateDayArr[i] == 1231]           # yearend day index 
                yearEndArr = EndDateYearArr[yearEndDayInd]              # yearend list
                yearEndDayArr = EndDateDayArr[yearEndDayInd]         # yearend day list
                if yearEndDayInd[-1] == len(arrEndDate)-1:     # if there have >=1 yearend and the last yearend is new,  use it                
                
                    dfOneCodeUseTemp  = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                           arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', keep='last')
                    dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
                elif len(yearEndDayInd) == 1 :
                    theyearEnd= EndDateYearArr[yearEndDayInd[0]]    # only one year end 
                    pastYearArr = EndDateYearArr[: yearEndDayInd[0]][::-1]    # past year end year
                    pastYearDayArr = EndDateDayArr[: yearEndDayInd[0]][::-1]  #past year end day
                    recentYearArr = EndDateYearArr[yearEndDayInd[0]+1:][::-1] #recent year end year
                    recentYearDayArr = EndDateDayArr[yearEndDayInd[0]+1:][::-1]  # recent year end day
                    
                    if len(set(pastYearDayArr) & set(recentYearDayArr)) !=0:
                        count = 0
                        for recentday in recentYearDayArr:
                            if recentday in pastYearDayArr:
                                pastYearUse = pastYearArr[pastYearDayArr == recentday][0]
                                pastDateUse = pastYearUse*10000 + recentday
                                recentYearUse = recentYearArr[recentYearDayArr == recentday][0]
                                recentDateUse = recentYearUse*10000 + recentday
                                if recentYearUse == pastYearUse+1:
                                    pastDateNet = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  pastDateUse].drop_duplicates('EndDate', \
                                                                     keep='last')[item].values[0]
                                    
                                    recentDateNet = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  recentDateUse].drop_duplicates('EndDate', \
                                                                       keep='last')[item].values[0]
                                    yearEndNet = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                           arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', \
                                                                    keep='last')[item].values[0]
                                    
                                    dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  recentDateUse].drop_duplicates('EndDate', keep='last')
                                    dfOneCodeUseTemp.iloc[0][item] = recentDateNet + yearEndNet - pastDateNet
            #                    dayUse = dfOneCodeUseTemp.index
                                    dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
                                    break
                            count = count + 1
                        if count == len(recentYearDayArr):                        
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
                    
                    newestYearDayArr = EndDateDayArr[newestYearEndDayInd+1:][::-1]
                    newestYearArr = EndDateYearArr[newestYearEndDayInd+1:][::-1]
                    lastYearDayArr = EndDateDayArr[lastYearEndDayInd+1: newestYearEndDayInd][::-1]
                    lastYearArr = EndDateYearArr[lastYearEndDayInd+1: newestYearEndDayInd][::-1]
                    if len(set(lastYearDayArr) & set(newestYearDayArr))==0:
                        dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                              arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', keep='last')
    #                    dayUse = dfOneCodeUseTemp.index
                        dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
                    else:
                        count = 0
                        for newestday in  newestYearDayArr:
                            if newestday in lastYearDayArr:
                                lastYearUse = lastYearArr[lastYearDayArr == newestday][0]
                                lastDateUse = lastYearUse*10000 + newestday
                                newestYearUse = newestYearArr[newestYearDayArr == newestday][0]
                                newestDateUse = newestYearUse*10000 + newestday
                                if newestYearUse == lastYearUse+1:
                                    lastDateNet = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  lastDateUse].drop_duplicates('EndDate', \
                                                                     keep='last')[item].values[0]
                                    
                                    newestDateNet = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  newestDateUse].drop_duplicates('EndDate', \
                                                                       keep='last')[item].values[0]
                                    
                                    yearEndNet = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                           arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', \
                                                                    keep='last')[item].values[0]
                                    dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  newestDateUse].drop_duplicates('EndDate', keep='last')
                                    dfOneCodeUseTemp.iloc[0][item] = newestDateNet + yearEndNet - lastDateNet
                                    dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
                                    break
                            count = count + 1
                        if count == len(newestYearDayArr):
                            dfOneCodeUseTemp = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                                  arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', \
                                                                  keep='last')
                            dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
        if number%10 == 0:                   
            print (number, code),                    
        dataTolIncomeDicUse[code] = dfOneCodeUse                       
                                
    return dataTolIncomeDicUse                             




## 2.2 get balance data from LC_BalanceStatementNew

def dataBalanceItemValueGet(item):  # item: u'Total sharehold equity' 
    






















