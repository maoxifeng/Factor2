#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 09:48:25 2017

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








## 2.1 combine one kind NF data with F data
def dataSheetCombinDicGet(pathNF, pathF, item):  # path: string, item: string
    
### 2.1.1 load non financial item data and financial item data
    # load code
    dataComCodeArr = dataCodeNumDicGet()['dataComCodeArr']   # 3415

    # itemscolumns list we used     
    dataColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark']
    dataColUseLis.append(item)
    
    # load non financial  statement_new data
    dataNFRaw = sio.loadmat(pathNF)  
    dataNFColTol = [dataNFRaw['col'][0][i][0] for i in range(dataNFRaw['col'].shape[1])]

    dataNFColUseInd = [dataNFColTol.index(i) for i in dataColUseLis]  # items index
    dataNFItemTolArr = dataNFRaw['data'][:, dataNFColUseInd]      
        
    # dataframe, data selected by company code and mark
    dataNFItemTolDF = pd.DataFrame(dataNFItemTolArr, columns=dataColUseLis)    # 
    dataNFItemUseDF = dataNFItemTolDF[dataNFItemTolDF[u'CompanyCode'].isin(dataComCodeArr)]  # 
    dataNFItemUseDF = dataNFItemUseDF[dataNFItemUseDF[u'Mark'].isin([1, 2])]      # 
    dataNFItemUseDF = dataNFItemUseDF[dataNFItemUseDF[item].notnull()]    # drop na rows
    
    
    # load financial  statement_new data
    dataFRaw = sio.loadmat(pathF)  
    dataFColTol = [dataFRaw['col'][0][i][0] for i in range(dataFRaw['col'].shape[1])]
    dataFColUseInd = [dataFColTol.index(i) for i in dataColUseLis]   # items index
    dataFItemTolArr = dataFRaw['data'][:, dataFColUseInd]    
    
    
    # dataframe, select by company code and mark
    dataFItemTolDF = pd.DataFrame(dataFItemTolArr, columns=dataColUseLis)    # 
    dataFItemUseDF = dataFItemTolDF[dataFItemTolDF[u'CompanyCode'].isin(dataComCodeArr)]  # 
    dataFItemUseDF = dataFItemUseDF[dataFItemUseDF[u'Mark'].isin([1, 2])]      # 
    dataFItemUseDF = dataFItemUseDF[dataFItemUseDF[item].notnull()]    #

    
