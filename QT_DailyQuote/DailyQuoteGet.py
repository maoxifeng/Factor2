# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 13:35:40 2017

@author: liusl
"""


'''
#==============================================================================
# fetch ItemAll data
#==============================================================================
'''

import numpy as np
import scipy.io as sio
import pandas as pd
import Common.TimeCodeGet as tc
import os
import Common.SmaFun as cs


dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)

itemsAllLis = [u'ID',
             u'InnerCode',
             u'TradingDay',
             u'PrevClosePrice',
             u'OpenPrice',
             u'HighPrice',
             u'LowPrice',
             u'ClosePrice',
             u'TurnoverVolume',
             u'TurnoverValue',
             u'TurnoverDeals',
             u'XGRQ',
             u'JSID']

savePath='/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/'  # DailyQuote factors saved path

def DailyQuoteGet(item):
    
    pathQTDaily = '/data/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/'
    fileNameLis = os.listdir(pathQTDaily)   
    fileNameDic = {float(filter(str.isdigit, ifile)): ifile for ifile in fileNameLis}
    fileYearLis = sorted(fileNameDic.keys())
    
    
    if item in itemsAllLis:    
        print item, 'daily quote get:'
        itmeSavePath = savePath + item + '/'
        
        if not os.path.exists(itmeSavePath):
            os.mkdir(itmeSavePath)             
    

    if len(os.listdir(itmeSavePath)) == 1:
        os.remove(itmeSavePath + os.listdir(itmeSavePath)[0])
        
    saveFileNameLis = os.listdir(itmeSavePath)
    
    print saveFileNameLis
#    saveFileNameLis = [str(ifile) for ifile in os.listdir(itmeSavePath)]   # !!!
    
    saveFileNameDic = {float(filter(str.isdigit, ifile)): ifile for ifile in saveFileNameLis}
    saveFileYearLis = sorted(saveFileNameDic.keys())

            
    # past year data
    if len(saveFileYearLis) == 0:
        print 'past year data:'
        dailyPastDic = {}    
        for ifileName in fileYearLis[:-1]:   
            ifilePath = pathQTDaily + fileNameDic[ifileName]
            print ifileName
            dataPastRaw = cs.SheetToDFGet(ifilePath)
            dataPastCol = [u'TradingDay', u'InnerCode', item]
            
            dataPastDFTol = dataPastRaw[dataPastCol]
            dataPastDFUse = dataPastDFTol[dataPastDFTol[u'InnerCode'].isin(dataInnerCodeArr)]
            
            dataPastDFUseSort = dataPastDFUse.sort_values(by=u'TradingDay')
            dataPastDFUseSort.set_index([u'TradingDay', u'InnerCode'], inplace=True)
            
            dataPastDF = dataPastDFUseSort[item].unstack()
            dailyPastDic[ifileName] = dataPastDF
        # conbine and order
        dataPastItemAllDF = pd.concat(dailyPastDic.values())
        dataPastItemAllSortDF = dataPastItemAllDF.sort_index()
        
        # delete duplicated data, and convert to formative array
        dataPastItemAllUse = dataPastItemAllSortDF[~dataPastItemAllSortDF.index.duplicated()]
        
        pastYear = int(dataPastItemAllUse.index[-1]) / 10000
        dataPastDSUseArr = dataDSArr[dataDSArr<(pastYear+1)*10000]  # date series used
        
        dataPastItemAllUseDF = dataPastItemAllUse.loc[dataPastDSUseArr]
        dataPastInnerCodeUseArr = [code for code in dataInnerCodeArr if code in dataPastItemAllUseDF.columns]  # inner code used
        
        dataPastItemAllUseDF = dataPastItemAllUseDF.reindex(columns = dataPastInnerCodeUseArr)
        dataPastItemAllUseArr = dataPastItemAllUseDF.values.astype(float)            
        
        dataPastDic = {'colInnerCode': dataPastInnerCodeUseArr, \
                       'indDate': dataPastDSUseArr.reshape(len(dataPastDSUseArr), 1), \
                       item: dataPastItemAllUseArr,
                       'arrKey': [item, 'indDate', 'colInnerCode']}
        fileSavePathName = itmeSavePath + 'DailyQuote_To' + str(pastYear) + '_' + item + '_arr.mat'
        sio.savemat(fileSavePathName, dataPastDic)
        print pastYear, 'past year data saved!'

    # this year data
    
    dataCol = [u'TradingDay', u'InnerCode', item]
    filePath = pathQTDaily + fileNameDic[fileYearLis[-1]]
    dataRaw = cs.SheetToDFGet(filePath)
    toYear = int(dataRaw[u'TradingDay'].iloc[0]) / 10000
    print toYear
        
    dataDFUse = dataRaw[dataCol]
    dataDFUseSort = dataDFUse.sort_values(by=u'TradingDay')
    dataDFUseSort.set_index([u'TradingDay', u'InnerCode'], inplace=True)
    dataDF = dataDFUseSort[item].unstack()
                                
    dataItemAllSortDF = dataDF.sort_index()
    dataItemAllUse = dataItemAllSortDF[~dataItemAllSortDF.index.duplicated()]
    
    dataDSUseArr = dataDSArr[dataDSArr>(toYear*10000)]  # date series used
    dataItemAllUseDF = dataItemAllUse.loc[dataDSUseArr]   # 
    
    dataItemAllUseDF = dataItemAllUseDF.reindex(columns = dataInnerCodeArr)    
    dataItemAllUseArr = dataItemAllUseDF.values.astype(float)
    
    
    dataDic = {'colInnerCode': dataInnerCodeArr, \
               'indDate': dataDSUseArr.reshape(len(dataDSUseArr), 1), \
               item: dataItemAllUseArr, 
               'arrKey': [item, 'indDate', 'colInnerCode']}
    fileSavePathName = itmeSavePath + 'DailyQuote_' + str(toYear)+ '_' + item + '_arr.mat'
    sio.savemat(fileSavePathName, dataDic)
    print str(toYear) + ' Year data saved'
    
    if (len(saveFileYearLis) >= 2) & (toYear == (saveFileYearLis[-1] + 1)):
        filePath = pathQTDaily + fileNameDic[fileYearLis[-2]]
        dataRaw = cs.SheetToDFGet(filePath)
        pastYear = int(saveFileYearLis[-1])
                
        dataDFUse = dataRaw[dataCol]
        dataDFUseSort = dataDFUse.sort_values(by=u'TradingDay')
        dataDFUseSort.set_index([u'TradingDay', u'InnerCode'], inplace=True)
        dataDF = dataDFUseSort[item].unstack()
                                    
        dataItemAllSortDF = dataDF.sort_index()
        dataItemAllUse = dataItemAllSortDF[~dataItemAllSortDF.index.duplicated()]
        
        dataDSUseArr = dataDSArr[(dataDSArr>(pastYear*10000)) * (dataDSArr<(toYear*10000))]  # date series used
        dataItemAllUseDF = dataItemAllUse.loc[dataDSUseArr]   # 
        
        dataItemAllUseDF = dataItemAllUseDF.reindex(columns = dataInnerCodeArr)    
        dataItemAllUseArr = dataItemAllUseDF.values.astype(float)
        
        
        dataDic = {'colInnerCode': dataInnerCodeArr, \
                   'indDate': dataDSUseArr.reshape(len(dataDSUseArr), 1), \
                   item: dataItemAllUseArr, 
                   'arrKey': [item, 'indDate', 'colInnerCode']}
        fileSavePathName = itmeSavePath + 'DailyQuote_' + str(pastYear)+ '_' + item + '_arr.mat'
        sio.savemat(fileSavePathName, dataDic)
        print str(pastYear) + ' Year data saved'

        
    return dataDic


    
def RAFactorGet():
    '''RatioAdjusting Factors'''
    # every time calculate all date
    pathRAFactor = '/data/liushuanglong/MyFiles/Data/JYDB2/QT_AdjustingFactor/QT_AdjustingFactor.mat'

    itmeSavePath = savePath + 'RatioAdjustingFactor/'
    if not os.path.exists(itmeSavePath):
        os.mkdir(itmeSavePath)            
        
    dataRADF = cs.SheetToDFGet(pathRAFactor)
    dataCol = [u'ExDiviDate', u'RatioAdjustingFactor', u'InnerCode']
    dataDFTol = dataRADF[dataCol]
    
    # transpose and fillna
    dataDFUse = dataDFTol[dataDFTol[u'InnerCode'].isin(dataInnerCodeArr)]
    dataDFUseSort = dataDFUse.sort_values(by=[u'ExDiviDate', u'InnerCode'])
    dataDFUseSta = dataDFUseSort.set_index([u'ExDiviDate', u'InnerCode'])[u'RatioAdjustingFactor'].unstack()
    dataDFUseFil = dataDFUseSta.fillna(method='ffill')
    dataDFUseFilTol = dataDFUseFil.fillna(1.)
    
    # total time fillna\
    dataUseTolTime = dataDFUseFilTol.loc[dataDSArr]      # this way may be good~
    dataUseTolTimeFil = dataUseTolTime.fillna(method='ffill')
    dataUseTolTimeFil = dataUseTolTimeFil.fillna(1.)
    
    # total InnerCode fillna
    dataUseTolFil = dataUseTolTimeFil.reindex(columns=dataInnerCodeArr, fill_value=1.)
    
    # calculate adjusting factors
    dataAdFactors = dataUseTolFil / dataUseTolFil.iloc[-1]
    
    # save data
    dataDic = {'colInnerCode': dataInnerCodeArr, \
               'indDate': dataDSArr.reshape(len(dataDSArr), 1), \
               'RatioAdjustingFactor': dataAdFactors.values.astype(float),\
               'arrKey': ['RatioAdjustingFactor', 'indDate', 'colInnerCode']}
    sio.savemat(itmeSavePath + 'RatioAdjustingFactor_arr.mat', dataDic)
    return dataDic

            
def AdjCloseGet():
    
    # every time calculate all date 
    facName = 'AdjClosePrice'
    pathCloseDaily = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/ClosePrice/'
    fileNameLis = os.listdir(pathCloseDaily)   
    
       
    itemSavePath = savePath + facName + '/'
    if not os.path.exists(itemSavePath):
        os.mkdir(itemSavePath)             
    
    dfLis = []
    for ifile in fileNameLis:
        ifilePath = pathCloseDaily + ifile
        tempDic = sio.loadmat(ifilePath)
        arrKey = tempDic['arrKey']
        arrKey = [key.split()[0] for key in arrKey]
        tempDF = pd.DataFrame(tempDic[arrKey[0]], index=tempDic[arrKey[1]][:, 0], columns=tempDic[arrKey[2]][0])
        dfLis = dfLis + [tempDF]
    
    dataCloseAllDF = pd.concat(dfLis).reindex(index=dataDSArr, columns=dataInnerCodeArr)
    dataCloseAllArr = dataCloseAllDF.values.astype(float)
    dataRAFactorDic = sio.loadmat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/RatioAdjustingFactor/RatioAdjustingFactor_arr.mat')
    arrKey = dataRAFactorDic['arrKey']
    dataRAFactorDF = dataRAFactorDic[arrKey[0]]
    
    dataAdjCloseArr = dataCloseAllArr * dataRAFactorDF.values.astype(float)
    dataDic = {'colInnerCode': dataInnerCodeArr,
               'indDate': dataDSArr.reshape(len(dataDSArr), 1), 
                facName: dataAdjCloseArr, 
                'arrKey': [facName, 'indDate', 'colInnerCode']}
    itemSaveName = itemSavePath + facName + '_arr.mat'
    sio.savemat(itemSaveName, dataDic)
    return dataDic
            
            
            
def StoReturnGet():
    '''all depend on adjusted close price'''
    
    facName = 'StoRet'
    print facName
    pathAdjClose = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/AdjClosePrice/AdjClosePrice_arr.mat'    
    
    # load adjusted close price, convert to df        
    dataAdjCloseRawDic = sio.loadmat(pathAdjClose)
    arrKey = dataAdjCloseRawDic['arrKey']
    arrKey = [key.split()[0] for key in arrKey]
    dataDSAllArr = dataAdjCloseRawDic[arrKey[1]][:, 0]
    dataInnerCodeAllArr = dataAdjCloseRawDic[arrKey[2]][0]
    dataAdjCloseAllArr = dataAdjCloseRawDic[arrKey[0]]
    dataAdjCloseAllDF = pd.DataFrame(dataAdjCloseAllArr, index=dataDSAllArr, 
                                     columns=dataInnerCodeAllArr)
    # year used
    toYear = int(dataAdjCloseAllDF.index[-1])/10000
    toYearFirInd = np.where(dataDSAllArr > toYear*10000)[0][0]
#    toYearFir = dataDSAllArr[toYearFirInd]
    
    pastYear = toYear - 1
    pastYearLasInd = toYearFirInd - 1
    pastYearLas = dataDSAllArr[pastYearLasInd]
    # save folder
    facSavePath = savePath + facName + '/'
    if not os.path.exists(facSavePath):
        os.mkdir(facSavePath)             

    # delete useless data
    if len(os.listdir(facSavePath)) == 1:
        os.remove(facSavePath + os.listdir(facSavePath)[0])

    # get file year
    fileNameLis = os.listdir(facSavePath)   
    fileNameDic = {float(filter(str.isdigit, ifile)): ifile for ifile in fileNameLis}
    fileYearLis = sorted(fileNameDic.keys())    
    
    ## main context
    if toYear in fileYearLis:
        # update data
        print 'update 2017 data'
        # load 2017 data
        toYearPath = facSavePath + fileNameDic[toYear]
        dataOldStoRetDF = cs.ForArrToDFGet(toYearPath)
        oldDateEnd = dataOldStoRetDF.index[-1]
        
        if oldDateEnd == dataDSAllArr[-1]:
            print 'already updated'
            
        else:
            dataAdjCloseDF = dataAdjCloseAllDF.loc[oldDateEnd:]
            dataAdjCloseArr = dataAdjCloseDF.values
            dataAddStoRetArr = np.zeros((len(dataAdjCloseArr), len(dataInnerCodeAllArr)))
            dataAddStoRetArr[:] = np.nan
            
            # calculate formula
            dataAddStoRetArr[1:] = np.log(dataAdjCloseArr[1:]) - np.log(dataAdjCloseArr[:-1])        
            dataAddStoRetArr = dataAddStoRetArr[1:]
            dataStoRetDF = dataOldStoRetDF.reindex(index=dataDSAllArr[toYearFirInd:], columns=dataInnerCodeAllArr)
            dataAddDSArr = dataDSAllArr[dataDSAllArr>oldDateEnd]
            dataStoRetDF.loc[dataAddDSArr] = dataAddStoRetArr
            dataStoRetArr = dataStoRetDF.values.astype(float)
            dataDic = {'colInnerCode': dataInnerCodeAllArr,  # depend on adj close innercode 
                    'indDate': dataDSAllArr[toYearFirInd:].reshape(len(dataDSAllArr[toYearFirInd:]), 1), # depend on adj close date 
                    facName: dataStoRetArr, 
                    'arrKey': [facName, 'indDate', 'colInnerCode']}        
            facSavePathName = facSavePath + facName + '_' + str(toYear) + '_arr.mat'
            sio.savemat(facSavePathName, dataDic)
            print '2017 file updated'    

        
    else:
        print 'create 2017 file'
        # create 2017 file
        dataAdjCloseArr = dataAdjCloseAllArr[pastYearLasInd:]
        dataStoRetArr = np.zeros((len(dataAdjCloseArr)-1, len(dataInnerCodeAllArr)))
        dataStoRetArr[:] = np.nan
        
        # calculate formula
        dataStoRetArr = np.log(dataAdjCloseArr[1:]) - np.log(dataAdjCloseArr[:-1])        
        dataDic = {'colInnerCode': dataInnerCodeAllArr,  # depend on adj close innercode 
                    'indDate': dataDSAllArr[toYearFirInd:].reshape(len(dataDSAllArr[toYearFirInd:]), 1), # depend on adj close date 
                    facName: dataStoRetArr, 
                    'arrKey': [facName, 'indDate', 'colInnerCode']}        
        facSavePathName = facSavePath + facName + '_' + str(toYear) + '_arr.mat'
        sio.savemat(facSavePathName, dataDic)
        print '2017 file created'
    
        if pastYear in fileYearLis:
            print 'update 2016 file'
            pastYearPath = facSavePath + fileNameDic[pastYear]
            dataPastOldStoRetDF = cs.ForArrToDFGet(pastYearPath)
            pastOldDateEnd = dataPastOldStoRetDF.index[-1]
            if pastOldDateEnd == pastYearLas:
                print 'do not need to update 2016 file'
            else:
                
                dataPastAdjCloseDF = dataAdjCloseAllDF.loc[pastOldDateEnd:pastYearLas]
                dataPastAdjCloseArr = dataPastAdjCloseDF.values
                dataPastAddStoRetArr = np.zeros((dataPastAdjCloseArr.shape[0], dataPastAdjCloseArr.shape[1]))
                dataPastAddStoRetArr[:] = np.nan
                # calculate formula
                dataPastAddStoRetArr[1:] = np.log(dataPastAdjCloseArr[1:]) - np.log(dataPastAdjCloseArr[:-1])        
                dataPastAddStoRetArr = dataPastAddStoRetArr[1:]
                
                dataPastDSArr = dataDSAllArr[(dataDSAllArr>(pastYear*10000)) & (dataDSAllArr<(toYear*10000))]
                dataPastStoRetDF = dataPastOldStoRetDF.reindex(index=dataPastDSArr, columns=dataInnerCodeAllArr)
                dataPastAddDSArr = dataPastDSArr[dataPastDSArr>pastOldDateEnd]
                dataPastStoRetDF.loc[dataPastAddDSArr] = dataPastAddStoRetArr
                dataPastStoRetArr = dataPastStoRetDF.values.astype(float)
                pastDataDic = {'colInnerCode': dataInnerCodeAllArr,  # depend on adj close innercode 
                        'indDate': dataPastDSArr.reshape(len(dataPastDSArr), 1), # depend on adj close date 
                        facName: dataPastStoRetArr, 
                        'arrKey': [facName, 'indDate', 'colInnerCode']}        
                facSavePathName = facSavePath + facName + '_' + str(pastYear) + '_arr.mat'
                sio.savemat(facSavePathName, pastDataDic)
                print '2016 file updated'    

        else:
            print 'create to2016 file'
            
            # create to 2016 file    
            dataPastAdjCloseDF = dataAdjCloseAllDF.loc[:pastYearLas].dropna(axis=1, how='all')
            dataPastDSArr = dataDSAllArr[dataDSAllArr<=pastYearLas]
            dataPastAdjCloseArr = dataPastAdjCloseDF.values.astype(float)
            dataPastStoRetArr = np.zeros_like(dataPastAdjCloseArr)
            dataPastStoRetArr[:] = np.nan
            dataPastStoRetArr[1:] = np.log(dataPastAdjCloseArr[1:]) - np.log(dataPastAdjCloseArr[:-1])        
            pastDataDic = {'colInnerCode': dataPastAdjCloseDF.columns.tolist(),
                           'indDate': dataPastDSArr.reshape(len(dataPastDSArr), 1),
                            facName: dataPastStoRetArr, 
                            'arrKey': [facName, 'indDate', 'colInnerCode']}
            pastSavePathName = facSavePath + facName + '_To' + str(pastYear) + '_arr.mat'
            sio.savemat(pastSavePathName, pastDataDic)
            print 'to2016 file created'
            
        # end 
        
    
    
    
                





































