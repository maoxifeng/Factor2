# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 18:53:48 2017

@author: liusl
"""

import numpy as np
import scipy.io as sio
import pandas as pd
import os
import time
import statsmodels.api as sm
import Common.TimeCodeGet as tc
import Common.SmaFun as cs
import Common.UpdateDataGet as cu


# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)

def FactorFMReturnGet(dataLoadDic, savePath='', facName='Factor', pool='A'):
    
#    dataLoadDic = dataROEDic; savePath=ROESavePathMain; facName=facName;pool='A'
    #==============================================================================
    # 1. load data
    #==============================================================================
    # make dir
    facName = facName + '_FMReturn' + '_' + pool
    ROESavePath = savePath + facName + '/'
    dataLoadLis = dataLoadDic.values()
    for code in dataLoadDic.keys():
        dataLoadDic[code].columns = [code]
        
    dataLoadDF = pd.concat(dataLoadLis, axis=1)
    dataLoadDF = dataLoadDF.sort_index()
    
    # convert company code to innercode !
    dataAllDF = dataLoadDF.reindex(columns=dataComCodeArr)
    dataAllDF.columns = dataInnerCodeArr
    dataFactorYearUseDF = dataAllDF.dropna(how='all')
    
    ## load stoct daily returns
    pathStoLogRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/StoRet/'
    dataStoRetArr = cs.AllArrToDFGet(pathStoLogRet).values.astype(float)
    
    ## load stock daily volumne
    pathVol = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/TurnoverVolume/'
    dataVolArr = cs.AllArrToDFGet(pathVol).values.astype(float)  # columns: inner code
    
    ## load stock AFloats
    pathAF = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/AFloats/'
    dataAFloatsArr = cs.AllArrToDFGet(pathAF).values.astype(float)

    dataInnerCodeUseArr = dataInnerCodeArr  # seems not useless, just a mark
    dataYearUseLis = dataFactorYearUseDF.index.tolist()       # 27

    
    # constant
    thrNum = 100
    if pool == 'HS300':
        print 'HS300 pool'
        # load HS300 index  0/1 sheet
        thrNum = 15
        dataGroupDateLis = [(iyear*10000+430) for iyear in dataYearUseLis]  # +430 not 0430!!!
        
        dataHS300IndexDF = tc.codeIndexDFGet(codeStr='HS300')
        dataHS300IndexDF[dataHS300IndexDF==0] = np.nan
#        print dataHS300IndexDF
        dataHS300IndexYearDF = pd.DataFrame(index=dataYearUseLis, columns=dataInnerCodeUseArr)
        for iyear, iyearDate in zip(dataYearUseLis, dataGroupDateLis):
            dataHS300IndexYearDF.loc[iyear] = dataHS300IndexDF.loc[:iyearDate].iloc[-1].values
            
        dataFactorYearUseDF = dataFactorYearUseDF * dataHS300IndexYearDF        
        dataFactorYearUseDF =  dataFactorYearUseDF.dropna(how='all')       
        dataYearUseLis = dataFactorYearUseDF.index.tolist()

        dataHS300IndexArr = dataHS300IndexDF.values.astype(float)
        dataStoRetArr = dataStoRetArr * dataHS300IndexArr
        dataVolArr = dataVolArr * dataHS300IndexArr
        dataAFloatsArr = dataAFloatsArr * dataHS300IndexArr
        
#        dataInnerCodeUseArr = dataInnerCodeArr[select]
    #==============================================================================
    # 2. seperate 3 groups        
    #==============================================================================
    
    groupLowFactorDic = {}
    groupMedFactorDic = {}
    groupHigFactorDic = {}
    groupAllFactorDic = {}
    
    #dfpercent2 = dataFactorYearDF.quantile([0.3, 0.75], axis=1).T   #  why? !!!
    dfpercent = pd.DataFrame(index=dataYearUseLis, columns=[0.3, 0.7])
    for year in dataYearUseLis:
        dfpercent.loc[year] = dataFactorYearUseDF.loc[year].quantile([0.3, 0.7])
        
    for year in dataYearUseLis:
        dataFactorYearUseTemp = dataFactorYearUseDF.loc[year]
        if len(dataFactorYearUseTemp.dropna()) >= thrNum:  # keep stocks groups when counts >=100
            groupAllFactorDic[year] = dataFactorYearUseTemp.dropna().index.tolist()
            per = dfpercent.loc[year]
            groupLowFactorDic[year] = dataFactorYearUseTemp[dataFactorYearUseTemp<=per[0.3]].index.tolist()
            groupMedFactorDic[year] = dataFactorYearUseTemp[(dataFactorYearUseTemp>=per[0.3]) & (dataFactorYearUseTemp<per[0.7])].index.tolist()
            groupHigFactorDic[year] = dataFactorYearUseTemp[dataFactorYearUseTemp>=per[0.7]].index.tolist()
    
    threeGroupsDic = {'low': groupLowFactorDic, 'median': groupMedFactorDic, 'high':groupHigFactorDic, 'all':groupAllFactorDic}
    
    #==============================================================================
    # 3. calculate the Factor value-weighted stock return
    #==============================================================================
    yearGroupLis = sorted(threeGroupsDic['low'].keys())
    
    ## calculate grouped Factor daily return
    
    dataVolUseArr = np.zeros((len(dataDSArr), len(dataInnerCodeUseArr)))
    dataReturnUseArr = np.zeros((len(dataDSArr), len(dataInnerCodeUseArr)))
    dataAFloatsUseArr = np.zeros((len(dataDSArr), len(dataInnerCodeUseArr)))
    dataReturnUseArr[:] = np.nan
    dataVolUseArr[:] = np.nan
    dataAFloatsUseArr[:] = np.nan
    
    #bool1Arr = np.where((~np.isnan(dataVolArr[1])) & (dataVolArr[1]!=0))
    for i in range(len(dataDSArr)):
        posUseArr = np.where((~np.isnan(dataVolArr[i])) & (dataVolArr[i]!=0))[0]
        if len(posUseArr) == 0:
            continue
        dataVolUseArr[i][posUseArr] = dataVolArr[i][posUseArr]
        dataReturnUseArr[i][posUseArr] = dataStoRetArr[i][posUseArr]
        dataAFloatsUseArr[i][posUseArr] = dataAFloatsArr[i][posUseArr]
    
    dataReturnDF = pd.DataFrame(dataReturnUseArr, index=dataDSArr, columns=dataInnerCodeUseArr)
    dataAFloatsDF = pd.DataFrame(dataAFloatsUseArr, index=dataDSArr, columns=dataInnerCodeUseArr)
    
    # three groups return
    dataFactorReturnDF = pd.DataFrame([], index=dataDSArr, columns=['low', 'median', 'high', 'HML'])    
    counts = 0
    
    print 'start divide group', time.strftime("%H:%M:%S", time.localtime())
    print 'date'
    for year in yearGroupLis:
        groupTemLis = [threeGroupsDic[i][year] for i in ['low', 'median', 'high']]
        for date in dataDSArr[(dataDSArr>(year*10000+430)) & (dataDSArr<((year+1)*10000+501))]:
            for i, group in enumerate(groupTemLis):
                dataOGTemDF = pd.DataFrame(index=group, columns=['return', 'aFloats', 'weight', 'wReturn'])
                dataOGTemDF['return'] = dataReturnDF.loc[date][group]
                dataOGTemDF['aFloats'] = dataAFloatsDF.loc[date][group]
                dataOGTemDF['weight'] = dataOGTemDF['aFloats'] / dataOGTemDF['aFloats'].sum()
                dataOGTemDF['wReturn'] = dataOGTemDF['return'] * dataOGTemDF['weight']				
                dataFactorReturnDF.loc[date].iloc[i] = dataOGTemDF['wReturn'].sum()
            counts = counts + 1    
            if counts%50 == 0:
                print date, 
    print '\n'
    dataFactorReturnDF['HML'] = dataFactorReturnDF['high'] - dataFactorReturnDF['low']
#    a = 0
    cu.UpdateItemDataGet(dataFacDF=dataFactorReturnDF,  facSavePath=ROESavePath, facName=facName)
        
    return ROESavePath
    
def FactorFMExposureGet(facReturnPath, facName, pool, regDays=250, per=0.2, index=3):
#    facReturnPath=ROEReturnFolderPath; facName=facName; pool='A'; regDays=250; per=0.2; index=3
    '''
    #==============================================================================
    # dataFactorReturnArr is based on the result of function FactorFMReturnGet() dataFactorReturnDF
    #==============================================================================    
    '''
#    facReturnPath = ROEHS30ReturnPath
    returnPath = facReturnPath.rstrip('/')
    facPath = os.path.split(returnPath)[0] + '/'
    facName = facName + '_FMExposure' + '_' + pool

#    facName=factName
    dataFactorReturnArr = cs.ItemAllArrToDFGet(facReturnPath).values.astype(float)[:, index]
    # load stock return
    ## load stoct daily returns
    pathStoLogRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/StoRet/'
    dataStoRetArr = cs.AllArrToDFGet(pathStoLogRet).values.astype(float)
    # load free returns

    pathFreeRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/BondReturn/'
    dataFreeRetArr = cs.AllArrToDFGet(pathFreeRet).values.astype(float)

    # stock free return !
    dataStoFreeRetArr = dataStoRetArr - dataFreeRetArr
        
    
    dataFactorExpArr = np.ones_like(dataStoFreeRetArr)
    dataFactorExpArr[:] = np.nan
    startNum = np.where((~np.isnan(dataFactorReturnArr)) & (~np.isnan(dataFreeRetArr[:, 0])))[0][0]
    startInd = startNum + regDays - 1
    
    print 'start calculate FM Exposure: ',
    print time.strftime("%H:%M:%S", time.localtime())
    print 'date', 'nowTime'
    
    dataFactorReturnArr = sm.add_constant(dataFactorReturnArr)
    
    for d in range(startInd, len(dataDSArr)):
        
        YTemp = dataStoFreeRetArr[(d-regDays+1):(d+1)]
        XTemp = dataFactorReturnArr[(d-regDays+1):(d+1)]
        for s in range(len(dataInnerCodeArr)):
            useIndArr = np.where(~np.isnan(YTemp[:, s]))[0]
            if len(useIndArr) > (regDays * per):   # 
                result = sm.OLS(YTemp[useIndArr, s], XTemp[useIndArr]).fit()
                dataFactorExpArr[d, s] = result.params[1]
        if d%100 == 0:
            print dataDSArr[d], time.strftime("%H:%M:%S", time.localtime())
    dataFactorExpDF = pd.DataFrame(dataFactorExpArr, index=dataDSArr, columns=dataInnerCodeArr)
    cu.UpdateFormDataGet(dataFactorExpDF, facPath, facName)
            
    return 
    
    
    

def FactorBarraReturnGet(loadDF, facPath, facName='Factor', pool='A', index=0):
    
    
    '''
    load dataDic as follows:
    arrName = facName + 'Values_Three3DArray'    
    dataDic = {'axis1Names_Items': np.array(itemsLis, dtype=object),
               'axis2Names_DateSeries': dataDSArr.reshape(len(dataDSArr), 1),\
               'axis3Names_ComCode': dataComCodeArr,\
               arrName: data3DArr, \
               'arrKey': [arrName, 'axis1Names_Items', 'axis2Names_DateSeries', 'axis3Names_ComCode']}
    '''
    
    facName = facName + '_BarraReturn_' +  pool
    
    # load stock log return
    pathStoLogRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/StoRet/'
    dataStoRetArr = cs.AllArrToDFGet(pathStoLogRet).values.astype(float)
        
    # load Factor values    
    dataFactorValues = loadDF.values.astype(float)
    if dataFactorValues.ndim == 3 :
        dataFactorValues = dataFactorValues[index]    
    
    
    olsCounts = 200
    # select stock pool
    if pool == 'HS300':    
        print 'HS300 pool'
        # load HS300 index  0/1 sheet
        olsCounts = 20 # regression sample counts
        
        dataHS300IndexDF = tc.codeIndexDFGet(codeStr='HS300')
        dataHS300IndexDF[dataHS300IndexDF==0] = np.nan
#        print dataHS300IndexDF
        dataStoRetArr = dataStoRetArr * dataHS300IndexDF.values.astype(float)
        dataFactorValues = dataFactorValues * dataHS300IndexDF.values.astype(float)
    
    # factor values standardize
    dataFactorStandArr = np.zeros_like(dataFactorValues)
    dataFactorStandArr[:] = np.nan

    for i in range(len(dataFactorValues)):
        dataFactorValueTemp = dataFactorValues[i][~np.isnan(dataFactorValues[i])]
        if len(dataFactorValueTemp) >=2:
            dataMeanTemp = np.mean(dataFactorValueTemp)
            dataStdTemp = np.std(dataFactorValueTemp)
            dataFactorStandArr[i] = (dataFactorValues[i] - dataMeanTemp) / dataStdTemp
    
    # OLS   calculate cross section factor return    
        
    dataFactorOLSReturn = np.zeros((len(dataFactorStandArr), 1))        
    dataFactorOLSReturn[:] = np.nan
    
    print 'start calculate Barra return'        
    print time.strftime("%H:%M:%S", time.localtime())
    print 'dateCounts', 'date'
    for i in range(len(dataFactorStandArr)):        
        useBool = (~np.isnan(dataFactorStandArr[i])) & (~np.isnan(dataStoRetArr[i]))
        Xuse = dataFactorStandArr[i][useBool]
        
        if len(Xuse)>olsCounts:        
            Yuse = dataStoRetArr[i][useBool]
            X = sm.add_constant(Xuse)
            result = sm.OLS(Yuse, X).fit()
            dataFactorOLSReturn[i, 0] = result.params[1]
            if i%1000 == 0:
                print dataDSArr[i]
    dataBarraRetDF = pd.DataFrame(dataFactorOLSReturn, index=dataDSArr, columns=[facName])
    cu.UpdateItemDataGet(dataBarraRetDF, facPath, facName)           
                
    return dataFactorOLSReturn

    