### 2.1.2 combine non financial  data with financial  data    
    # look for duplicated companycode
    dataNFComCodeUse = np.unique(dataNFItemUseDF[u'CompanyCode'])      # NF used company code
    dataFComCodeUse = np.unique(dataFItemUseDF[u'CompanyCode'])       # F used company code
    
    
    dataDupComCode = np.unique(list(set(dataNFComCodeUse) & set(dataFComCodeUse)))   # duplicated code  
    dataTolComCode = np.unique(list(set(dataNFComCodeUse) | set(dataFComCodeUse)))   # total code use 
    
    dataNFEComCode = np.unique(list(set(dataNFComCodeUse) - set(dataFComCodeUse)))        # NF effective code  
    dataFEComCode = np.unique(list(set(dataFComCodeUse) - set(dataNFComCodeUse)))          # F effective code  
    
    
    # sort by company code , published date, end date, mark
    dataNFItemUseDFSor = dataNFItemUseDF.sort_values(by=[u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark'], \
                                                         ascending=[True, True, True, False])
    dataFItemUseDFSor = dataFItemUseDF.sort_values(by=[u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark'], \
                                                       ascending=[True, True, True, False])
    
    dataNFItemUseDFInd = dataNFItemUseDFSor.set_index([u'CompanyCode', u'InfoPublDate'])
    dataFItemUseDFInd = dataFItemUseDFSor.set_index([u'CompanyCode', u'InfoPublDate'])

    
    # create  a dict , contain all code data
    dataTolItemDic={}   # 3414
    for code in dataTolComCode:
        if code in dataDupComCode:
            dataNFIncomeDFTemp = dataNFItemUseDFInd.loc[code]
            dataFIncomeDFTemp = dataFItemUseDFInd.loc[code]
            dataDupIncomeDFTemp = pd.concat([dataNFIncomeDFTemp, dataFIncomeDFTemp]).sort_index()
            dataTolItemDic[code] = dataDupIncomeDFTemp
        elif code in dataNFEComCode:
            dataTolItemDic[code] = dataNFItemUseDFInd.loc[code]
        else:
            dataTolItemDic[code] = dataFItemUseDFInd.loc[code]
            
    return dataTolItemDic





## 2.2 get statement item values

def dataYearEndItemValueGet(pathNF, pathF, item):  # item: u'NetProfit'

    
### 2.2.1 load non financial income data and financial income data
    # itemscolumns list we used     
     dataColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark']
     dataColUseLis.append(item)
    
    # create  a dict , contain all code data
    dataTolItemDic=dataSheetCombinDicGet(pathNF, pathF, item)  # path: string, item: string
    dataComCodeUseLis = sorted(dataTolItemDic.keys())
    
### 2.2.2 calculate item yearend value    
    # create a new df dict
    dataTolItemDicUse = {}   
    for number, code in enumerate(dataComCodeUseLis):    
        dfOneCode = dataTolItemDic[code]                              # df one code
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
                
                dfOneCodeUseTemp  = dfOneCodeUseTolRaw[dfOneCodeUseTolRaw[u'EndDate']==\
                                                       arrEndDate[yearEndDayInd[-1]]].drop_duplicates('EndDate', keep='last')
                dfOneCodeUse.loc[day] = dfOneCodeUseTemp.values.reshape(3,)
            else: 
                dfOneCodeUse.loc[day] = np.nan
                
        dataTolItemDicUse[code] = dfOneCodeUse 
                
    return dataTolItemDicUse


### 2.2.3 convert to three dimential arrays  

    # load data series
    dataTSArr = dataTimeSeriesDicGet()['dataTSArr']    # 6498
    
    # load code
    dataComCodeTol = dataCodeNumDicGet()['dataComCodeArr']   # 3415
    # items saved
    itemsLis = dataTolItemDicUse[dataComCodeUseLis[0]].columns.tolist()
    
    # create a dic contain all effective date data
    dataValuesDicTolTime = {}
    for code in dataComCodeTol:
        if code in dataComCodeUseLis:
            dataOneCodeTolDF = dataTolItemDicUse[code].sort_index()
            dataOneCodeTSRaw = dataOneCodeTolDF.index.tolist()
            dataOneCodeTSTol = sorted(set(dataTSArr) | set(dataOneCodeTSRaw))
            dataOneCodeUseDF = dataOneCodeTolDF.reindex(dataOneCodeTSTol, method='ffill').loc[dataTSArr]
            dataValuesDicTolTime[code] = dataOneCodeUseDF
        else:
            dataValuesDicTolTime[code] = pd.DataFrame(index=dataTSArr, columns=itemsLis)
        
    # save dataValuesDicTolTime  Values as 3D array   , total codes
    dataTolValuesArr = np.zeros((len(itemsLis), len(dataTSArr), len(dataComCodeTol)))           # use not financial codes

    for i, it in enumerate(itemsLis):
        for j, code in enumerate(dataComCodeTol):
            dataTolValuesArr[i, :, j] = dataValuesDicTolTime[code][it].values
    
    
    itemsNamesArr = np.zeros((1, len(itemsLis)), dtype=object)
    for i, j in enumerate(itemsLis):
        itemsNamesArr[0][i] = np.array([j])
    
    dataDic = {'axis1_itemNames': itemsNamesArr, \
               'axis2_indexTime': dataTSArr.reshape(len(dataTSArr), 1), \
               'axis3_colCompanyCode': dataComCodeTol, \
               'threeDimentionArray': dataTolValuesArr}
    return dataDic
    

def dataROEValueArrGet(pathNFIC, pathFIC, pathNFBL, pathFBL, itemIncome=[u'NetProfit'], \
                       itemBalance=[u'TotalShareholderEquity', u'DeferredTaxAssets', u'EPreferStock']):
    
    dataNetProDic = dataYearEndItemValueGet(pathNFIC, pathFIC, itemIncome[0])
    dataNetProValArr = dataNetProDic['threeDimentionArray'][2]
    dataNetProEndDateArr = dataNetProDic['threeDimentionArray'][0]
    
    dataEquityDic = dataYearEndItemValueGet(pathNFBL, pathFBL, itemBalance[1])
    dataEquityValArr = dataEquityDic['threeDimentionArray'][2]
    dataEquityEndDateArr = dataEquityDic['threeDimentionArray'][0]
    
    dataDefDic = dataYearEndItemValueGet(pathNFBL, pathFBL, itemBalance[0])
    dataDefValArr = dataDefDic['threeDimentionArray'][2]
    dataDefEndDateArr = dataDefDic['threeDimentionArray'][0]    
    
    dataEPDic = dataYearEndItemValueGet(pathNFBL, pathFBL, itemBalance[2])
    dataEPValArr = dataEPDic['threeDimentionArray'][2]
    dataEPEndDateArr = dataEPDic['threeDimentionArray'][0]    
    
    dataTSArr = dataTimeSeriesDicGet()['dataTSArr']    # 6498
    dataComCodeTol = dataCodeNumDicGet()['dataComCodeArr']   # 3415
    dataROEValArr = np.zeros((len(dataTSArr), len(dataComCodeTol)))
    dataROEEndDateArr = np.zeros((len(dataTSArr), len(dataComCodeTol)))
    
    for i in range(len(dataTSArr)):
        for j in range(len(dataComCodeTol)):
            if 
    
    
    


    






















