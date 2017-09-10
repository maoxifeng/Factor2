# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 15:58:15 2017

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



# load time and code 
dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)
dataComCodeArr = tc.codeDFGet().iloc[:, 1].values.astype(float)



def UpdateFormDataGet(dataFacDF, savePath, facName):
    
    # year used
    toYear = int(dataDSArr[-1])/10000
    toYearFirInd = np.where(dataDSArr > toYear*10000)[0][0]
    toYearFir = dataDSArr[toYearFirInd]
    
    pastYear = toYear - 1
    pastYearLasInd = toYearFirInd - 1
    pastYearLas = dataDSArr[pastYearLasInd]
    # save folder
    facSavePath = savePath + '/' + facName + '/'
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
        dataOldFacDF = cs.ForArrToDFGet(toYearPath)
        oldDateEnd = dataOldFacDF.index[-1]
        
        if oldDateEnd == dataDSArr[-1]:
            print 'already updated'
            
        else:
            # calculate formula
            dataNewFacDF = dataOldFacDF.reindex(index=dataDSArr[toYearFirInd:], columns=dataInnerCodeArr)
            dataAddDSArr = dataDSArr[dataDSArr>oldDateEnd]
            dataNewFacDF.loc[dataAddDSArr] = dataFacDF.loc[dataAddDSArr]
            dataNewFacArr = dataNewFacDF.values.astype(float)
            dataDic = {'colInnerCode': dataInnerCodeArr,  # depend on adj close innercode 
                    'indDate': dataDSArr[toYearFirInd:].reshape(len(dataDSArr[toYearFirInd:]), 1), # depend on adj close date 
                    facName: dataNewFacArr, 
                    'arrKey': [facName, 'indDate', 'colInnerCode']}        
            facSavePathName = facSavePath + facName + '_' + str(toYear) + '_arr.mat'
            sio.savemat(facSavePathName, dataDic)
            print '2017 file updated'    

        
    else:
        print 'create 2017 file'
        # create 2017 file
        
        dataNewFacDF = dataFacDF.loc[toYearFir:]
        dataNewFacArr = dataNewFacDF.values.astype(float)
        dataDic = {'colInnerCode': dataInnerCodeArr,  # depend on adj close innercode 
                    'indDate': dataDSArr[toYearFirInd:].reshape(len(dataDSArr[toYearFirInd:]), 1), # depend on adj close date 
                    facName: dataNewFacArr, 
                    'arrKey': [facName, 'indDate', 'colInnerCode']}        
        facSavePathName = facSavePath + facName + '_' + str(toYear) + '_arr.mat'
        sio.savemat(facSavePathName, dataDic)
        print '2017 file created'
    
        if pastYear in fileYearLis:
            print 'update 2016 file'
            pastYearPath = facSavePath + fileNameDic[pastYear]
            dataPastOldFacDF = cs.ForArrToDFGet(pastYearPath)
            pastOldDateEnd = dataPastOldFacDF.index[-1]
            if pastOldDateEnd == pastYearLas:
                print 'do not need to update 2016 file'
            else:
                dataPastDSArr = dataDSArr[(dataDSArr>(pastYear*10000)) & (dataDSArr<(toYear*10000))]
                dataPastFacDF = dataPastOldFacDF.reindex(index=dataPastDSArr, columns=dataInnerCodeArr)
                dataPastAddDSArr = dataPastDSArr[dataPastDSArr>pastOldDateEnd]
                dataPastFacDF.loc[dataPastAddDSArr] = dataFacDF.loc[pastOldDateEnd:pastYearLas]
                dataPastFacArr = dataPastFacDF.values.astype(float)
                pastDataDic = {'colInnerCode': dataInnerCodeArr,  # depend on adj close innercode 
                        'indDate': dataPastDSArr.reshape(len(dataPastDSArr), 1), # depend on adj close date 
                        facName: dataPastFacArr, 
                        'arrKey': [facName, 'indDate', 'colInnerCode']}        
                facSavePathName = facSavePath + facName + '_' + str(pastYear) + '_arr.mat'
                sio.savemat(facSavePathName, pastDataDic)
                print '2016 file updated'    

        else:
            print 'create to2016 file'
            
            # create to 2016 file    
            dataPastFacDF = dataFacDF.loc[:pastYearLas]
            dataPastDSArr = dataDSArr[dataDSArr<=pastYearLas]
            dataPastFacArr = dataPastFacDF.values.astype(float)
            pastDataDic = {'colInnerCode': dataPastFacDF.columns.tolist(),
                           'indDate': dataPastDSArr.reshape(len(dataPastDSArr), 1),
                            facName: dataPastFacArr, 
                            'arrKey': [facName, 'indDate', 'colInnerCode']}
            pastSavePathName = facSavePath + facName + '_To' + str(pastYear) + '_arr.mat'
            sio.savemat(pastSavePathName, pastDataDic)
            print 'to2016 file created'
 
    return None
