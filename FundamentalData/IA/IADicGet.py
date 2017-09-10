# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 09:51:41 2017

@author: liusl
"""


import numpy as np
import scipy.io as sio
import pandas as pd
import time
import Common.SmaFun as cs
import Common.TimeCodeGet as tc

# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)



def IADicGet():    
    #
    #==============================================================================
    # 1. get datetime series, code numbers we used
    #==============================================================================
    #==============================================================================
    # 2. get data from banlance sheet
    #==============================================================================
    
    #def equityGet():
    # load non financial balance statement_new data
    pathNF = '/data/liushuanglong/MyFiles/Data/JYDB2/LC_BalanceSheetNew/LC_BalanceSheetNew.mat'
    dataNFRaw = cs.SheetToDFGet(pathNF)  
    dataNFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'FixedAssets',\
     u'TotalCurrentAssets', u'TotalCurrentLiability', u'TotalAssets']
    
    # dataframe, select by company code and mark
    dataNFBalanceTolDF = dataNFRaw[dataNFColUseLis]
    dataNFBalanceUseDF = dataNFBalanceTolDF[dataNFBalanceTolDF[u'CompanyCode'].isin(dataComCodeArr)]  #544258 
    dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceUseDF[u'Mark'].isin([1, 2])]      #287129
    
    # dropna nan and zero values
    dataNFBalanceNanInd = ((dataNFBalanceUseDF[u'FixedAssets'].notnull()) & (dataNFBalanceUseDF[u'FixedAssets'] != 0)\
     & (dataNFBalanceUseDF[u'TotalCurrentAssets'].notnull()) & (dataNFBalanceUseDF[u'TotalCurrentAssets'] != 0)\
     & (dataNFBalanceUseDF[u'TotalCurrentLiability'].notnull()) & (dataNFBalanceUseDF[u'TotalCurrentLiability'] != 0)\
     & (dataNFBalanceUseDF[u'TotalAssets'].notnull()) & (dataNFBalanceUseDF[u'TotalAssets'] != 0)  )
     
    dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceNanInd]    #285190
    
    
    # load financial balance statement_new data
    pathF = '/data/liushuanglong/MyFiles/Data/JYDB2/LC_FBalanceSheetNew/LC_FBalanceSheetNew.mat'
    dataFRaw = cs.SheetToDFGet(pathF)  
    dataFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'FixedAssets', u'TotalAssets']
    
    # dataframe, select by company code and mark
    dataFBalanceTolDF = dataFRaw[dataFColUseLis]
    dataFBalanceUseDF = dataFBalanceTolDF[dataFBalanceTolDF[u'CompanyCode'].isin(dataComCodeArr)]  # 7902
    dataFBalanceUseDF = dataFBalanceUseDF[dataFBalanceUseDF[u'Mark'].isin([1, 2])]      # 4437
    
    # drop nan
    dataFBalanceNanInd = ((dataFBalanceUseDF[u'FixedAssets'].notnull()) & (dataFBalanceUseDF[u'FixedAssets'] != 0)\
     & (dataFBalanceUseDF[u'TotalAssets'].notnull()) & (dataFBalanceUseDF[u'TotalAssets'] != 0)  )
    
    dataFBalanceUseDF = dataFBalanceUseDF[dataFBalanceNanInd]    #4301
    
    # look for duplicated companycode
    dataNFComCodeUse = np.unique(dataNFBalanceUseDF[u'CompanyCode']) # used company code,   banlenc:3362
    len(dataNFComCodeUse)
    dataFComCodeUse = np.unique(dataFBalanceUseDF[u'CompanyCode'])   # used company code,  balence: 61
    len(dataFComCodeUse)
    
    #dataDupComCodeSet = set(dataNFComCodeUse) & set(dataFComCodeUse)
    #dataTolComCodeSet = set(dataNFComCodeUse) | set(dataFComCodeUse)
    dataTolComCode = sorted(set(dataNFComCodeUse) | set(dataFComCodeUse))   # total code use balence:3414
    len(dataTolComCode)
    dataDupComCode = sorted(set(dataNFComCodeUse) & set(dataFComCodeUse))   # duplicated code balence: 9
    len(dataDupComCode)
    dataNFEComCode = sorted(set(dataNFComCodeUse) - set(dataFComCodeUse))   # NF effective code  balence: 3353
    len(dataNFEComCode)
    dataFEComCode = sorted(set(dataFComCodeUse) - set(dataNFComCodeUse))    # F effective code  balence:52
    len(dataFEComCode)
    
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
            dataTolBalanceDic[code] = dataDupBalanceDFTemp.reindex(columns=[u'EndDate', u'Mark', 'FixedAssets',\
                u'TotalCurrentAssets', u'TotalCurrentLiability', u'TotalAssets']).fillna(0)
        elif code in dataNFEComCode:
            dataTolBalanceDic[code] = dataNFBalanceUseDFInd.loc[code]
        else:
            dataTolBalanceDic[code] = dataFBalanceUseDFInd.loc[code].reindex(columns=[u'EndDate', u'Mark', 'FixedAssets',\
                u'TotalCurrentAssets', u'TotalCurrentLiability', u'TotalAssets'], fill_value=0)
    return dataTolBalanceDic

def IABarraExposureGet():
    
    dataIADic = IADicGet()
    print 'IADic got'
    comCodeUseLis = dataIADic.keys()
    
    # calculate IA values
    dataIAUse={}
    colNames = [u'IA', u'EndDate']
    print 'Start calculating:'
    for iicode, icode in enumerate(comCodeUseLis):
        dataIATempDF = dataIADic[icode]
        dataIATempDF[u'Capital'] = dataIATempDF[u'FixedAssets'] + dataIATempDF[u'TotalCurrentAssets'] - dataIATempDF[u'TotalCurrentLiability']
        dateSerTemArr = np.unique(dataIATempDF.index)
        iIAUseTempDF = pd.DataFrame(columns=colNames)
        for iidate, idate in enumerate(dateSerTemArr):
            idateIATempDF = dataIATempDF[dataIATempDF.index<=idate].sort_values(by=[u'EndDate', u'Mark'], ascending=[True, False])
            idateEndDateArr = np.unique(idateIATempDF['EndDate'])
            for iiendDate, iendDate in enumerate(idateEndDateArr[::-1]):
                if (iendDate-10**4) in idateEndDateArr:
                    ilastEndDate = idateEndDateArr[idateEndDateArr==(iendDate-10**4)][-1]
                    icapital = idateIATempDF[idateIATempDF[u'EndDate']==iendDate][u'Capital'].iloc[-1]
                    ilastCapital = idateIATempDF[idateIATempDF[u'EndDate']==ilastEndDate ][u'Capital'].iloc[-1]
                    iassets = idateIATempDF[idateIATempDF[u'EndDate']==iendDate][u'TotalAssets'].iloc[-1]
                    idifIAValues = (icapital - ilastCapital)/ iassets
                    iIAUseTempDF.loc[idate] = [idifIAValues, iendDate]  # keep enddate and IA values
                    
                    break
        
        dataIAUse[icode] = iIAUseTempDF
        if (iicode+1)%100 == 0:
            print time.strftime("%H:%M:%S", time.localtime()),   
            print iicode, icode
        
    dataFormatDF = pd.DataFrame(index=dataDSArr, columns=dataComCodeArr)        
    
    for iicode, icode in enumerate(comCodeUseLis):
        if dataIAUse[icode].size==0:
            continue        
        pubDateLis = dataIAUse[icode].index.tolist()
        pubDateLis.extend(list(dataDSArr))
        allDateArr = np.unique(pubDateLis)
        # famative date process
        icodeDF = dataIAUse[icode].reindex(index=allDateArr, method='ffill')
        icodeDefDF = icodeDF.loc[dataDSArr]
        dataFormatDF[icode] = icodeDefDF[u'IA']
    dataFormatDF.columns = dataInnerCodeArr
    
    print 'IA_Barra DF completed'
    return dataFormatDF


def IAFMDicGet():
        # load IA data dic
    dataIADic = IADicGet()
    print 'IA values dic got'
    dataTolComCode = dataIADic.keys()
    
    # create a new df dict
    dataIAYearendDic = {}
    for number, code in enumerate(dataTolComCode):    
        dfBalanceCode = dataIADic[code]
        pubDateArr = np.unique(dfBalanceCode.index)              
        pubYearArr = np.unique([int(i)/10000 for i in pubDateArr])
        dfOneCodeUse = pd.DataFrame(columns=[u'Change_On_Investments_To_Assets'])
        for year in pubYearArr:
            dateIndArr = np.where((pubDateArr>(year*10000)) & (pubDateArr<(year*10000+501)))[0]
    
            if (len(dateIndArr) > 0):
                pubDateUseArr = pubDateArr[dateIndArr]
                lastYearDate = (year-1) * 10000 + 1231
                llastYearDate = (year-2) * 10000 + 1231 
                if (lastYearDate in dfBalanceCode.loc[pubDateUseArr, u'EndDate'].values)\
                        & (llastYearDate in dfBalanceCode.loc[:pubDateUseArr[-1], u'EndDate'].values):
                    # last yearend data
                    dfBalanceOneCodeLYTemp = dfBalanceCode.loc[pubDateUseArr]#  t-1 year date must in t year 0101~0430
                    dfBalanceOneCodeLYTemp = dfBalanceOneCodeLYTemp[dfBalanceOneCodeLYTemp[u'EndDate'] == lastYearDate].iloc[-1, 2:]
            #            dfBalanceOneCodeLYTemp = dfBalanceOneCodeLYTemp[:-1] / dfBalanceOneCodeLYTemp[-1]   # calculte ratio
                    # last two yearend data
                    dfBalanceOneCodeLLYTemp = dfBalanceCode.loc[:pubDateUseArr[-1]]  # t-2 year date can <= t year 0430  
                    dfBalanceOneCodeLLYTemp = dfBalanceOneCodeLLYTemp[dfBalanceOneCodeLLYTemp[u'EndDate'] == llastYearDate].iloc[-1, 2:]
            #            dfBalanceOneCodeLLYTemp = dfBalanceOneCodeLLYTemp[:-1] / dfBalanceOneCodeLLYTemp[-1]  #  calculte ratio
                    # change
                    dfBalanceOneCodeTemp = dfBalanceOneCodeLYTemp - dfBalanceOneCodeLLYTemp   # drop 'assets item'
                    dfOneCodeUse.loc[year] = (dfBalanceOneCodeTemp.iloc[0] + dfBalanceOneCodeTemp.iloc[1] - dfBalanceOneCodeTemp.iloc[2]) / \
                                          dfBalanceOneCodeLYTemp.iloc[-1]  
                    
        dataIAYearendDic[code] = dfOneCodeUse
    return dataIAYearendDic
    
    
    
    
    


