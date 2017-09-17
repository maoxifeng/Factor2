# -*- coding: utf-8 -*-

'''
use a class contains all factors
'''

import os
import time 
import numpy as np
import scipy.io as sio 
import pandas as pd
import matplotlib.pyplot as plt 



class Factors(object):
    '''factor class'''
    
    
    
    '''
	1. init method, to make public dir 
	'''
    def __init__(self, savePathMain='/data/liushuanglong/'):
        self.facMainDir = savePathMain + 'Factors'
        # create the 'Factors' folder
        if not os.path.exists(self.facMainDir):
            os.mkdir(self.facMainDir)
            print self.facMainDir, 'folder created!'
        pass 

    	
    '''
	2. some small methods 
	'''
    def SheetToDFGet(self, path):
        dataRaw = sio.loadmat(path)
        dataSt = dataRaw['dataStruct'][0, 0]
        col = dataSt.dtype.names
        dataArr = np.hstack(dataSt)
        dataDF = pd.DataFrame(dataArr, columns=col)
        return dataDF
    
    def ForArrToDFGet(self, path):
        dataRawDic = sio.loadmat(path)
        arrKey = dataRawDic['arrKey']
        arrKey = [key.split()[0] for key in arrKey]
        dataDSAllArr = dataRawDic[arrKey[1]][:, 0]
        dataInnerCodeAllArr = dataRawDic[arrKey[2]][0]
        dataAllArr = dataRawDic[arrKey[0]]
        dataAllDF = pd.DataFrame(dataAllArr, index=dataDSAllArr,
                                 columns=dataInnerCodeAllArr)
        return dataAllDF
    
    
    def AllArrToDFGet(self, path):
        '''depend on the file name which has digits'''
        fileNameLis = os.listdir(path)
        fileNameDic = {float(filter(str.isdigit, ifile)): ifile for ifile in fileNameLis}
        fileYearLis = sorted(fileNameDic.keys())
        dfLis = []
        for ifileYear in fileYearLis:
            ifilePath = path + '/' + fileNameDic[ifileYear]
            dfTemp = ForArrToDFGet(ifilePath)
            dfLis = dfLis + [dfTemp]
            if ifileYear == fileYearLis[-1]:
                dataInnerCode = dfTemp.columns
    
        dataDF = pd.concat(dfLis)
        dataDF = dataDF.reindex(columns=dataInnerCode)
        dataDF = dataDF.sort_index()
        return dataDF
    
    
    def ItemArrToDFGet(self, path):
        dataRawDic = sio.loadmat(path)
        arrKey = dataRawDic['arrKey']
        arrKey = [key.split()[0] for key in arrKey]
        dataDSAllArr = dataRawDic[arrKey[1]][:, 0]
        dataItemsLis = [i[0] for i in dataRawDic[arrKey[2]][0]]
        dataAllArr = dataRawDic[arrKey[0]]
        dataAllDF = pd.DataFrame(dataAllArr, index=dataDSAllArr,
                                 columns=dataItemsLis)
    
        return dataAllDF
    
    
    def ItemAllArrToDFGet(self, path):
        fileNameLis = os.listdir(path)
        fileNameDic = {float(filter(str.isdigit, ifile)): ifile for ifile in fileNameLis}
        fileYearLis = sorted(fileNameDic.keys())
        dfLis = []
        for ifileYear in fileYearLis:
            ifilePath = path + '/' + fileNameDic[ifileYear]
            dfTemp = ItemArrToDFGet(ifilePath)
            dfLis = dfLis + [dfTemp]
        dataDF = pd.concat(dfLis)
        dataDF = dataDF.sort_index()
        return dataDF
    
    
    def nonNanFirIndGet(self, arr):
    
        '''return the index of the first non nan row of the load array'''
        for i in xrange(len(arr)):
            if len(arr[i][~np.isnan(arr[i])]) > 0:
                break
        return i




    '''
	3. code and date methods 
	'''
    def init_code(self):
        pathCode = '/data/liushuanglong/MyFiles/Data/Common/astock.mat'
        dataDF = cs.SheetToDFGet(pathCode).set_index('InnerCode')
        lastInnerCode = sio.loadmat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/ordInnerCode.mat')['ordInnerCode'][0]
        newInnerCode = dataDF.index.tolist()
       
        addInnerCode = list(set(newInnerCode) - set(lastInnerCode))
        orderInnerCode = np.concatenate([lastInnerCode, addInnerCode]).astype(float)
       
        dataDic = {'ordInnerCode': orderInnerCode}
        sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/ordInnerCode.mat', dataDic)
 
        pass        

    def codeDFGet(self, use=True):
        pathCode = '/data/liushuanglong/MyFiles/Data/Common/astock.mat'
        dataDF = cs.SheetToDFGet(pathCode).set_index('InnerCode', drop=False)
        ordInnerCode = sio.loadmat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/ordInnerCode.mat')['ordInnerCode'][0]
        ordCodeDF = dataDF.reindex(ordInnerCode)
        ordCodeDF.reset_index(drop=True, inplace=True)
        if use:
            ordCodeDF = ordCodeDF.iloc[:, [0, 1, 2, 4]]
        return ordCodeDF
    
    
    def dateSerArrGet(self):
        path = '/data/liushuanglong/MyFiles/Data/Common/alltdays.mat'
        dataRawDF = cs.SheetToDFGet(path)
        dsArr = dataRawDF.values.astype(float)[:, 0]
        DSArr = np.zeros((len(dsArr), 4))
        DSArr[:, 0]= dsArr
        DSArr[:, 1]= np.floor(dsArr/100)
        for imon in np.unique(DSArr[:, 1]):
            useInd = np.where(DSArr[:, 1]==imon)[0]
            DSArr[useInd[0], 2] = 1
            DSArr[useInd[-1], 3] = 1
        return DSArr
    
    def codeIndexDFGet(self, codeStr='HS300', saveBool=False):
    
        '''formative sheet, values are 0 or 1 '''
        # depend on the order of the code, the same order with the code
        codeDic={'HS300': 3145, 'ZZ800': 4982}
        codeInt = codeDic[codeStr]
        pathInd = '/data/liushuanglong/MyFiles/Data/JYDB2/LC_IndexComponent/idxcomponent.mat'
        dataRawDF = cs.SheetToDFGet(pathInd)
    
        dataColUseLis = [u'IndexInnerCode', u'SecuInnerCode', u'InDate', u'OutDate']
        dataUseArr = dataRawDF[dataColUseLis].values.astype(float)
        dataIndArr = dataUseArr[dataUseArr[:, 0]==codeInt]
    
        dataIndArr[dataIndArr[:, 3]==1010101.0, 3] = 90000000.0
    
        dataDSArr = dateSerArrGet()[:, 0]
    
        dataInnerCodeArr = codeDFGet().iloc[:, 0].values.astype(float)   # default value is 0
    
        # formative index array
        #
        forIndexArr = np.zeros((len(dataDSArr), len(dataInnerCodeArr)))
        dataInnerCodeUseArr = np.unique(dataIndArr[:, 1])  #  use codes belong to index sheet
        for iicode, icode in enumerate(dataInnerCodeUseArr):
            arrTemp = dataIndArr[dataIndArr[:, 1]==icode, 2:]   # select one code indate, outdate data
            for ilen in range(len(arrTemp)):          #
                useBool = (dataDSArr>=arrTemp[ilen, 0]) & (dataDSArr<arrTemp[ilen, 1])
                forIndexArr[useBool, dataInnerCodeArr==icode] = 1     #  if the code is in the pool, the value is 1
    
        if saveBool:
            arrName = codeStr + '_IndexCode'
            dataDic={'colInnerCode': dataInnerCodeArr,
                     'indDate': dataDSArr.reshape(len(dataDSArr), 1),
                     arrName: forIndexArr, \
                     'arrKey': [arrName, 'indDate', 'colNames']}
    
            savePath ='/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/'
            saveName = savePath + '/' + arrName + '_array.mat'
            sio.savemat(saveName, dataDic)
            print 'file saved ~'
        forIndexDF = pd.DataFrame(forIndexArr, index=dataDSArr, columns=dataInnerCodeArr)
        return forIndexDF

 

    '''
	4. update methods, default form  
	'''
	def UpdateFormDataGet(self, dataFacDF, savePath, facName):
	
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
	
	def UpdateItemDataGet(self, dataFacDF, savePath, facName):
	
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


    '''
	5. daily quote 

	'''
    def DailyQuoteGet(self, item):
    
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
    
    
    
    def RAFactorGet(self):
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
    
    
    def AdjCloseGet(self):
    
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
    
    
    
    def StoReturnGet(self):
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

        return None  


    def DailyQuote(self):
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
        # Close
        _ = dq.DailyQuoteGet(u'ClosePrice')
        
        # Volume
        _ = dq.DailyQuoteGet(u'TurnoverVolume')
        
        # Turnover value
        _ = dq.DailyQuoteGet(u'TurnoverValue')
        
        # Adjusting price factors
        _ = dq.RAFactorGet()
        
        # Adjusted Close
        _ = dq.AdjCloseGet()
        
        # stock log return
        dq.StoReturnGet()

        return None



    '''
	6. index quote 

	'''
	def IndexQuoteGet(self, mar='HS300', facName='ClosePrice', items=[u'PrevClosePrice', u'ClosePrice']):
	
		itemsLis = [u'TradingDay',
		             u'XGRQ',
		             u'ChangePCT',
		             u'ClosePrice',
		             u'HighPrice',
		             u'InnerCode',
		             u'LowPrice',
		             u'NegotiableMV',
		             u'OpenPrice',
		             u'PrevClosePrice',
		             u'TurnoverDeals',
		             u'TurnoverValue',
		             u'TurnoverVolume']
	    '''save file'''
	    pathQTDaily = '/data/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/'
	    savePathMain = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/'
	    indexSavePath = savePathMain + mar + '/'
	    if not os.path.exists(indexSavePath):
	        os.mkdir(indexSavePath)
	    facName = mar + '_' + facName
	    facSavePath = indexSavePath + facName + '/'
	    if not os.path.exists(facSavePath):
	        os.mkdir(facSavePath)
	
	
	    fileLis = os.listdir(pathQTDaily)
	    dailyLis = []
	    codeDic={'HS300': 3145, 'ZZ800': 4982}
	    for ifileName in fileLis:
	        ifilePath = pathQTDaily + ifileName
	        dataRaw = cs.SheetToDFGet(ifilePath)
	        dataCol = [u'TradingDay', u'InnerCode'] + items
	        dataDFTol = dataRaw[dataCol]
	
	        dataDFUse = dataDFTol[dataDFTol[u'InnerCode']==codeDic[mar]]
	        dataDFUseSort = dataDFUse.sort_values(by=u'TradingDay')
	        dataDFUseSort = dataDFUseSort.drop([u'InnerCode'], axis=1)
	        dataIndexDF = dataDFUseSort.set_index('TradingDay')
	
	        dailyLis = dailyLis + [dataIndexDF]
	
	
	    dataItemAllDF = pd.concat(dailyLis)
	    dataItemAllSortDF = dataItemAllDF.sort_index()
	
	    dataItemAllUse = dataItemAllSortDF[~dataItemAllSortDF.index.duplicated()]
	
	    dataItemAllUseDF = dataItemAllUse.loc[dataDSArr]   #
	    cu.UpdateItemDataGet(dataItemAllUseDF,  facSavePath, facName)   
	
	    return None
	
	
	def IndexLogReturnGet(self, mar='HS300'):
	    dicPath = {'HS300': '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/HS300/HS300_ClosePrice'}
	    closePath = dicPath[mar]
	    indexPath = os.path.split(closePath)[0]
	
	    facName = mar + '_Return'
	    savePath = indexPath + '/' + facName + '/'
	    if not os.path.exists(savePath):
	        os.mkdir(savePath)
	
	    indexDataDF = cs.ItemAllArrToDFGet(closePath)
	    IndexLogReturnDF = pd.DataFrame(index=indexDataDF.index, columns=[facName])
	    IndexLogReturnDF.iloc[:, 0] = np.log(indexDataDF[u'ClosePrice']) - np.log(indexDataDF[u'PrevClosePrice'])
	#    if Free:
	#            pathFreeRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Common/Wind_Daily10YearBond_LogReturn_array.mat'
	#            dataFreeRetArr = sio.loadmat(pathFreeRet)['TenYearBond_LogReturn']
	#            IndexLogReturnArr = IndexLogReturnArr - dataFreeRetArr
	#            mar = mar + 'Free'
	    cu.UpdateItemDataGet(IndexLogReturnDF, savePath, facName)
	    return None
	
	
	def BondReturnGet(self):
	    '''from wind 10 years bond '''
	    savePathMain = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/'
	    facName = 'BondReturn'
	    facSavePath = savePathMain + facName + '/'
	
	    if not os.path.exists(facSavePath):
	        os.mkdir(facSavePath)
	
	    path = '/data/liushuanglong/MyFiles/Data/Common/bond_10y.mat'
	    dataRawDF = cs.SheetToDFGet(path)
	    dataDF = dataRawDF.set_index('date')
	    dataDSArr = tc.dateSerArrGet()[:, 0]
	    dataDF = dataDF.reindex(dataDSArr)
	    dataPrice = dataDF.values.astype(float)
	    dataReturn = pd.DataFrame(index=dataDSArr, columns=['Return'])
	    dataReturn.iloc[1:] = np.log(dataPrice[1:]) - np.log(dataPrice[:-1])  # log return
	
	    cu.UpdateItemDataGet(dataReturn, facSavePath, facName)
	    return None


    def IndexQuote(self):
        '''get index quote data'''

        # HS300 Index Close
        iq.IndexQuoteGet(mar='HS300', facName='ClosePrice', items=[u'PrevClosePrice', u'ClosePrice'])
        
        # HS300 Index Return
        iq.IndexLogReturnGet(mar='HS300')
        
        # Wind 10 year Bond Return
        iq.BondReturnGet()
        
        return None

    def IndexExposure(self):

        pass
        return None



    '''
	7. factor common fundamental data  

	'''

    def AFloatsGet(self):
    
        savePath = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/'
        facName = 'AFloats'
        # load income statement new data
        pathST = '/data/liushuanglong/MyFiles/Data/JYDB2/LC_ShareStru/sharestru.mat'
        dataRaw = cs.SheetToDFGet(pathST)
        dataColUseLis = [u'CompanyCode', u'EndDate', facName]   #use enddate
        dataValuesTolArr = dataRaw[dataColUseLis]
    
        # dataframe, select by company code and mark
        dataValuesTolDF = pd.DataFrame(dataValuesTolArr, columns=dataColUseLis)
        dataValuesTolDF = dataValuesTolDF[dataValuesTolDF[u'CompanyCode'].isin(dataComCodeArr)]
    
        # sort by company code, end date, mark
        dataValuesUseDFSor = dataValuesTolDF.sort_values(by=[u'CompanyCode',u'EndDate'])
        dataValuesUseDFSor = dataValuesUseDFSor.drop_duplicates(subset=[u'CompanyCode',u'EndDate'])
        dataComCodeUse = np.unique(dataValuesUseDFSor[u'CompanyCode'])  
    
        # create  df dict of total data
        dataValuesUseDFInd = dataValuesUseDFSor.set_index([u'CompanyCode',u'EndDate'])
    
        print facName, 'dic getting:', time.strftime("%H:%M:%S", time.localtime())
        dataValuesDic = {}
        for code in dataComCodeUse:
            dataValuesDic[code] = dataValuesUseDFInd.loc[code]
    
        # create a dic contain all effective date
        dataFacDF = pd.DataFrame(index=dataDSArr, columns=dataComCodeArr)
        for iicode, code in enumerate(dataComCodeUse):
            dataOneCodeTolDF = dataValuesDic[code]
            dataOneCodeTolDF[u'EndDate'] = dataOneCodeTolDF.index
            dataOneCodeTSRaw = dataOneCodeTolDF.index.tolist()
            dataOneCodeTSTol = sorted(set(dataDSArr) | set(dataOneCodeTSRaw))
            dataOneCodeUseDF = dataOneCodeTolDF.reindex(dataOneCodeTSTol, method='ffill').loc[dataDSArr]
            if dataOneCodeUseDF.size==0:
                continue
            dataFacDF[code] = dataOneCodeUseDF[facName]
            if iicode % 100 == 0:
                print 'code', code, 'data got'
        print facName, 'dic got', time.strftime("%H:%M:%S", time.localtime())
    
        # convert to innercode
        dataFacDF.columns = dataInnerCodeArr
    
        # year used
        toYear = int(dataDSArr[-1])/10000
        toYearFirInd = np.where(dataDSArr > toYear*10000)[0][0]
        toYearFir = dataDSArr[toYearFirInd]
    
        pastYear = toYear - 1
        pastYearLasInd = toYearFirInd - 1
        pastYearLas = dataDSArr[pastYearLasInd]
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
                dataPastFacDF = dataFacDF.loc[:pastYearLas].dropna(axis=1, how='all')
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



    '''
	8. factor common methods 

	'''

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


    def FacDicTo3DArrDicGet(dataRawDic, facName='Factor'):
        comCodeLis = dataRawDic.keys()
        itemsLis = dataRawDic[comCodeLis[0]].columns.tolist()  # item order !
        dataFormatDic = {}
        for iitem in itemsLis:
            dataFormatDic[iitem] = pd.DataFrame(index=dataDSArr, columns=dataComCodeArr)
    
    
        print 'start convert to 3D form array: ',
        print time.strftime("%H:%M:%S", time.localtime())
        print 'code counts', 'code'
        for iicode, icode in enumerate(comCodeLis):
            if dataRawDic[icode].size==0:
                continue
            pubDateLis = dataRawDic[icode].index.tolist()
            pubDateLis.extend(list(dataDSArr))
            allDateArr = np.unique(pubDateLis)
            # famative date process
            icodeDF = dataRawDic[icode].reindex(index=allDateArr, method='ffill')
            icodeDefDF = icodeDF.loc[dataDSArr]
            for iitem in icodeDefDF.columns:
                dataFormatDic[iitem][icode] = icodeDefDF[iitem]
    
            if iicode%100 == 0:
                print iicode, icode
    
        data3DArr = np.zeros((len(itemsLis), len(dataDSArr), len(dataComCodeArr)))
        data3DArr[:] = np.nan
        for iiitem, iitem in enumerate(itemsLis):
            arrTemp = dataFormatDic[iitem].values.astype(float)
            data3DArr[iiitem] = arrTemp
    
        arrName = facName + '_3DValues'
        dataDic = {'axis1Names_Items': np.array(itemsLis, dtype=object),
                   'axis2Names_DateSeries': dataDSArr.reshape(len(dataDSArr), 1),\
                   'axis3Names_ComCode': dataComCodeArr,\
                   arrName: data3DArr,
                   'arrKey': [arrName, 'axis1Names_Items', 'axis2Names_DateSeries', 'axis3Names_ComCode']}
        return dataDic



    def DivGroRetGet(loadPath, divGroNum=10, divPer='1M', pool='A', facName='Factor', saveBool=False, arrDimIndex=0):
        #==============================================================================
        # 1. load data
        #==============================================================================
        ## load factor exposure data
        dataFactorExpDic = sio.loadmat(loadPath)
        facArrKey = dataFactorExpDic['arrKey'][0]
        dataFactorExpArr = dataFactorExpDic[facArrKey]
        if dataFactorExpArr.ndim == 3 :
            dataFactorExpArr = dataFactorExpArr[arrDimIndex]
    
        dataFactorExpDF = pd.DataFrame(dataFactorExpArr, index=dataDSArr, columns=dataInnerCodeArr)
    
        ## load stoct daily returns
        pathStoLogRet = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_array.mat'
        dataStoRetArr = sio.loadmat(pathStoLogRet)['StoLogReturn']
    
        ## load stock daily volumne
        pathVol = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_TurnoverVolume_array.mat'
        dataVolRaw = sio.loadmat(pathVol)
        dataVolArr = dataVolRaw[u'TurnoverVolume']  # columns: inner code
    
        ## load stock AFloats
        pathAF = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/Afloats/LC_AFloats_mat.mat'
        dataAFloatsRaw = sio.loadmat(pathAF)
        dataAFloats3DArr = dataAFloatsRaw['LC_AFloats']
        dataAFloatsArr = dataAFloats3DArr[0]
    
         # constant
        thrNum = 100
        if pool == 'HS300':
            print 'HS300 pool'
            thrNum = 15
    
            # load HS300 index  0/1 sheet
            dataHS300IndexDF = tc.codeIndexDFGet(codeStr='HS300')
            dataHS300IndexDF[dataHS300IndexDF==0] = np.nan
            dataFactorExpDF = dataHS300IndexDF * dataFactorExpDF
            dataFactorExpArr = dataFactorExpDF.values.astype(float)
    
            dataHS300IndexArr = dataHS300IndexDF.values.astype(float)
            dataStoRetArr = dataStoRetArr * dataHS300IndexArr
            dataVolArr = dataVolArr * dataHS300IndexArr
            dataAFloatsArr = dataAFloatsArr * dataHS300IndexArr
    
        dataVolUseArr = np.zeros((len(dataDSArr), len(dataInnerCodeArr)))
        dataReturnUseArr = np.zeros((len(dataDSArr), len(dataInnerCodeArr)))
        dataAFloatsUseArr = np.zeros((len(dataDSArr), len(dataInnerCodeArr)))
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
    
        dataStoRetDF = pd.DataFrame(dataReturnUseArr, index=dataDSArr, columns=dataInnerCodeArr)
        dataAFloatsDF = pd.DataFrame(dataAFloatsUseArr, index=dataDSArr, columns=dataInnerCodeArr)
        #==============================================================================
        # 2. seperate groups and calculate groups returns
        #==============================================================================
        colNames = ['group'+str(i+1) for i in range(divGroNum)]
        dataFacGroReturnDF = pd.DataFrame(index=dataDSArr, columns=colNames)
    
        staInd = sf.nonNanFirIndGet(dataFactorExpArr)
    
        dataDSAllEffArr = tc.dateSerArrGet()[staInd:]
        monEndDateArr = dataDSAllEffArr[dataDSAllEffArr[:, 3]==1, 0]
    
        print 'start divide', str(divGroNum) + 'groups:', time.strftime("%H:%M:%S", time.localtime())
        percentNumAllArr = np.linspace(0, 1, divGroNum+1)
        for iimonendDate, imonendDate in enumerate(monEndDateArr[:-1]):
            dataFactorMonUseTemp = dataFactorExpDF.loc[imonendDate]
            if len(dataFactorMonUseTemp.dropna()) >= thrNum:  # keep stocks groups when counts >=100
                perFactorExpArr = np.zeros_like(percentNumAllArr)       
                perFactorExpArr[-1] = dataFactorMonUseTemp.max()
                perFactorExpArr[0] = dataFactorMonUseTemp.min()
                perFactorExpArr[1:-1] = dataFactorMonUseTemp.quantile(percentNumAllArr[1:-1]).values
                dsTemp = dataDSArr[(dataDSArr>monEndDateArr[iimonendDate]) & (dataDSArr<=monEndDateArr[iimonendDate+1])]
    #            print dsTemp
                for iigro in range(divGroNum):
                    igroupLis = dataFactorMonUseTemp[(dataFactorMonUseTemp>perFactorExpArr[iigro])\
                                                    & (dataFactorMonUseTemp<=perFactorExpArr[iigro+1])].index.tolist()
                    for iidate, idate in enumerate(dsTemp):
                        dataOGTemDF = pd.DataFrame(index=igroupLis, columns=['return', 'aFloats', 'weight', 'wReturn'])
                        dataOGTemDF['return'] = dataStoRetDF.loc[idate][igroupLis]
                        dataOGTemDF['aFloats'] = dataAFloatsDF.loc[idate][igroupLis]
                        dataOGTemDF['weight'] = dataOGTemDF['aFloats'] / dataOGTemDF['aFloats'].sum()
                        dataOGTemDF['wReturn'] = dataOGTemDF['return'] * dataOGTemDF['weight']
                        dataFacGroReturnDF.loc[idate].iloc[iigro] = dataOGTemDF['wReturn'].sum()
                print imonendDate, 'Done' , time.strftime("%H:%M:%S", time.localtime())
        dataFacGroReturnArr = dataFacGroReturnDF.values.astype(float)
        arrName = facName + '_' + pool + '_' + str(divGroNum) + 'Groups' + 'Return'
        dataDic={'colNames': np.array(colNames, dtype=object),
                 'indDate': dataDSArr.reshape(len(dataDSArr), 1),
                 arrName: dataFacGroReturnArr, \
                 'arrKey': [arrName, 'indDate', 'colNames']}
    
        if saveBool :
            savePath = os.path.split(loadPath)[0]
            saveName = savePath + '/' + arrName + '_arr.mat'
            sio.savemat(saveName, dataDic)
            print arrName + '_array.mat', 'saved ~'
    
        return dataFacGroReturnArr
    
    
    def DivGroExcRetGraphGet(loadArr=None, loadPath=None, facName_Pool='Factor'):
    
        corUseLis = ['lightcoral', 'red', 'gold', 'lawngreen',\
                    'darkgreen', 'aquamarine', 'dodgerblue', 'blue', 'mediumorchid', 'fuchsia', 'pink']
        if loadArr is not None:
            dataRetRawArr = loadArr
        else:
            dataRawDic = sio.loadmat(loadPath)
            facArrKey = dataRawDic['arrKey'][0]
            dataRetRawArr = dataRawDic[facArrKey]
    
        pathMar = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/IndexQuote/IndexQuote_HS300_LogReturn_arr.mat'
        dataMarRetRaw = sio.loadmat(pathMar)
        dataMarRetArr = dataMarRetRaw[dataMarRetRaw['arrKey'][0]]
    
    
        dataRetArr = dataRetRawArr.copy()
        startGroInd = sf.nonNanFirIndGet(dataRetArr)
        startMarInd = sf.nonNanFirIndGet(dataMarRetArr)
        startInd = max(startGroInd, startMarInd)
        dataRetArr[:startInd] = 0
        dataRetCumArr = np.cumsum(dataRetArr, axis=0)
        dataRetCumArr[:startInd] = np.nan
        dataMarRetArr[:startInd] = 0
        dataMarRetCumArr = np.cumsum(dataMarRetArr, axis=0)
        dataMarRetCumArr[:startInd] = np.nan
        #re2 = np.corrcoef(bb, cc)
    
        groNums = dataRetCumArr.shape[1]
        dataRetCumArr = dataRetCumArr - dataMarRetCumArr
        fig = plt.figure(figsize=(15, 10))
        ax1 = fig.add_subplot(211)
        for i in range(groNums):
            ax1.plot(range(len(dataDSArr)), dataRetCumArr[:, i], color=corUseLis[i], lw=1.5, label='Group'+str(i+1))
    
        ax1.set_xlim(startInd-250, len(dataDSArr)+400)
    
    #    ax1.set_ylim(-0.5, 2.5 )
        ax1.set_xticks(range(startInd, len(dataDSArr), 250))
        ax1.set_xticklabels([dataDSArr[i] for i in ax1.get_xticks()], rotation=30, fontsize='small')
        #ax1.set_yticks(range(-0.3, 1.8, 0.2))
        ax1.set_yticklabels([str((int(i*100)))+'%' for i in ax1.get_yticks()])
        titleName = facName_Pool + '_' + str(groNums) + 'Groups_ExcessReturn'
        ax1.set_title(titleName)
        #ax1.set_xlabel('Date')
        ax1.set_ylabel('Cumulative_ExcessReturn')
        ax1.legend(loc=1, fontsize='small')
    
        ax2 = fig.add_subplot(212)
        ax2.bar((np.arange(1, groNums+1)), dataRetCumArr[-1], width=0.8,  align="center", color=corUseLis)
        ax2.set_xlim(0, 12)
        ax2.set_xticks(np.arange(1, groNums+1))
        ax2.set_xticklabels(['Group'+str(int(i)) for i in ax2.get_xticks()])
        ax2.set_yticklabels([str((int(i*100)))+'%' for i in ax2.get_yticks()])
        ax2.set_ylabel('Cumulative_ExcessReturn')
    #    ax2.legend(loc=1)
        if loadPath is not None:
            savePath = os.path.split(loadPath)[0]
            saveName = savePath + '/' + titleName + '.png'
            plt.savefig(saveName, dpi=400)
            print titleName + '.png saved~'
        return dataRetCumArr




    '''
	9. factors

	'''