(wfwfw)

def UpdateItemDataGet(dataFacDF, savePath, facName):
    
#    dataFacDF=dataFactorReturnDF; facName=facName;facSavePath=ROESavePath
    # year used
    
    toYear = int(dataDSArr[-1])/10000
    toYearFirInd = np.where(dataDSArr > toYear*10000)[0][0]
    toYearFir = dataDSArr[toYearFirInd]
    
    pastYear = toYear - 1
    pastYearLasInd = toYearFirInd - 1
    pastYearLas = dataDSArr[pastYearLasInd]
    
    facSavePath = savePath + '/' + facName + '/'
    if not os.path.exists(facSavePath):
        os.mkdir(facSavePath)             

    # delete useless data
    if len(os.listdir(facSavePath)) == 1:
        os.remove(facSavePath + os.listdir(facSavePath)[0])

    # get file year
    fileNameLis = os.listdir(facSavePath)  
    fileNameLis = [str(i) for i in fileNameLis]
    fileNameDic = {float(filter(str.isdigit, ifile)): ifile for ifile in fileNameLis}
    fileYearLis = sorted(fileNameDic.keys())    
    
    ## main context
    if toYear in fileYearLis:
        # update data
        print 'update 2017 data'
        # load 2017 data
        toYearPath = facSavePath + fileNameDic[toYear]
        
        dataOldFacDF = cs.ItemArrToDFGet(toYearPath)
        oldDateEnd = dataOldFacDF.index[-1]
        
        if oldDateEnd == dataDSArr[-1]:
            print 'already updated'
            
        else:
            # calculate formula
            dataNewFacDF = dataOldFacDF.reindex(index=dataDSArr[toYearFirInd:])
            dataAddDSArr = dataDSArr[dataDSArr>oldDateEnd]
            dataNewFacDF.loc[dataAddDSArr] = dataFacDF.loc[dataAddDSArr]
            dataNewFacArr = dataNewFacDF.values.astype(float)
            colNames = dataNewFacDF.columns.tolist()
    
            dataDic = {'colNames': np.array(colNames, dtype=object),   
                    'indDate': dataDSArr[toYearFirInd:].reshape(len(dataDSArr[toYearFirInd:]), 1), 
                    facName: dataNewFacArr, 
                    'arrKey': [facName, 'indDate', 'colInnerCode']}        
            facSavePathName = facSavePath + facName + '_' + str(toYear) + '_arr.mat'
            sio.savemat(facSavePathName, dataDic)
            print '2017 file updated'    

        
    else:
        print 'create 2017 file'
        # create 2017 file
        
        dataNewFacDF = dataFacDF.loc[toYearFir:]
        dataNewFacArr = dataNewFacDF.values.astype(float)
        
        colNames = dataNewFacDF.columns.tolist()
        dataDic = {'colNames': np.array(colNames, dtype=object),   
                    'indDate': dataDSArr[toYearFirInd:].reshape(len(dataDSArr[toYearFirInd:]), 1),
                    facName: dataNewFacArr, 
                    'arrKey': [facName, 'indDate', 'colNames']}        
        facSavePathName = facSavePath + facName + '_' + str(toYear) + '_arr.mat'
        sio.savemat(facSavePathName, dataDic)
        print '2017 file created'
    
        if pastYear in fileYearLis:
            print 'update 2016 file'
            pastYearPath = facSavePath + fileNameDic[pastYear]
            dataPastOldFacDF = cs.ForArrToDFGet(pastYearPath)
            pastOldDateEnd = dataPastOldFacDF.index[-1]
            if pastOldDateEnd == pastYearLas:
                print 'do not need to update 2016 file'
            else:
                dataPastDSArr = dataDSArr[(dataDSArr>(pastYear*10000)) & (dataDSArr<(toYear*10000))]
                dataPastFacDF = dataPastOldFacDF.reindex(index=dataPastDSArr, columns=dataInnerCodeArr)
                dataPastAddDSArr = dataPastDSArr[dataPastDSArr>pastOldDateEnd]
                dataPastFacDF.loc[dataPastAddDSArr] = dataFacDF.loc[pastOldDateEnd:pastYearLas]
                dataPastFacArr = dataPastFacDF.values.astype(float)
                pastDataDic = {'colNames': np.array(colNames, dtype=object), 
                        'indDate': dataPastDSArr.reshape(len(dataPastDSArr), 1), 
                        facName: dataPastFacArr, 
                        'arrKey': [facName, 'indDate', 'colNames']}        
                facSavePathName = facSavePath + facName + '_' + str(pastYear) + '_arr.mat'
                sio.savemat(facSavePathName, pastDataDic)
                print '2016 file updated'    

        else:
            print 'create to2016 file'
            
            # create to 2016 file    
            dataPastFacDF = dataFacDF.loc[:pastYearLas]
            dataPastDSArr = dataDSArr[dataDSArr<=pastYearLas]
            dataPastFacArr = dataPastFacDF.values.astype(float)
            pastDataDic = {'colNames': np.array(colNames, dtype=object), 
                           'indDate': dataPastDSArr.reshape(len(dataPastDSArr), 1),
                            facName: dataPastFacArr, 
                            'arrKey': [facName, 'indDate', 'colNames']}
            pastSavePathName = facSavePath + facName + '_To' + str(pastYear) + '_arr.mat'
            sio.savemat(pastSavePathName, pastDataDic)
            print 'to2016 file created'
 
    return None

