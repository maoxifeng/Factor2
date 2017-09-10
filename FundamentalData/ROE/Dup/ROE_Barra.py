# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 12:08:24 2017

@author: liusl
"""




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
import time

import Common.TimeCodeGet as tc
import FundamentalData.ROE.sheetDicGet as sg




'''
This program is to calculate ROE formative values and then barra return.

Netprofit is calculated as the year duration data at the newest date.

'''
# working path
pathROE = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/'

#==============================================================================
# 1. load time and code 
#==============================================================================
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)

#==============================================================================
# 2. load balance, income sheet data, and calculate year duration ROE
#==============================================================================
dataTolBalanceDic= sg.equityGet()
dataTolIncomeDic = sg.netprofitGet()

# 
dataTolNetDic = {}   
print 'begin calculate netprofit: '
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
        
    dataTolROEDic[code] = dfROEOneCode
    
# end for loop, and save ROE dic
#cp.dump(dataTolROEDic, open(pathROE + 'ROE_FormatValuesDic.pkl', 'w')) 


#==============================================================================
# 3. save as 3 dimensional array            
#==============================================================================
import FundamentalData.FunCommon.Format3DArrayGet as f3a

ROE3DArr, ROE3DArrPath = f3a.FacDicTo3DArrDicGet(dataRawDic=dataTolROEDic, savePath=pathROE, facName='ROE')


#==============================================================================
#4. Barra Return
#==============================================================================

import FundamentalData.FunCommon.FactorReturnGet as facret

# all stock return
ROE_A_BarraReturn = facret.FactorBarraReturnGet(loadPath=ROE3DArrPath, index=3, facName='ROE')

# HS300 return
ROEHS300_OLSReturn = facret.FactorBarraReturnGet(loadPath=ROE3DArrPath, pool='HS300',index=3, facName='ROE')































