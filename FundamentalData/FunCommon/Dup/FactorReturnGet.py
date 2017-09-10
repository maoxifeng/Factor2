# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 15:13:11 2017

@author: liusl
"""



import numpy as np
import scipy.io as sio
import pandas as pd
import os
import time
import statsmodels.api as sm
import Common.TimeCodeGet as tc

# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)

def FactorFMReturnGet(dataLoadDic, savePath='', pool='A', facName='Factor'):
    
    #==============================================================================
    # 1. load data
    #==============================================================================
    ## factor year data convert to formative stocks
    
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
    pathStoLogRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_arr.mat'
    dataStoRetArr = sio.loadmat(pathStoLogRet)['StoLogReturn']
    
    ## load stock daily volumne
    pathVol = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_TurnoverVolume_arr.mat'
    dataVolRaw = sio.loadmat(pathVol)
    dataVolArr = dataVolRaw[u'TurnoverVolume']  # columns: inner code
    
    ## load stock AFloats
    pathAF = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/Afloats/LC_AFloats_mat.mat'
    dataAFloatsRaw = sio.loadmat(pathAF)
    dataAFloats3DArr = dataAFloatsRaw['LC_AFloats']
    dataAFloatsArr = dataAFloats3DArr[0]

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
    
    dataFactorReturnDF['HML'] = dataFactorReturnDF['high'] - dataFactorReturnDF['low']
    colNames = dataFactorReturnDF.columns.tolist()
    
    arrName = facName + '_' + pool + '_' + 'FMReturn'
    dataDic={'colNames': np.array(colNames, dtype=object), 
             'indDate': dataDSArr.reshape(len(dataDSArr), 1),
             arrName: dataFactorReturnDF.values.astype(float), \
             'arrKey': [arrName, 'indDate', 'colNames']}
             
    saveName = ''
    if savePath !='':
        saveName = savePath + '/' + arrName + '_array.mat'
        sio.savemat(saveName, dataDic)
        print 'file saved ~'    
    
    return dataFactorReturnDF, saveName
    
def FactorFMExposureGet(loadPath, regDays=250, per=0.2, index=3, saveBool=True, facName_Pool='Factor'):
    
    '''
    #==============================================================================
    # dataFactorReturnArr is based on the result of function FactorFMReturnGet() dataFactorReturnDF
    #==============================================================================    
    '''
    dataFactorReturnDic = sio.loadmat(loadPath)
        
    facArrKey = dataFactorReturnDic['arrKey'][0]
    dataFactorReturnArr = dataFactorReturnDic[facArrKey][:, index]    
    # load stock return
    ## load stoct daily returns
    pathStoLogRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_arr.mat'
    dataStoRetArr = sio.loadmat(pathStoLogRet)['StoLogReturn']
    # load free returns

    pathFreeRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Wind_Daily10YearBond_LogReturn_arr.mat'
    dataFreeRetArr = sio.loadmat(pathFreeRet)['TenYearBond_LogReturn']

    # stock free return !
    dataStoFreeRetArr = dataStoRetArr - dataFreeRetArr
        
    
    dataFactorExpArr = np.ones_like(dataStoFreeRetArr)
    dataFactorExpArr[:] = np.nan
    startNum = np.where((~np.isnan(dataFactorReturnArr)) & (~np.isnan(dataFreeRetArr[:, 0])))[0][0]
    startInd = startNum + regDays - 1
    
    print 'start calculate FM Exposure: ',
    print time.strftime("%H:%M:%S", time.localtime())
    print 'date', 'nowTime'
    for d in range(startInd, len(dataDSArr)):
        
        YTemp = dataStoFreeRetArr[(d-regDays+1):(d+1)]
        Xtemp = dataFactorReturnArr[(d-regDays+1):(d+1)]
        for s in range(len(dataInnerCodeArr)):
            useIndArr = np.where(~np.isnan(YTemp[:, s]))[0]
            if len(useIndArr) > (regDays * per):   # 
                result = sm.OLS(YTemp[useIndArr, s], Xtemp[useIndArr]).fit()
                dataFactorExpArr[d, s] = result.params[1]
        if d%100 == 0:
            print dataDSArr[d], time.strftime("%H:%M:%S", time.localtime())
            
    arrName = facName_Pool + '_FMExposure' + '_' + str(regDays) + 'RDs'
    dataDic={'colInnerCode': dataInnerCodeArr, 
             'indDate': dataDSArr.reshape(len(dataDSArr), 1),
                arrName: dataFactorExpArr, 
                'arrKey': [arrName, 'indDate', 'colInnerCode']}

    if saveBool :
        savePath = os.path.split(loadPath)[0]
        saveName = savePath + '/' + arrName + '_array.mat'
        sio.savemat(saveName, dataDic)
        print arrName + '_array.mat', 'saved ~'
    return dataFactorExpArr
    
    
    

def FactorBarraReturnGet(loadPath, index=0, pool='A', saveBool=True, facName='Factor'):
    
    
    '''
    load dataDic as follows:
    arrName = facName + 'Values_Three3DArray'    
    dataDic = {'axis1Names_Items': np.array(itemsLis, dtype=object),
               'axis2Names_DateSeries': dataDSArr.reshape(len(dataDSArr), 1),\
               'axis3Names_ComCode': dataComCodeArr,\
               arrName: data3DArr, \
               'arrKey': [arrName, 'axis1Names_Items', 'axis2Names_DateSeries', 'axis3Names_ComCode']}
    '''
    
    # load stock log return
    pathStoLogRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_array.mat'
    dataStoRet = sio.loadmat(pathStoLogRet)['StoLogReturn']
        
    # load free return, not use
#    pathFreeRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Wind_Daily10YearBond_LogReturn_array.mat'
#    dataFreeRet = sio.loadmat(pathFreeRet)['TenYearBond_LogReturn']

    # stock free return    
#    dataStoFreeRet = dataStoRet - dataFreeRet
    dataStoFreeRet = dataStoRet    # not need free stock return 
    
    # load Factor values    
    dataFactorValuesDic = sio.loadmat(loadPath)
    facArrKey = dataFactorValuesDic['arrKey'][0]
    dataFactorValues = dataFactorValuesDic[facArrKey]
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
        dataStoFreeRet = dataStoFreeRet * dataHS300IndexDF.values.astype(float)
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
        useBool = (~np.isnan(dataFactorStandArr[i])) & (~np.isnan(dataStoFreeRet[i]))
        Xuse = dataFactorStandArr[i][useBool]
        
        if len(Xuse)>olsCounts:        
            Yuse = dataStoFreeRet[i][useBool]
            X = sm.add_constant(Xuse)
            result = sm.OLS(Yuse, X).fit()
            dataFactorOLSReturn[i, 0] = result.params[1]
            if i%1000 == 0:
                print dataDSArr[i]
    arrName = facName + '_' + pool + '_' + 'BarraReturn'
    dataDic = {'indDate': dataDSArr.reshape(len(dataDSArr), 1), \
                arrName: dataFactorOLSReturn, 'arrKey': [arrName, 'indDate']}
    
    if saveBool :
        savePath = os.path.split(loadPath)[0]
        saveName = savePath + '/' + arrName + '_arr.mat'
        sio.savemat(saveName, dataDic)
        print arrName + '_arr.mat', 'saved'
    return dataFactorOLSReturn

    
    

#def SepGroRetGet(pathExp, pathFM):
    
    
    
    
    
    
    
    
    
    
    
    
    
    
          