#def Update3DFormDataGet(dataFacDF, facSavePath, facName):
#    #    dataFacDF=dataFactorReturnDF; facName=facName;facSavePath=ROESavePath
#    # year used
#    toYear = int(dataDSArr[-1])/10000
#    toYearFirInd = np.where(dataDSArr > toYear*10000)[0][0]
#    toYearFir = dataDSArr[toYearFirInd]  # this year first date
#    
#    pastYear = toYear - 1
#    pastYearLasInd = toYearFirInd - 1
#    pastYearLas = dataDSArr[pastYearLasInd]  # past year last date
#    # delete useless data
#    if len(os.listdir(facSavePath)) == 1:
#        os.remove(facSavePath + os.listdir(facSavePath)[0])
#
#    # get file year
#    fileNameLis = os.listdir(facSavePath)   
#    fileNameDic = {float(filter(str.isdigit, ifile)): ifile for ifile in fileNameLis}
#    fileYearLis = sorted(fileNameDic.keys())    
#    
#    ## main context
#    if toYear in fileYearLis:
#        # update data
#        print 'update 2017 data'
#        # load 2017 data
#        toYearPath = facSavePath + fileNameDic[toYear]
#        
#        dataOldFacDF = cs.ItemArrToDFGet(toYearPath)
#        oldDateEnd = dataOldFacDF.index[-1]
#        
#        if oldDateEnd == dataDSArr[-1]:
#            print 'already updated'
#            
#        else:
#            # calculate formula
#            dataNewFacDF = dataOldFacDF.reindex(index=dataDSArr[toYearFirInd:])
#            dataAddDSArr = dataDSArr[dataDSArr>oldDateEnd]
#            dataNewFacDF.loc[dataAddDSArr] = dataFacDF.loc[dataAddDSArr]
#            dataNewFacArr = dataNewFacDF.values.astype(float)
#            colNames = dataNewFacDF.columns.tolist()
#    
#            dataDic = {'colNames': np.array(colNames, dtype=object),   
#                    'indDate': dataDSArr[toYearFirInd:].reshape(len(dataDSArr[toYearFirInd:]), 1), 
#                    facName: dataNewFacArr, 
#                    'arrKey': [facName, 'indDate', 'colInnerCode']}        
#            facSavePathName = facSavePath + facName + '_' + str(toYear) + '_arr.mat'
#            sio.savemat(facSavePathName, dataDic)
#            print '2017 file updated'    
#
#        
#    else:
#        print 'create 2017 file'
#        # create 2017 file
#        
#        dataNewFacDF = dataFacDF.loc[toYearFir:]
#        dataNewFacArr = dataNewFacDF.values.astype(float)
#        
#        colNames = dataNewFacDF.columns.tolist()
#        dataDic = {'colNames': np.array(colNames, dtype=object),   
#                    'indDate': dataDSArr[toYearFirInd:].reshape(len(dataDSArr[toYearFirInd:]), 1),
#                    facName: dataNewFacArr, 
#                    'arrKey': [facName, 'indDate', 'colNames']}        
#        facSavePathName = facSavePath + facName + '_' + str(toYear) + '_arr.mat'
#        sio.savemat(facSavePathName, dataDic)
#        print '2017 file created'
#    
#        if pastYear in fileYearLis:
#            print 'update 2016 file'
#            pastYearPath = facSavePath + fileNameDic[pastYear]
#            dataPastOldFacDF = cs.ForArrToDFGet(pastYearPath)
#            pastOldDateEnd = dataPastOldFacDF.index[-1]
#            if pastOldDateEnd == pastYearLas:
#                print 'do not need to update 2016 file'
#            else:
#                dataPastDSArr = dataDSArr[(dataDSArr>(pastYear*10000)) & (dataDSArr<(toYear*10000))]
#                dataPastFacDF = dataPastOldFacDF.reindex(index=dataPastDSArr, columns=dataInnerCodeArr)
#                dataPastAddDSArr = dataPastDSArr[dataPastDSArr>pastOldDateEnd]
#                dataPastFacDF.loc[dataPastAddDSArr] = dataFacDF.loc[pastOldDateEnd:pastYearLas]
#                dataPastFacArr = dataPastFacDF.values.astype(float)
#                pastDataDic = {'colNames': np.array(colNames, dtype=object), 
#                        'indDate': dataPastDSArr.reshape(len(dataPastDSArr), 1), 
#                        facName: dataPastFacArr, 
#                        'arrKey': [facName, 'indDate', 'colNames']}        
#                facSavePathName = facSavePath + facName + '_' + str(pastYear) + '_arr.mat'
#                sio.savemat(facSavePathName, pastDataDic)
#                print '2016 file updated'    
#
#        else:
#            print 'create to2016 file'
#            
#            # create to 2016 file    
#            dataPastFacDF = dataFacDF.loc[:pastYearLas]
#            dataPastDSArr = dataDSArr[dataDSArr<=pastYearLas]
#            dataPastFacArr = dataPastFacDF.values.astype(float)
#            pastDataDic = {'colNames': np.array(colNames, dtype=object), 
#                           'indDate': dataPastDSArr.reshape(len(dataPastDSArr), 1),
#                            facName: dataPastFacArr, 
#                            'arrKey': [facName, 'indDate', 'colNames']}
#            pastSavePathName = facSavePath + facName + '_To' + str(pastYear) + '_arr.mat'
#            sio.savemat(pastSavePathName, pastDataDic)
#            print 'to2016 file created'
# 
#    return None













