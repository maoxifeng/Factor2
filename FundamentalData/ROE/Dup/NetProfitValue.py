#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 14:10:11 2017

@author: liushuanglong
"""


import numpy as np
import scipy.io as sio
import pandas as pd
import cPickle as cp


# load code
pathCode = '/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
dataCode =  sio.loadmat(pathCode)
dataComCode = dataCode['data'].T[1]   # 3415



# load non financial income statement_new data
pathNF = '/home/liushuanglong/MyFiles/Data/JYDB2/LC_IncomeStatementNew/LC_IncomeStatementNew_mat.mat'
dataNFRaw = sio.loadmat(pathNF)  
dataNFColTol = [dataNFRaw['col'][0][i][0] for i in range(dataNFRaw['col'].shape[1])]
dataNFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'NetProfit']
dataNFColUseInd = [dataNFColTol.index(i) for i in dataNFColUseLis]
dataNFIncomeTolArr = dataNFRaw['data'][:, dataNFColUseInd]


# dataframe, select by company code and mark
dataNFIncomeTolDF = pd.DataFrame(dataNFIncomeTolArr, columns=dataNFColUseLis)    # 923302
dataNFIncomeUseDF = dataNFIncomeTolDF[dataNFIncomeTolDF[u'CompanyCode'].isin(dataComCode)]  # 667895
dataNFIncomeUseDF = dataNFIncomeUseDF[dataNFIncomeUseDF[u'Mark'].isin([1, 2])]      # 293845
dataNFIncomeUseDF = dataNFIncomeUseDF[dataNFIncomeUseDF[u'NetProfit'].notnull()]    #293805 


# load financial income statement_new data
pathF = '/home/liushuanglong/MyFiles/Data/JYDB2/LC_FIncomeStatementNew/LC_FIncomeStatementNew_mat.mat'
dataFRaw = sio.loadmat(pathF)  
dataFColTol = [dataFRaw['col'][0][i][0] for i in range(dataFRaw['col'].shape[1])]
dataFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'NetProfit']
dataFColUseInd = [dataFColTol.index(i) for i in dataFColUseLis]
dataFIncomeTolArr = dataFRaw['data'][:, dataFColUseInd]


# dataframe, select by company code and mark
dataFIncomeTolDF = pd.DataFrame(dataFIncomeTolArr, columns=dataFColUseLis)    # 25283
dataFIncomeUseDF = dataFIncomeTolDF[dataFIncomeTolDF[u'CompanyCode'].isin(dataComCode)]  # 9550
dataFIncomeUseDF = dataFIncomeUseDF[dataFIncomeUseDF[u'Mark'].isin([1, 2])]      # 4500
dataFIncomeUseDF = dataFIncomeUseDF[dataFIncomeUseDF[u'NetProfit'].notnull()]    #4493


# look for duplicated companycode
dataNFComCodeUse = np.unique(dataNFIncomeUseDF[u'CompanyCode'])             # used company code, 3364 counts
dataFComCodeUse = np.unique(dataFIncomeUseDF[u'CompanyCode'])             # used company code, 61 counts


#dataDupComCodeSet = set(dataNFComCodeUse) & set(dataFComCodeUse)
#dataTolComCodeSet = set(dataNFComCodeUse) | set(dataFComCodeUse)
dataDupComCode = np.unique(list(set(dataNFComCodeUse) & set(dataFComCodeUse)))   # duplicated code  11
dataTolComCode = np.unique(list(set(dataNFComCodeUse) | set(dataFComCodeUse)))   # total code use 3414

dataNFEComCode = np.unique(list(set(dataNFComCodeUse) - set(dataFComCodeUse)))        # NF effective code  3353
dataFEComCode = np.unique(list(set(dataFComCodeUse) - set(dataNFComCodeUse)))          # F effective code  50



# sort by company code , published date, end date, mark
dataNFIncomeUseDFSor = dataNFIncomeUseDF.sort_values(by=[u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark'], \
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
        
## have a see
#dataNFIncomeUseDFInd.loc[348].tail()
#len(dataNFIncomeUseDFInd.loc[348])
#dataFIncomeUseDFInd.loc[348].head()
#len(dataFIncomeUseDFInd.loc[348])
#dataTolIncomeDic[348].loc[20060819:].head(10)
#len(dataTolIncomeDic[348])


#dataNFIncomeDic = {}
#dataFIncomeDic = {}
#dataDupIncomeDic = {}
#
#for code in dataNFComCodeUse:
#    dataNFIncomeDic[code] = dataNFIncomeUseDFInd.loc[code]
#for codeF in dataFComCodeUse:
#    dataFIncomeDic[code] = dataFIncomeUseDFInd.loc[code]
#       
#for code in dataDupComCode:
#    dataNFIncomeDFTemp = dataNFIncomeDic[code]
#    dataFIncomeDFTemp = dataFIncomeDic[code]
#    dataDupIncomeDFTemp = pd.concat([dataNFIncomeDFTemp, dataFIncomeDFTemp])
#    dataDupIncomeDic[code] = dataDupIncomeDFTemp
#    
#dataTolIncomeDic = {}
#for code in dataNFEComCode:
#    dataTolIncomeDic[code] = dataNFIncomeDic[code]
#    
#for code in dataFEComCode:
#    dataTolIncomeDic[code] = dataFIncomeDic[code]
#
#for code in dataDupComCode:
#    dataTolIncomeDic[code] = dataDupIncomeDic[code]
#


# create a new df dict
dataTolIncomeDicUse = {}   
for number, code in enumerate(dataTolComCode):    
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
    if number%10 == 0:                   
        print (number, code),                    
    dataTolIncomeDicUse[code] = dfOneCodeUse                       
                            
                            
# accomplish the NetProfit, save by cPickle as dictionary
#
cp.dump(dataTolIncomeDicUse, open("/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalData/LC_IncomeStatementNew_Total_NetProfit_YearDuration_DicUse.pkl", "w")) 

#cp.dump(dataIncomeDic, open("/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalData/LC_IncomeStatementNew_NetProfit_YearDuration_Dic.pkl", "w")) 


    
    
    
    
            
            




