# -*- coding: utf-8 -*-



"""
use a class contains all factors
"""

import os
import time 
import numpy as np
import scipy.io as sio 
import pandas as pd
import matplotlib.pyplot as plt 
import statsmodels.api as sm


class Factor(object):
    """factor class"""

    # ----------------------------------------------------------------------
    # 1. init method, to make public dir 

    def __init__(self, savePathMain='/data/liushuanglong/'):
        """Make directory and get data directory. 

        Args:
        -----
        savePathMain: string, default '/data/liushuanglong/'.
            Main directory of all data.
        
        Return:  
        -------
        facMainDir: string.
            Main directory of all factors. 
        dataMainDir: string. 
            Main directory of all data, already created by matlab script, 
            the same time, two sub-directory: Data/, JYDB2/ made. 
         
        DirDiagram:
        -----------
        Factor/ 
        Data/Common/
        Data/JYDB2/
        """
        self.facMainDir = savePathMain + 'Factors/'
        self.dataMainDir = savePathMain + 'Data/' 
        self.dataComDir = savePathMain + 'Data/Common/'
        self.dataJYDBDir = savePathMain + 'Data/JYDB2/'
        # Create the 'Factors' folder
        if not os.path.exists(self.facMainDir):
            os.mkdir(self.facMainDir)
            print self.facMainDir, 'folder created!'
        if not os.path.exists(self.dataMainDir):
            print self.dataMainDir, 'not exist!'
        self.init_code()  # initialize inner code 
        # codeDF, has 4 columns, as follows:
        # 0: InnerCode, 1: CompanyCode, 2: SecuCode, 3: SecuMarket
        self.codeDF = self.codeDFGet()
        self.dataInnerCodeArr = self.codeDF.iloc[:, 0].values.astype(float)
        self.dataComCodeArr = self.codeDF.iloc[:, 1].values.astype(float)
        self.dateArr = self.dateSerArrGet()
        self.dataDSArr = self.dateArr[:, 0]
        # Get index formative array. 
        self.HS300IndexDF = self.codeIndexDFGet(codeStr='HS300')
        return 

    # ----------------------------------------------------------------------
    # 2. some small common methods 

    def SheetToDF(self, path):
        # convert raw single company sheet dataStruct to single dataframe
        dataRaw = sio.loadmat(path)
        dataSt = dataRaw['dataStruct'][0, 0]
        col = dataSt.dtype.names
        dataArr = np.hstack(dataSt)
        dataDF = pd.DataFrame(dataArr, columns=col)
        return dataDF
    
    def FormArrToDF(self, path):
        """
        convert single formative dataDict saved by sio.io to single dataframe
        
        show dataDic as follows: 
        dataDic = {'colInnerCode': self.dataInnerCodeArr, \
                   'indDate': dataDSUseArr.reshape(len(dataDSUseArr), 1), \
                   item: dataArr,
                   'arrKey': [item, 'indDate', 'colInnerCode']}
        """
        dataRawDic = sio.loadmat(path)
        arrKey = dataRawDic['arrKey']
        arrKey = [key.split()[0] for key in arrKey]
        dataDSAllArr = dataRawDic[arrKey[1]][:, 0]
        dataInnerCodeAllArr = dataRawDic[arrKey[2]][0]
        dataAllArr = dataRawDic[arrKey[0]]
        dataAllDF = pd.DataFrame(dataAllArr, index=dataDSAllArr,
                                 columns=dataInnerCodeAllArr)
        return dataAllDF
    
    def AllFormArrToDF(self, path):
        """
        depend on the file name which includes digit 
        will use FormArrToDF funtion 
        """
        fileNameLis = os.listdir(path)
        fileNameDic = {float(filter(str.isdigit, ifile)): ifile for ifile in fileNameLis}
        fileYearLis = sorted(fileNameDic.keys())
        dfLis = []
        for ifileYear in fileYearLis:
            ifilePath = path + '/' + fileNameDic[ifileYear]
            dfTemp = self.FormArrToDF(ifilePath)
            dfLis = dfLis + [dfTemp]
            if ifileYear == fileYearLis[-1]:
                dataInnerCode = dfTemp.columns
        dataDF = pd.concat(dfLis)
        dataDF = dataDF.reindex(columns=dataInnerCode)
        dataDF = dataDF.sort_index()
        return dataDF
    
    def ItemArrToDF(self, path):
        """
        convert single dataDict saved by sio.io to single dataframe
        
        show dataDic as follows: 
        dataDic = {'items': np.array(items, dtype=object), \
                   'indDate': dataDSUseArr.reshape(len(dataDSUseArr), 1), \
                   item: dataArr,
                   'arrKey': [item, 'indDate', 'items']}
        """
        dataRawDic = sio.loadmat(path)
        arrKey = dataRawDic['arrKey']
        arrKey = [key.split()[0] for key in arrKey]
        dataDSAllArr = dataRawDic[arrKey[1]][:, 0]
        dataItemsLis = [i[0] for i in dataRawDic[arrKey[2]][0]]
        dataAllArr = dataRawDic[arrKey[0]]
        dataAllDF = pd.DataFrame(dataAllArr, index=dataDSAllArr,
                                 columns=dataItemsLis)
        return dataAllDF
    
    def AllItemArrToDF(self, path):
        fileNameLis = os.listdir(path)
        fileNameDic = {float(filter(str.isdigit, ifile)): ifile for ifile in fileNameLis}
        fileYearLis = sorted(fileNameDic.keys())
        dfLis = []
        for ifileYear in fileYearLis:
            ifilePath = path + '/' + fileNameDic[ifileYear]
            dfTemp = self.ItemArrToDF(ifilePath)
            dfLis = dfLis + [dfTemp]
        dataDF = pd.concat(dfLis)
        dataDF = dataDF.sort_index()
        return dataDF
    
    def nonNanFirInd(self, arr):
        """return the index of the first non nan row of the load array."""
        for i in xrange(len(arr)):
            if len(arr[i][~np.isnan(arr[i])]) > 0:
                break
        return i

    # ----------------------------------------------------------------------
    # 3. code and date methods

    def init_code(self):
        pathCode = self.dataComDir + 'astock.mat'
        dataDF = self.SheetToDF(pathCode).set_index('InnerCode')
        newInnerCode = dataDF.index.tolist()
        timeCodeFold = self.facMainDir + 'Time_Code/'
        ordInnerCodeFileName = timeCodeFold + 'ordInnerCode.mat' 
        if not os.path.exists(timeCodeFold):
            os.mkdir(timeCodeFold)
            dataDic = {'ordInnerCode': newInnerCode}
            sio.savemat(ordInnerCodeFileName, dataDic)
            self.ordInnerCode = newInnerCode  
        else:
            lastInnerCode = sio.loadmat(ordInnerCodeFileName)['ordInnerCode'][0]
            addInnerCode = list(set(newInnerCode) - set(lastInnerCode))
            orderInnerCode = np.concatenate([lastInnerCode, addInnerCode]).astype(float)
            dataDic = {'ordInnerCode': orderInnerCode}
            sio.savemat(ordInnerCodeFileName, dataDic)
            self.ordInnerCode = orderInnerCode 

    def codeDFGet(self, use=True):
        pathCode = self.dataComDir + 'astock.mat'
        dataDF = self.SheetToDF(pathCode).set_index('InnerCode', drop=False)
        ordCodeDF = dataDF.reindex(self.ordInnerCode)
        ordCodeDF.reset_index(drop=True, inplace=True)
        if use:
            # 0: InnerCode, 1: CompanyCode, 2: SecuCode, 4: SecuMarket
            ordCodeDF = ordCodeDF.iloc[:, [0, 1, 2, 4]]
        return ordCodeDF
    
    def dateSerArrGet(self):
        """Get the date series of the trading day. 

        Returns:
        --------
        DSArr: DF
            It has four columns:
            0: date, 1: month, 3: if the first day of the month 
            4: if the last day of the month
        """
        path = self.dataComDir + 'alltdays.mat'
        dataRawDF = self.SheetToDF(path)
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
        """formative sheet, values are 0 or 1 """
        # depend on the order of the code, the same order with the code
        codeDic={'HS300': 3145, 'ZZ800': 4982}
        codeInt = codeDic[codeStr]
        pathInd = self.dataJYDBDir + 'LC_IndexComponent/idxcomponent.mat'
        dataRawDF = self.SheetToDF(pathInd)
        dataColUseLis = [u'IndexInnerCode', u'SecuInnerCode', u'InDate', u'OutDate']
        dataUseArr = dataRawDF[dataColUseLis].values.astype(float)
        dataIndArr = dataUseArr[dataUseArr[:, 0]==codeInt]
        dataIndArr[dataIndArr[:, 3]==1010101.0, 3] = 90000000.0
        # formative index array
        forIndexArr = np.zeros((len(self.dataDSArr), len(self.dataInnerCodeArr)))
        dataInnerCodeUseArr = np.unique(dataIndArr[:, 1])  #  use codes belong to index sheet
        for iicode, icode in enumerate(dataInnerCodeUseArr):
            arrTemp = dataIndArr[dataIndArr[:, 1]==icode, 2:]   # select one code indate, outdate data
            for ilen in range(len(arrTemp)):          #
                useBool = (self.dataDSArr>=arrTemp[ilen, 0]) & (self.dataDSArr<arrTemp[ilen, 1])
                forIndexArr[useBool, self.dataInnerCodeArr==icode] = 1     #  if the code is in the pool, the value is 1
        if saveBool:
            arrName = codeStr + '_IndexCode'
            dataDic={'colInnerCode': self.dataInnerCodeArr,
                     'indDate': self.dataDSArr.reshape(len(self.dataDSArr), 1),
                     arrName: forIndexArr, \
                     'arrKey': [arrName, 'indDate', 'colNames']}
    
            savePath = self.facMainDir + 'Time_Code/'
            saveName = savePath + '/' + arrName + '_array.mat'
            sio.savemat(saveName, dataDic)
            print 'file saved ~'
        forIndexDF = pd.DataFrame(forIndexArr, index=self.dataDSArr, columns=self.dataInnerCodeArr)
        return forIndexDF

    # ----------------------------------------------------------------------
    # 4. update methods, default form

    def UpdateFormDataGet(self, dataFacDF, savePath, facName):
        # year used
        toYear = int(self.dataDSArr[-1])/10000
        toYearFirInd = np.where(self.dataDSArr > toYear*10000)[0][0]
        toYearFir = self.dataDSArr[toYearFirInd]
    
        pastYear = toYear - 1
        pastYearLasInd = toYearFirInd - 1
        pastYearLas = self.dataDSArr[pastYearLasInd]
        # save folder
        facSavePath = savePath + '/' + facName + '/'
        if not os.path.exists(facSavePath):
            os.mkdir(facSavePath)
        # delete useless data
        if len(os.listdir(facSavePath)) == 1:
            os.remove(facSavePath + os.listdir(facSavePath)[0])
        # get file year
        fileNameLis = os.listdir(facSavePath)
        fileNameLis = [ifile for ifile in fileNameLis if ifile[-4:]=='.mat']
        fileNameDic = {float(filter(str.isdigit, ifile[-12:-8])): ifile for ifile in fileNameLis}
        fileYearLis = sorted(fileNameDic.keys())
        ## main context
        if toYear in fileYearLis:
            # update data
            print 'update 2017 data'
            # load 2017 data
            toYearPath = facSavePath + fileNameDic[toYear]
            dataOldFacDF = self.FormArrToDF(toYearPath)
            oldDateEnd = dataOldFacDF.index[-1]
            if oldDateEnd == self.dataDSArr[-1]:
                print 'already updated'
            else:
                # calculate formula
                dataNewFacDF = dataOldFacDF.reindex(index=self.dataDSArr[toYearFirInd:], columns=self.dataInnerCodeArr)
                dataAddDSArr = self.dataDSArr[self.dataDSArr>oldDateEnd]
                dataNewFacDF.loc[dataAddDSArr] = dataFacDF.loc[dataAddDSArr]
                dataNewFacArr = dataNewFacDF.values.astype(float)
                dataDic = {'colInnerCode': self.dataInnerCodeArr,  # depend on adj close innercode
                        'indDate': self.dataDSArr[toYearFirInd:].reshape(len(self.dataDSArr[toYearFirInd:]), 1), # depend on adj close date
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
            dataDic = {'colInnerCode': self.dataInnerCodeArr,  # depend on adj close innercode
                        'indDate': self.dataDSArr[toYearFirInd:].reshape(len(self.dataDSArr[toYearFirInd:]), 1), # depend on adj close date
                        facName: dataNewFacArr,
                        'arrKey': [facName, 'indDate', 'colInnerCode']}
            facSavePathName = facSavePath + facName + '_' + str(toYear) + '_arr.mat'
            sio.savemat(facSavePathName, dataDic)
            print '2017 file created'
            if pastYear in fileYearLis:
                print 'update 2016 file'
                pastYearPath = facSavePath + fileNameDic[pastYear]
                dataPastOldFacDF = self.FormArrToDF(pastYearPath)
                pastOldDateEnd = dataPastOldFacDF.index[-1]
                if pastOldDateEnd == pastYearLas:
                    print 'do not need to update 2016 file'
                else:
                    dataPastDSArr = self.dataDSArr[(self.dataDSArr>(pastYear*10000)) & (self.dataDSArr<(toYear*10000))]
                    dataPastFacDF = dataPastOldFacDF.reindex(index=dataPastDSArr, columns=self.dataInnerCodeArr)
                    dataPastAddDSArr = dataPastDSArr[dataPastDSArr>pastOldDateEnd]
                    dataPastFacDF.loc[dataPastAddDSArr] = dataFacDF.loc[pastOldDateEnd:pastYearLas]
                    dataPastFacArr = dataPastFacDF.values.astype(float)
                    pastDataDic = {'colInnerCode': self.dataInnerCodeArr,  # depend on adj close innercode
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
                dataPastDSArr = self.dataDSArr[self.dataDSArr<=pastYearLas]
                dataPastFacArr = dataPastFacDF.values.astype(float)
                pastDataDic = {'colInnerCode': dataPastFacDF.columns.tolist(),
                               'indDate': dataPastDSArr.reshape(len(dataPastDSArr), 1),
                                facName: dataPastFacArr,
                                'arrKey': [facName, 'indDate', 'colInnerCode']}
                pastSavePathName = facSavePath + facName + '_To' + str(pastYear) + '_arr.mat'
                sio.savemat(pastSavePathName, pastDataDic)
                print 'to2016 file created'
        return None
    
    def UpdateItemDataGet(self, dataFacDF, savePath, facName):
        # dataFacDF=dataFactorReturnDF; facName=facName;facSavePath=ROESavePath
        # year used
        toYear = int(self.dataDSArr[-1])/10000
        toYearFirInd = np.where(self.dataDSArr > toYear*10000)[0][0]
        toYearFir = self.dataDSArr[toYearFirInd]
    
        pastYear = toYear - 1
        pastYearLasInd = toYearFirInd - 1
        pastYearLas = self.dataDSArr[pastYearLasInd]
    
        facSavePath = savePath + '/' + facName + '/'
        if not os.path.exists(facSavePath):
            os.mkdir(facSavePath)
    
        # delete useless data
        if len(os.listdir(facSavePath)) == 1:
            os.remove(facSavePath + os.listdir(facSavePath)[0])
    
        # get file year
        fileNameLis = os.listdir(facSavePath)
        fileNameLis = [str(i) for i in fileNameLis]
        fileNameLis = [ifile for ifile in fileNameLis if ifile[-4:]=='.mat']
        fileNameDic = {float(filter(str.isdigit, ifile[-12:-8])): ifile for ifile in fileNameLis}
        fileYearLis = sorted(fileNameDic.keys())
    
        ## main context
        if toYear in fileYearLis:
            # update data
            print 'update 2017 data'
            # load 2017 data
            toYearPath = facSavePath + fileNameDic[toYear]
    
            dataOldFacDF = self.ItemArrToDF(toYearPath)
            oldDateEnd = dataOldFacDF.index[-1]
    
            if oldDateEnd == self.dataDSArr[-1]:
                print 'already updated'
    
            else:
                # calculate formula
                dataNewFacDF = dataOldFacDF.reindex(index=self.dataDSArr[toYearFirInd:])
                dataAddDSArr = self.dataDSArr[self.dataDSArr>oldDateEnd]
                dataNewFacDF.loc[dataAddDSArr] = dataFacDF.loc[dataAddDSArr]
                dataNewFacArr = dataNewFacDF.values.astype(float)
                colNames = dataNewFacDF.columns.tolist()
    
                dataDic = {'colNames': np.array(colNames, dtype=object),
                        'indDate': self.dataDSArr[toYearFirInd:].reshape(len(self.dataDSArr[toYearFirInd:]), 1),
                        facName: dataNewFacArr,
                        'arrKey': [facName, 'indDate', 'colNames']}
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
                        'indDate': self.dataDSArr[toYearFirInd:].reshape(len(self.dataDSArr[toYearFirInd:]), 1),
                        facName: dataNewFacArr,
                        'arrKey': [facName, 'indDate', 'colNames']}
            facSavePathName = facSavePath + facName + '_' + str(toYear) + '_arr.mat'
            sio.savemat(facSavePathName, dataDic)
            print '2017 file created'
    
            if pastYear in fileYearLis:
                print 'update 2016 file'
                pastYearPath = facSavePath + fileNameDic[pastYear]
                dataPastOldFacDF = self.FormArrToDF(pastYearPath)
                pastOldDateEnd = dataPastOldFacDF.index[-1]
                if pastOldDateEnd == pastYearLas:
                    print 'do not need to update 2016 file'
                else:
                    dataPastDSArr = self.dataDSArr[(self.dataDSArr>(pastYear*10000)) & (dataDSArr<(toYear*10000))]
                    dataPastFacDF = dataPastOldFacDF.reindex(index=dataPastDSArr, columns=self.dataInnerCodeArr)
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
                dataPastDSArr = self.dataDSArr[self.dataDSArr<=pastYearLas]
                dataPastFacArr = dataPastFacDF.values.astype(float)
                pastDataDic = {'colNames': np.array(colNames, dtype=object),
                               'indDate': dataPastDSArr.reshape(len(dataPastDSArr), 1),
                                facName: dataPastFacArr,
                                'arrKey': [facName, 'indDate', 'colNames']}
                pastSavePathName = facSavePath + facName + '_To' + str(pastYear) + '_arr.mat'
                sio.savemat(pastSavePathName, pastDataDic)
                print 'to2016 file created'
    
        return None

    # ----------------------------------------------------------------------
    # 5. Daily quote adn RA factor. 

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
        savePath= self.facMainDir + 'DailyQuote/'  # DailyQuote factors saved path
        pathQTDaily = self.dataJYDBDir + 'QT_DailyQuote/'
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
        saveFileNameLis = [str(ifile) for ifile in os.listdir(itmeSavePath)]   # !!!
        saveFileNameDic = {float(filter(str.isdigit, ifile)): ifile for ifile in saveFileNameLis}
        saveFileYearLis = sorted(saveFileNameDic.keys())
    
        # past year data
        if len(saveFileYearLis) == 0:
            print 'past year data:'
            dailyPastDic = {}
            for ifileName in fileYearLis[:-1]:
                ifilePath = pathQTDaily + fileNameDic[ifileName]
                print ifileName
                dataPastRaw = self.SheetToDF(ifilePath)
                dataPastCol = [u'TradingDay', u'InnerCode', item]
                dataPastDFTol = dataPastRaw[dataPastCol]
                dataPastDFUse = dataPastDFTol[dataPastDFTol[u'InnerCode'].isin(self.dataInnerCodeArr)]
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
            dataPastDSUseArr = self.dataDSArr[self.dataDSArr<(pastYear+1)*10000]  # date series used
            dataPastItemAllUseDF = dataPastItemAllUse.loc[dataPastDSUseArr]
            dataPastInnerCodeUseArr = [code for code in self.dataInnerCodeArr if code in dataPastItemAllUseDF.columns]  # inner code used
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
        dataRaw = self.SheetToDF(filePath)
        toYear = int(dataRaw[u'TradingDay'].iloc[0]) / 10000
        print toYear, 'begin: '
        dataDFUse = dataRaw[dataCol]
        dataDFUseSort = dataDFUse.sort_values(by=u'TradingDay')
        dataDFUseSort.set_index([u'TradingDay', u'InnerCode'], inplace=True)
        dataDF = dataDFUseSort[item].unstack()
    
        dataItemAllSortDF = dataDF.sort_index()
        dataItemAllUse = dataItemAllSortDF[~dataItemAllSortDF.index.duplicated()]
    
        dataDSUseArr = self.dataDSArr[self.dataDSArr>(toYear*10000)]  # date series used
        dataItemAllUseDF = dataItemAllUse.loc[dataDSUseArr]   #
        dataItemAllUseDF = dataItemAllUseDF.reindex(columns = self.dataInnerCodeArr)
        dataItemAllUseArr = dataItemAllUseDF.values.astype(float)
    
        dataDic = {'colInnerCode': self.dataInnerCodeArr, \
                   'indDate': dataDSUseArr.reshape(len(dataDSUseArr), 1), \
                   item: dataItemAllUseArr,
                   'arrKey': [item, 'indDate', 'colInnerCode']}
        fileSavePathName = itmeSavePath + 'DailyQuote_' + str(toYear)+ '_' + item + '_arr.mat'
        sio.savemat(fileSavePathName, dataDic)
        print str(toYear) + ' Year data saved'
    
        if (len(saveFileYearLis) >= 2) & (toYear == (saveFileYearLis[-1] + 1)):
            filePath = pathQTDaily + fileNameDic[fileYearLis[-2]]
            dataRaw = self.SheetToDF(filePath)
            pastYear = int(saveFileYearLis[-1])
    
            dataDFUse = dataRaw[dataCol]
            dataDFUseSort = dataDFUse.sort_values(by=u'TradingDay')
            dataDFUseSort.set_index([u'TradingDay', u'InnerCode'], inplace=True)
            dataDF = dataDFUseSort[item].unstack()
    
            dataItemAllSortDF = dataDF.sort_index()
            dataItemAllUse = dataItemAllSortDF[~dataItemAllSortDF.index.duplicated()]
    
            dataDSUseArr = self.dataDSArr[(self.dataDSArr>(pastYear*10000)) * (dataDSArr<(toYear*10000))]  # date series used
            dataItemAllUseDF = dataItemAllUse.loc[dataDSUseArr]   #
    
            dataItemAllUseDF = dataItemAllUseDF.reindex(columns = self.dataInnerCodeArr)
            dataItemAllUseArr = dataItemAllUseDF.values.astype(float)
    
            dataDic = {'colInnerCode': self.dataInnerCodeArr, \
                       'indDate': dataDSUseArr.reshape(len(dataDSUseArr), 1), \
                       item: dataItemAllUseArr,
                       'arrKey': [item, 'indDate', 'colInnerCode']}
            fileSavePathName = itmeSavePath + 'DailyQuote_' + str(pastYear)+ '_' + item + '_arr.mat'
            sio.savemat(fileSavePathName, dataDic)
            print str(pastYear) + ' Year data saved'
        return dataDic
    
    def RAFactorGet(self):
        """RatioAdjusting Factors"""
        # every time calculate all date
        pathRAFactor = self.dataJYDBDir + 'QT_AdjustingFactor/QT_AdjustingFactor.mat'
        savePath= self.facMainDir + 'DailyQuote/'  # DailyQuote factors saved path
        itmeSavePath = savePath + 'RatioAdjustingFactor/'
        if not os.path.exists(itmeSavePath):
            os.mkdir(itmeSavePath)
        dataRADF = self.SheetToDF(pathRAFactor)
        dataCol = [u'ExDiviDate', u'RatioAdjustingFactor', u'InnerCode']
        dataDFTol = dataRADF[dataCol]
        # transpose and fillna
        dataDFUse = dataDFTol[dataDFTol[u'InnerCode'].isin(self.dataInnerCodeArr)]
        dataDFUseSort = dataDFUse.sort_values(by=[u'ExDiviDate', u'InnerCode'])
        dataDFUseSta = dataDFUseSort.set_index([u'ExDiviDate', u'InnerCode'])[u'RatioAdjustingFactor'].unstack()
        dataDFUseFil = dataDFUseSta.fillna(method='ffill')
        dataDFUseFilTol = dataDFUseFil.fillna(1.)
        # total time fillna\
        dataUseTolTime = dataDFUseFilTol.loc[self.dataDSArr]      # this way may be good~
        dataUseTolTimeFil = dataUseTolTime.fillna(method='ffill')
        dataUseTolTimeFil = dataUseTolTimeFil.fillna(1.)
        # total InnerCode fillna
        dataUseTolFil = dataUseTolTimeFil.reindex(columns=self.dataInnerCodeArr, fill_value=1.)
        # calculate adjusting factors
        dataAdFactors = dataUseTolFil / dataUseTolFil.iloc[-1]
        # save data
        dataDic = {'colInnerCode': self.dataInnerCodeArr, \
                   'indDate': self.dataDSArr.reshape(len(self.dataDSArr), 1), \
                   'RatioAdjustingFactor': dataAdFactors.values.astype(float),\
                   'arrKey': ['RatioAdjustingFactor', 'indDate', 'colInnerCode']}
        sio.savemat(itmeSavePath + 'RatioAdjustingFactor_arr.mat', dataDic)
        return dataDic
    
    def AdjCloseGet(self):
        # every time calculate all date
        facName = 'AdjClosePrice'
        pathCloseDaily = self.facMainDir + 'DailyQuote/ClosePrice/'
        fileNameLis = os.listdir(pathCloseDaily)
        savePath= self.facMainDir + 'DailyQuote/'  # DailyQuote factors saved path
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
        dataCloseAllDF = pd.concat(dfLis).reindex(index=self.dataDSArr, columns=self.dataInnerCodeArr)
        dataCloseAllArr = dataCloseAllDF.values.astype(float)
        dataRAFactorDic = sio.loadmat(self.facMainDir + 'DailyQuote/RatioAdjustingFactor/RatioAdjustingFactor_arr.mat')
        arrKey = dataRAFactorDic['arrKey']
        dataRAFactorArr = dataRAFactorDic[arrKey[0]]
        dataAdjCloseArr = dataCloseAllArr * dataRAFactorArr
        dataDic = {'colInnerCode': self.dataInnerCodeArr,
                   'indDate': self.dataDSArr.reshape(len(self.dataDSArr), 1),
                    facName: dataAdjCloseArr,
                    'arrKey': [facName, 'indDate', 'colInnerCode']}
        itemSaveName = itemSavePath + facName + '_arr.mat'
        sio.savemat(itemSaveName, dataDic)
        return dataDic
    
    def StoReturnGet(self):
        """all depend on adjusted close price"""
        
        facName = 'StoRet'
        print facName
        savePath= self.facMainDir + 'DailyQuote/'  # DailyQuote factors saved path
        pathAdjClose = savePath + 'AdjClosePrice/AdjClosePrice_arr.mat'

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
            dataOldStoRetDF = self.FormArrToDF(toYearPath)
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
                dataPastOldStoRetDF = self.FormArrToDF(pastYearPath)
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
        _ = self.DailyQuoteGet(u'ClosePrice')
        
        # Volume
        _ = self.DailyQuoteGet(u'TurnoverVolume')
        
        # Turnover value
        _ = self.DailyQuoteGet(u'TurnoverValue')
        
        # Adjusting price factors
        _ = self.RAFactorGet()
        
        # Adjusted Close
        _ = self.AdjCloseGet()
        
        # stock log return
        self.StoReturnGet()

        return None


    # ----------------------------------------------------------------------
    # 6. index quote

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
        # save file
        pathQTDaily = self.dataJYDBDir + 'QT_IndexQuote/'
        savePathMain = self.facMainDir + 'IndexQuote/'
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
            dataRaw = self.SheetToDF(ifilePath)
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
    
        dataItemAllUseDF = dataItemAllUse.loc[self.dataDSArr]   #
        self.UpdateItemDataGet(dataItemAllUseDF, indexSavePath, facName)   
        return None
    
    def IndexLogReturnGet(self, mar='HS300'):
        dicPath = {'HS300': self.facMainDir+'IndexQuote/HS300/HS300_ClosePrice'}
        closePath = dicPath[mar]
        indexPath = os.path.split(closePath)[0]
    
        facName = mar + '_Return'
        savePath = indexPath + '/' + facName + '/'
        if not os.path.exists(savePath):
            os.mkdir(savePath)
    
        indexDataDF = self.AllItemArrToDF(closePath)
        IndexLogReturnDF = pd.DataFrame(index=indexDataDF.index, columns=[facName])
        IndexLogReturnDF.iloc[:, 0] = np.log(indexDataDF[u'ClosePrice']) - np.log(indexDataDF[u'PrevClosePrice'])
    #    if Free:
    #            pathFreeRet = self.facMainDir + 'Common/Wind_Daily10YearBond_LogReturn_array.mat'
    #            dataFreeRetArr = sio.loadmat(pathFreeRet)['TenYearBond_LogReturn']
    #            IndexLogReturnArr = IndexLogReturnArr - dataFreeRetArr
    #            mar = mar + 'Free'
        self.UpdateItemDataGet(IndexLogReturnDF, indexPath, facName)
        return None
    
    def BondReturnGet(self):
        """from wind 10 years bond """
        savePathMain = self.facMainDir + 'IndexQuote/'
        facName = 'BondReturn'
        facSavePath = savePathMain + facName + '/'
        if not os.path.exists(facSavePath):
            os.mkdir(facSavePath)
        path = self.dataComDir + 'bond_10y.mat'
        dataRawDF = self.SheetToDF(path)
        dataDF = dataRawDF.set_index('date')
        dataDF = dataDF.reindex(self.dataDSArr)
        dataPrice = dataDF.values.astype(float)
        dataReturn = pd.DataFrame(index=self.dataDSArr, columns=['Return'])
        dataReturn.iloc[1:] = np.log(dataPrice[1:]) - np.log(dataPrice[:-1])  # log return
        self.UpdateItemDataGet(dataReturn, savePathMain, facName)
        return None

    def IndexQuote(self):
        """get index quote data"""
        # HS300 Index Close
        print 'Get HS300 Index close.'
        self.IndexQuoteGet(mar='HS300', facName='ClosePrice', items=[u'PrevClosePrice', u'ClosePrice'])
        
        print 'Get HS300 Index return.'
        # HS300 Index Return
        self.IndexLogReturnGet(mar='HS300')
        
        # Wind 10 year Bond Return
        print 'Get wind 10 year bond return.'
        self.BondReturnGet()
        return None

    def IndexExposure(self):
        pass

    # ----------------------------------------------------------------------
    # 7. factor common fundamental data

    def AFloatsGet(self):
        # May use FormArrToDF function.
        savePath = self.facMainDir + 'CompanyFundamentalFactors/'
        facName = 'AFloats'
        # load income statement new data
        pathST = self.dataJYDBDir + 'LC_ShareStru/sharestru.mat'
        dataRaw = self.SheetToDF(pathST)
        dataColUseLis = [u'CompanyCode', u'EndDate', facName]   #use enddate
        dataValuesTolArr = dataRaw[dataColUseLis]
    
        # dataframe, select by company code and mark
        dataValuesTolDF = pd.DataFrame(dataValuesTolArr, columns=dataColUseLis)
        dataValuesTolDF = dataValuesTolDF[dataValuesTolDF[u'CompanyCode'].isin(self.dataComCodeArr)]
    
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
        dataFacDF = pd.DataFrame(index=self.dataDSArr, columns=self.dataComCodeArr)
        for iicode, code in enumerate(dataComCodeUse):
            dataOneCodeTolDF = dataValuesDic[code]
            dataOneCodeTolDF[u'EndDate'] = dataOneCodeTolDF.index
            dataOneCodeTSRaw = dataOneCodeTolDF.index.tolist()
            dataOneCodeTSTol = sorted(set(self.dataDSArr) | set(dataOneCodeTSRaw))
            dataOneCodeUseDF = dataOneCodeTolDF.reindex(dataOneCodeTSTol, method='ffill').loc[self.dataDSArr]
            if dataOneCodeUseDF.size==0:
                continue
            dataFacDF[code] = dataOneCodeUseDF[facName]
            if iicode % 100 == 0:
                print 'code', code, 'data got'
        print facName, 'dic got', time.strftime("%H:%M:%S", time.localtime())
    
        # convert to innercode
        dataFacDF.columns = self.dataInnerCodeArr
    
        # year used
        toYear = int(self.dataDSArr[-1])/10000
        toYearFirInd = np.where(self.dataDSArr > toYear*10000)[0][0]
        toYearFir = self.dataDSArr[toYearFirInd]
    
        pastYear = toYear - 1
        pastYearLasInd = toYearFirInd - 1
        pastYearLas = self.dataDSArr[pastYearLasInd]
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
            dataOldFacDF = self.FormArrToDF(toYearPath)
            oldDateEnd = dataOldFacDF.index[-1]
    
            if oldDateEnd == self.dataDSArr[-1]:
                print 'already updated'
    
            else:
                # calculate formula
                dataNewFacDF = dataOldFacDF.reindex(index=self.dataDSArr[toYearFirInd:], columns=self.dataInnerCodeArr)
                dataAddDSArr = self.dataDSArr[self.dataDSArr>oldDateEnd]
                dataNewFacDF.loc[dataAddDSArr] = dataFacDF.loc[dataAddDSArr]
                dataNewFacArr = dataNewFacDF.values.astype(float)
                dataDic = {'colInnerCode': self.dataInnerCodeArr,  # depend on adj close innercode
                        'indDate': self.dataDSArr[toYearFirInd:].reshape(len(self.dataDSArr[toYearFirInd:]), 1), # depend on adj close date
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
            dataDic = {'colInnerCode': self.dataInnerCodeArr,  # depend on adj close innercode
                        'indDate': self.dataDSArr[toYearFirInd:].reshape(len(self.dataDSArr[toYearFirInd:]), 1), # depend on adj close date
                        facName: dataNewFacArr,
                        'arrKey': [facName, 'indDate', 'colInnerCode']} 
            facSavePathName = facSavePath + facName + '_' + str(toYear) + '_arr.mat'
            sio.savemat(facSavePathName, dataDic)
            print '2017 file created'
    
            if pastYear in fileYearLis:
                print 'update 2016 file'
                pastYearPath = facSavePath + fileNameDic[pastYear]
                dataPastOldFacDF = self.FormArrToDF(pastYearPath)
                pastOldDateEnd = dataPastOldFacDF.index[-1]
                if pastOldDateEnd == pastYearLas:
                    print 'do not need to update 2016 file'
                else:
                    dataPastDSArr = self.dataDSArr[(self.dataDSArr>(pastYear*10000)) & (dataDSArr<(toYear*10000))]
                    dataPastFacDF = dataPastOldFacDF.reindex(index=dataPastDSArr, columns=self.dataInnerCodeArr)
                    dataPastAddDSArr = dataPastDSArr[dataPastDSArr>pastOldDateEnd]
                    dataPastFacDF.loc[dataPastAddDSArr] = dataFacDF.loc[pastOldDateEnd:pastYearLas]
                    dataPastFacArr = dataPastFacDF.values.astype(float)
                    pastDataDic = {'colInnerCode': self.dataInnerCodeArr,  # depend on adj close innercode
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
                dataPastDSArr = self.dataDSArr[self.dataDSArr<=pastYearLas]
                dataPastFacArr = dataPastFacDF.values.astype(float)
                pastDataDic = {'colInnerCode': dataPastFacDF.columns.tolist(),
                               'indDate': dataPastDSArr.reshape(len(dataPastDSArr), 1),
                                facName: dataPastFacArr,
                                'arrKey': [facName, 'indDate', 'colInnerCode']}
                pastSavePathName = facSavePath + facName + '_To' + str(pastYear) + '_arr.mat'
                sio.savemat(pastSavePathName, pastDataDic)
                print 'to2016 file created'
        return None

    # ----------------------------------------------------------------------
    # 8. factor common methods

    def FactorFMReturnGet(self, dataLoadDic, savePath='', facName='Factor', pool='A'):
        # 1. load data
        # make dir
        facName = facName + '_FMReturn' + '_' + pool
        ROESavePath = savePath + facName + '/'
        dataLoadLis = dataLoadDic.values()
        for code in dataLoadDic.keys():
            dataLoadDic[code].columns = [code]
    
        dataLoadDF = pd.concat(dataLoadLis, axis=1)
        dataLoadDF = dataLoadDF.sort_index()
    
        # convert company code to innercode !
        dataAllDF = dataLoadDF.reindex(columns=self.dataComCodeArr)
        dataAllDF.columns = self.dataInnerCodeArr
        dataFactorYearUseDF = dataAllDF.dropna(how='all')
    
        ## load stoct daily returns
        pathStoLogRet = self.facMainDir + 'DailyQuote/StoRet/'
        dataStoRetArr = self.AllFormArrToDF(pathStoLogRet).values.astype(float)
    
        ## load stock daily volumne
        pathVol = self.facMainDir + 'DailyQuote/TurnoverVolume/'
        dataVolArr = self.AllFormArrToDF(pathVol).values.astype(float)  # columns: inner code
    
        ## load stock AFloats
        pathAF = self.facMainDir + 'CompanyFundamentalFactors/AFloats/'
        dataAFloatsArr = self.AllFormArrToDF(pathAF).values.astype(float)
    
        dataInnerCodeUseArr = self.dataInnerCodeArr  # seems not useless, just a mark
        dataYearUseLis = dataFactorYearUseDF.index.tolist()       # 27
    
    
        # constant
        thrNum = 100
        if pool == 'HS300':
            print 'HS300 pool'
            # load HS300 index  0/1 sheet
            thrNum = 15
            dataGroupDateLis = [(iyear*10000+430) for iyear in dataYearUseLis]  # +430 not 0430!!!
    
            dataHS300IndexDF = self.HS300IndexDF
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
    
        # 2. seperate 3 groups
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
    
        # 3. calculate the Factor value-weighted stock return
        yearGroupLis = sorted(threeGroupsDic['low'].keys())
    
        ## calculate grouped Factor daily return
        dataVolUseArr = np.zeros((len(self.dataDSArr), len(dataInnerCodeUseArr)))
        dataReturnUseArr = np.zeros((len(self.dataDSArr), len(dataInnerCodeUseArr)))
        dataAFloatsUseArr = np.zeros((len(self.dataDSArr), len(dataInnerCodeUseArr)))
        dataReturnUseArr[:] = np.nan
        dataVolUseArr[:] = np.nan
        dataAFloatsUseArr[:] = np.nan
    
        #bool1Arr = np.where((~np.isnan(dataVolArr[1])) & (dataVolArr[1]!=0))
        for i in range(len(self.dataDSArr)):
            posUseArr = np.where((~np.isnan(dataVolArr[i])) & (dataVolArr[i]!=0))[0]
            if len(posUseArr) == 0:
                continue
            dataVolUseArr[i][posUseArr] = dataVolArr[i][posUseArr]
            dataReturnUseArr[i][posUseArr] = dataStoRetArr[i][posUseArr]
            dataAFloatsUseArr[i][posUseArr] = dataAFloatsArr[i][posUseArr]
    
        dataReturnDF = pd.DataFrame(dataReturnUseArr, index=self.dataDSArr, columns=dataInnerCodeUseArr)
        dataAFloatsDF = pd.DataFrame(dataAFloatsUseArr, index=self.dataDSArr, columns=dataInnerCodeUseArr)
    
        # three groups return
        dataFactorReturnDF = pd.DataFrame([], index=self.dataDSArr, columns=['low', 'median', 'high', 'HML'])
        counts = 0
    
        print 'start divide group', time.strftime("%H:%M:%S", time.localtime())
        print 'date'
        for year in yearGroupLis:
            groupTemLis = [threeGroupsDic[i][year] for i in ['low', 'median', 'high']]
            for date in self.dataDSArr[(self.dataDSArr>(year*10000+430)) & (self.dataDSArr<((year+1)*10000+501))]:
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
        self.UpdateItemDataGet(dataFactorReturnDF, savePath, facName)
        return ROESavePath
    
    def FactorFMExposureGet(self, facReturnPath, facName, pool, regDays=250, per=0.2, index=3):
        # dataFactorReturnArr is based on the result of function FactorFMReturnGet() dataFactorReturnDF
        returnPath = facReturnPath.rstrip('/')
        facPath = os.path.split(returnPath)[0] + '/'
        facName = facName + '_FMExposure' + '_' + pool
    
    #    facName=factName
        dataFactorReturnArr = self.AllItemArrToDF(facReturnPath).values.astype(float)[:, index]
        # load stock return
        ## load stoct daily returns
        pathStoLogRet = self.facMainDir + 'DailyQuote/StoRet/'
        dataStoRetArr = self.AllFormArrToDF(pathStoLogRet).values.astype(float)
        # load free returns
        pathFreeRet = self.facMainDir + 'IndexQuote/BondReturn/'
        dataFreeRetArr = self.AllItemArrToDF(pathFreeRet).values.astype(float)
    
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
    
        for d in range(startInd, len(self.dataDSArr)):
    
            YTemp = dataStoFreeRetArr[(d-regDays+1):(d+1)]
            XTemp = dataFactorReturnArr[(d-regDays+1):(d+1)]
            for s in range(len(self.dataInnerCodeArr)):
                useIndArr = np.where(~np.isnan(YTemp[:, s]))[0]
                if len(useIndArr) > (regDays * per):   #
                    result = sm.OLS(YTemp[useIndArr, s], XTemp[useIndArr]).fit()
                    dataFactorExpArr[d, s] = result.params[1]
            if d%100 == 0:
                print self.dataDSArr[d], time.strftime("%H:%M:%S", time.localtime())
        dataFactorExpDF = pd.DataFrame(dataFactorExpArr, index=self.dataDSArr, columns=self.dataInnerCodeArr)
        self.UpdateFormDataGet(dataFactorExpDF, facPath, facName)
        return
    
    def FactorBarraReturnGet(self, loadDF, facPath, facName='Factor', pool='A', index=0):
        """
        load dataDic as follows:
        arrName = facName + 'Values_Three3DArray'
        dataDic = {'axis1Names_Items': np.array(itemsLis, dtype=object),
                   'axis2Names_DateSeries': self.dataDSArr.reshape(len(self.dataDSArr), 1),\
                   'axis3Names_ComCode': self.dataComCodeArr,\
                   arrName: data3DArr, \
                   'arrKey': [arrName, 'axis1Names_Items', 'axis2Names_DateSeries', 'axis3Names_ComCode']}
        """
        facName = facName + '_BarraReturn_' +  pool
        # load stock log return
        pathStoLogRet = self.facMainDir + 'DailyQuote/StoRet/'
        dataStoRetArr = self.AllFormArrToDF(pathStoLogRet).values.astype(float)
    
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
    
            dataHS300IndexDF = self.HS300IndexDF
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
                    print self.dataDSArr[i]
        dataBarraRetDF = pd.DataFrame(dataFactorOLSReturn, index=self.dataDSArr, columns=[facName])
        self.UpdateItemDataGet(dataBarraRetDF, facPath, facName)          
        return dataFactorOLSReturn

    def FacDicTo3DArrDicGet(self, dataRawDic, facName='Factor'):
        comCodeLis = dataRawDic.keys()
        itemsLis = dataRawDic[comCodeLis[0]].columns.tolist()  # item order !
        dataFormatDic = {}
        for iitem in itemsLis:
            dataFormatDic[iitem] = pd.DataFrame(index=self.dataDSArr, columns=self.dataComCodeArr)
    
        print 'start convert to 3D form array: ',
        print time.strftime("%H:%M:%S", time.localtime())
        print 'code counts', 'code'
        for iicode, icode in enumerate(comCodeLis):
            if dataRawDic[icode].size==0:
                continue
            pubDateLis = dataRawDic[icode].index.tolist()
            pubDateLis.extend(list(self.dataDSArr))
            allDateArr = np.unique(pubDateLis)
            # famative date process
            icodeDF = dataRawDic[icode].reindex(index=allDateArr, method='ffill')
            icodeDefDF = icodeDF.loc[self.dataDSArr]
            for iitem in icodeDefDF.columns:
                dataFormatDic[iitem][icode] = icodeDefDF[iitem]
    
            if iicode%100 == 0:
                print iicode, icode
    
        data3DArr = np.zeros((len(itemsLis), len(self.dataDSArr), len(self.dataComCodeArr)))
        data3DArr[:] = np.nan
        for iiitem, iitem in enumerate(itemsLis):
            arrTemp = dataFormatDic[iitem].values.astype(float)
            data3DArr[iiitem] = arrTemp
    
        arrName = facName + '_3DValues'
        dataDic = {'axis1Names_Items': np.array(itemsLis, dtype=object),
                   'axis2Names_DateSeries': self.dataDSArr.reshape(len(self.dataDSArr), 1),\
                   'axis3Names_ComCode': self.dataComCodeArr,\
                   arrName: data3DArr,
                   'arrKey': [arrName, 'axis1Names_Items', 'axis2Names_DateSeries', 'axis3Names_ComCode']}
        return dataDic

    def DivGroRetGet(self, loadPath, divGroNum=10, divPer='1M', pool='A', facName='Factor', saveBool=False, arrDimIndex=0):
        # TODO: Need modification.  
        # 1. load data
        ## load factor exposure data
        dataFactorExpDic = sio.loadmat(loadPath)
        facArrKey = dataFactorExpDic['arrKey'][0]
        dataFactorExpArr = dataFactorExpDic[facArrKey]
        if dataFactorExpArr.ndim == 3 :
            dataFactorExpArr = dataFactorExpArr[arrDimIndex]
    
        dataFactorExpDF = pd.DataFrame(dataFactorExpArr, index=self.dataDSArr, columns=self.dataInnerCodeArr)
    
        ## load stoct daily returns
        pathStoLogRet = self.facMainDir + 'DailyQuote/DailyQuote_LogReturn_array.mat'
        dataStoRetArr = sio.loadmat(pathStoLogRet)['StoLogReturn']
    
        ## load stock daily volumne
        pathVol = self.facMainDir + 'DailyQuote/DailyQuote_TurnoverVolume_array.mat'
        dataVolRaw = sio.loadmat(pathVol)
        dataVolArr = dataVolRaw[u'TurnoverVolume']  # columns: inner code
    
        ## load stock AFloats
        pathAF = self.facMainDir + 'CompanyFundamentalFactors/Afloats/LC_AFloats_mat.mat'
        dataAFloatsRaw = sio.loadmat(pathAF)
        dataAFloats3DArr = dataAFloatsRaw['LC_AFloats']
        dataAFloatsArr = dataAFloats3DArr[0]
    
        # constant
        thrNum = 100
        if pool == 'HS300':
            print 'HS300 pool'
            thrNum = 15
            # load HS300 index  0/1 sheet
            dataHS300IndexDF = self.HS300IndexDF
            dataHS300IndexDF[dataHS300IndexDF==0] = np.nan
            dataFactorExpDF = dataHS300IndexDF * dataFactorExpDF
            dataFactorExpArr = dataFactorExpDF.values.astype(float)
    
            dataHS300IndexArr = dataHS300IndexDF.values.astype(float)
            dataStoRetArr = dataStoRetArr * dataHS300IndexArr
            dataVolArr = dataVolArr * dataHS300IndexArr
            dataAFloatsArr = dataAFloatsArr * dataHS300IndexArr
    
        dataVolUseArr = np.zeros((len(self.dataDSArr), len(self.dataInnerCodeArr)))
        dataReturnUseArr = np.zeros((len(self.dataDSArr), len(self.dataInnerCodeArr)))
        dataAFloatsUseArr = np.zeros((len(self.dataDSArr), len(self.dataInnerCodeArr)))
        dataReturnUseArr[:] = np.nan
        dataVolUseArr[:] = np.nan
        dataAFloatsUseArr[:] = np.nan
    
        #bool1Arr = np.where((~np.isnan(dataVolArr[1])) & (dataVolArr[1]!=0))
        for i in range(len(self.dataDSArr)):
            posUseArr = np.where((~np.isnan(dataVolArr[i])) & (dataVolArr[i]!=0))[0]
            if len(posUseArr) == 0:
                continue
            dataVolUseArr[i][posUseArr] = dataVolArr[i][posUseArr]
            dataReturnUseArr[i][posUseArr] = dataStoRetArr[i][posUseArr]
            dataAFloatsUseArr[i][posUseArr] = dataAFloatsArr[i][posUseArr]
    
        dataStoRetDF = pd.DataFrame(dataReturnUseArr, index=self.dataDSArr, columns=self.dataInnerCodeArr)
        dataAFloatsDF = pd.DataFrame(dataAFloatsUseArr, index=self.dataDSArr, columns=self.dataInnerCodeArr)
        
        # 2. seperate groups and calculate groups returns
        colNames = ['group'+str(i+1) for i in range(divGroNum)]
        dataFacGroReturnDF = pd.DataFrame(index=self.dataDSArr, columns=colNames)
    
        staInd = self.nonNanFirInd(dataFactorExpArr)
    
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
                dsTemp = self.dataDSArr[(self.dataDSArr>monEndDateArr[iimonendDate]) & (self.dataDSArr<=monEndDateArr[iimonendDate+1])]
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
                 'indDate': self.dataDSArr.reshape(len(self.dataDSArr), 1),
                 arrName: dataFacGroReturnArr, \
                 'arrKey': [arrName, 'indDate', 'colNames']}
    
        if saveBool :
            savePath = os.path.split(loadPath)[0]
            saveName = savePath + '/' + arrName + '_arr.mat'
            sio.savemat(saveName, dataDic)
            print arrName + '_array.mat', 'saved ~'
    
        return dataFacGroReturnArr
    
    def DivGroExcRetGraphGet(self, loadArr=None, loadPath=None, facName_Pool='Factor'):
        # TODO: Need modification. 
        corUseLis = ['lightcoral', 'red', 'gold', 'lawngreen',\
                    'darkgreen', 'aquamarine', 'dodgerblue', 'blue', 'mediumorchid', 'fuchsia', 'pink']
        if loadArr is not None:
            dataRetRawArr = loadArr
        else:
            dataRawDic = sio.loadmat(loadPath)
            facArrKey = dataRawDic['arrKey'][0]
            dataRetRawArr = dataRawDic[facArrKey]
    
        pathMar = self.facMainDir + 'IndexQuote/HS300/HS300_Return/'
        dataMarRetRaw = sio.loadmat(pathMar)
        dataMarRetArr = dataMarRetRaw[dataMarRetRaw['arrKey'][0]]
    
        dataRetArr = dataRetRawArr.copy()
        startGroInd = self.nonNanFirInd(dataRetArr)
        startMarInd = self.nonNanFirInd(dataMarRetArr)
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
            ax1.plot(range(len(self.dataDSArr)), dataRetCumArr[:, i], color=corUseLis[i], lw=1.5, label='Group'+str(i+1))
    
        ax1.set_xlim(startInd-250, len(self.dataDSArr)+400)
    
    #    ax1.set_ylim(-0.5, 2.5 )
        ax1.set_xticks(range(startInd, len(self.dataDSArr), 250))
        ax1.set_xticklabels([self.dataDSArr[i] for i in ax1.get_xticks()], rotation=30, fontsize='small')
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

    # ----------------------------------------------------------------------
    # 9. factors

    # ROE
    # ---
    # NOTE: will add some note.
    # TODO: may be packaged to one function.

    def NetprofitDicGet(self): 
        # 1. get netprofit data
        # load non financial income statement_new data
        pathNFIC = self.dataJYDBDir + 'LC_IncomeStatementNew/LC_IncomeStatementNew.mat'
        dataNFICRaw = self.SheetToDF(pathNFIC)
        dataNFICColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'NetProfit']
        dataNFIncomeTolArr = dataNFICRaw[dataNFICColUseLis]
        # dataframe, select by company code and mark
        dataNFIncomeTolDF = pd.DataFrame(dataNFIncomeTolArr, columns=dataNFICColUseLis)    # 923302
        dataNFIncomeUseDF = dataNFIncomeTolDF[dataNFIncomeTolDF[u'CompanyCode'].isin(self.dataComCodeArr)]  # 667895
        dataNFIncomeUseDF = dataNFIncomeUseDF[dataNFIncomeUseDF[u'Mark'].isin([1, 2])]      # 293845
        dataNFIncomeUseDF = dataNFIncomeUseDF[dataNFIncomeUseDF[u'NetProfit'].notnull()]    #293805
    
        # load financial income statement_new data
        pathFIC = self.dataJYDBDir + 'LC_FIncomeStatementNew/LC_FIncomeStatementNew.mat'
        dataFICRaw = self.SheetToDF(pathFIC)
        dataFICColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'NetProfit']
        dataFIncomeTolArr = dataFICRaw[dataFICColUseLis]
    
        # dataframe, select by company code and mark
        dataFIncomeTolDF = pd.DataFrame(dataFIncomeTolArr, columns=dataFICColUseLis)    # 25283
        dataFIncomeUseDF = dataFIncomeTolDF[dataFIncomeTolDF[u'CompanyCode'].isin(self.dataComCodeArr)]  # 9550
        dataFIncomeUseDF = dataFIncomeUseDF[dataFIncomeUseDF[u'Mark'].isin([1, 2])]      # 4500
        dataFIncomeUseDF = dataFIncomeUseDF[dataFIncomeUseDF[u'NetProfit'].notnull()]    #4493
    
    
        # look for duplicated companycode
        dataNFICComCodeUse = np.unique(dataNFIncomeUseDF[u'CompanyCode'])             # used company code, 3364 counts
        dataFICComCodeUse = np.unique(dataFIncomeUseDF[u'CompanyCode'])             # used company code, 61 counts
    
    
        #dataDupComCodeSet = set(dataNFComCodeUse) & set(dataFComCodeUse)
        #dataTolComCodeSet = set(dataNFComCodeUse) | set(dataFComCodeUse)
        dataDupComCode = np.unique(list(set(dataNFICComCodeUse) & set(dataFICComCodeUse)))   # duplicated code  11
        dataTolComCode = np.unique(list(set(dataNFICComCodeUse) | set(dataFICComCodeUse)))   # total code use 3414
    
        dataNFEComCode = np.unique(list(set(dataNFICComCodeUse) - set(dataFICComCodeUse)))        # NF effective code  3353
    #    dataFEComCode = np.unique(list(set(dataFICComCodeUse) - set(dataNFICComCodeUse)))          # F effective code  50
    
        # sort by company code , published date, end date, mark
        dataNFIncomeUseDFSor = dataNFIncomeUseDF.sort_values(by=[u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark'],
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
    
        return dataTolIncomeDic
    
    # 2. get equity data
    def EquityDicGet(self):
    
        # load non financial balance statement_new data
        pathNF = self.dataJYDBDir + 'LC_BalanceSheetNew/LC_BalanceSheetNew.mat'
        dataNFRaw = self.SheetToDF(pathNF)
        dataNFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'TotalShareholderEquity', u'DeferredTaxAssets', \
                           u'EPreferStock']
        dataNFBalanceTolArr = dataNFRaw[dataNFColUseLis]
    
        # dataframe, select by company code and mark
        dataNFBalanceTolDF = pd.DataFrame(dataNFBalanceTolArr, columns=dataNFColUseLis)    # 789264
        dataNFBalanceUseDF = dataNFBalanceTolDF[dataNFBalanceTolDF[u'CompanyCode'].isin(self.dataComCodeArr)]  # 544258
        dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceUseDF[u'Mark'].isin([1, 2])]      # 287129
        dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceUseDF[u'TotalShareholderEquity'].notnull()]    #287097
        dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceUseDF[u'TotalShareholderEquity']!=0]    #287075
    
        # load financial balance statement_new data
        pathF = self.dataJYDBDir + 'LC_FBalanceSheetNew/LC_FBalanceSheetNew.mat'
        dataFRaw = self.SheetToDF(pathF)
        dataFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'TotalShareholderEquity', u'DeferredTaxAssets', \
                          u'EPreferStock']
        dataFBalanceTolArr = dataFRaw[dataFColUseLis]
    
        # dataframe, select by company code and mark
        dataFBalanceTolDF = pd.DataFrame(dataFBalanceTolArr, columns=dataFColUseLis)    # 23090
        dataFBalanceUseDF = dataFBalanceTolDF[dataFBalanceTolDF[u'CompanyCode'].isin(self.dataComCodeArr)]  # 7902
        dataFBalanceUseDF = dataFBalanceUseDF[dataFBalanceUseDF[u'Mark'].isin([1, 2])]      # 4438
        dataFBalanceUseDF = dataFBalanceUseDF[dataFBalanceUseDF[u'TotalShareholderEquity'].notnull()]    #4428
        dataFBalanceUseDF = dataFBalanceUseDF[dataFBalanceUseDF[u'TotalShareholderEquity']!=0]    #4428
    
        # look for duplicated companycode
        dataNFComCodeUse = np.unique(dataNFBalanceUseDF[u'CompanyCode']) # used company code, income:3364 counts  banlenc:3363
        dataFComCodeUse = np.unique(dataFBalanceUseDF[u'CompanyCode'])   # used company code, income:61 counts, balence: 61
    
        #dataDupComCodeSet = set(dataNFComCodeUse) & set(dataFComCodeUse)
        #dataTolComCodeSet = set(dataNFComCodeUse) | set(dataFComCodeUse)
        dataDupComCode = sorted(set(dataNFComCodeUse) & set(dataFComCodeUse))   # duplicated code  income:11,  balence: 10
        dataTolComCode = sorted(set(dataNFComCodeUse) | set(dataFComCodeUse))   # total code use income:3414, balence:3414
    
        dataNFEComCode = sorted(set(dataNFComCodeUse) - set(dataFComCodeUse))   # NF effective code income:3353, balence:3353
    #    dataFEComCode = sorted(set(dataFComCodeUse) - set(dataNFComCodeUse))    # F effective code  income:50, balence:51
    
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
                dataTolBalanceDic[code] = dataDupBalanceDFTemp
            elif code in dataNFEComCode:
                dataTolBalanceDic[code] = dataNFBalanceUseDFInd.loc[code]
            else:
                dataTolBalanceDic[code] = dataFBalanceUseDFInd.loc[code]
    
        return dataTolBalanceDic

    # 3. ROE_FMDicGet
    def ROE_FMDicGet(self):
    
    #    ROESavePath = self.facMainDir + 'CompanyFundamentalFactors/ROE/'
        # 1. calculate ROE
        # start calculate FM year duration ROE value
    
        print 'start:', time.strftime('%H:%M:%S', time.localtime())
        dataTolIncomeDic = self.NetprofitDicGet()
        print 'netprofit dic got'
    
        dataTolBalanceDic = self.EquityDicGet()
        print 'equity dic got'
    
        #    # create a new df dict
    
        netprofitDic = {}
        for number, code in enumerate(dataTolIncomeDic.keys()):
            dfIncomeOneCode = dataTolIncomeDic[code]
            pubDateArr = np.unique(dfIncomeOneCode.index)
            pubYearArr = np.unique([int(i)/10000 for i in pubDateArr])
            dfOneCodeUse = pd.DataFrame(columns=[u'NetProfit'])
            for year in pubYearArr:
                dateIndArr = np.where((pubDateArr>(year*10000)) & (pubDateArr<(year*10000+501)))[0]
                pubDateUseArr = pubDateArr[dateIndArr]  # array
                lastYearDate = (year-1) * 10000 + 1231
                if (len(dateIndArr) > 0) & (lastYearDate in dfIncomeOneCode.loc[pubDateUseArr, u'EndDate'].values):
                    dfIncomOneCodeTemp = dfIncomeOneCode.loc[pubDateUseArr]   # is a df
                    dfIncomOneCodeTemp = dfIncomOneCodeTemp[dfIncomOneCodeTemp[u'EndDate'] == lastYearDate].iloc[-1] # is a series
                    dfOneCodeUse.loc[year, u'NetProfit'] = dfIncomOneCodeTemp[u'NetProfit']
            netprofitDic[code] = dfOneCodeUse
    
        equityDic = {}
        for number, code in enumerate(dataTolBalanceDic.keys()):
            dfBalanceCode = dataTolBalanceDic[code]
            pubDateArr = np.unique(dfBalanceCode.index)
            pubYearArr = np.unique([int(i)/10000 for i in pubDateArr])
            dfOneCodeUse = pd.DataFrame(columns=[u'equity'])
            for year in pubYearArr:
                dateIndArr = np.where((pubDateArr>(year*10000)) & (pubDateArr<(year*10000+501)))[0]
                pubDateUseArr = pubDateArr[dateIndArr]
                lastYearDate = (year-1) * 10000 + 1231
                if (len(dateIndArr) > 0) & (lastYearDate in dfBalanceCode.loc[pubDateUseArr, u'EndDate'].values):
                    dfBalanceOneCodeTemp = dfBalanceCode.loc[pubDateUseArr]
                    dfBalanceOneCodeTemp = dfBalanceOneCodeTemp[dfBalanceOneCodeTemp[u'EndDate'] == lastYearDate].iloc[-1, 2:]
                    dfOneCodeUse.loc[year, u'equity'] = dfBalanceOneCodeTemp.sum()
            equityDic[code] = dfOneCodeUse
    
    
        comCodeUseLis = list(set(netprofitDic.keys()) & set(equityDic.keys()))
        dataROEDic = {}
        for i, code in enumerate(comCodeUseLis):
            netOneCodeDF = netprofitDic[code]
            equityOneCodeDF = equityDic[code]
            ROEOneCodeDF = pd.concat([netOneCodeDF, equityOneCodeDF], axis=1)
            if ROEOneCodeDF.size != 0:
                ROETempDF = pd.DataFrame(columns=['ROE'])
                ROETempDF['ROE'] = ROEOneCodeDF[u'NetProfit'] / ROEOneCodeDF[u'equity']  # use innercode as columns names
                dataROEDic[code] = ROETempDF
        print 'ROE_FM dic completed.', time.strftime('%H:%M:%S', time.localtime())
    
        return dataROEDic
    
    # 4.
    def ROE_BarraDFGet(self):
        """
        This function is to calculate ROE values for subsequent barra return.
        Netprofit is calculated as the year duration data at the newest date.
        """
    
        # working path
    #    pathROE = self.facMainDir + 'CompanyFundamentalFactors/ROE/'
        # load balance, income sheet data, and calculate year duration ROE
        dataTolBalanceDic= self.EquityDicGet()
        print 'equity dic got'
    
        dataTolIncomeDic = self.NetprofitDicGet()
        print 'netprofit dic got'
    
        #
        dataTolNetDic = {}
        print 'begin calculate netprofit value: '
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
    
    #        dfROEOneCode = dfROEOneCode.reindex(columns=[u'ReturnOnEquity', u'EndDate', u'IncomeMark', u'BalanceMark'])
            dataTolROEDic[code] = dfROEOneCode
    
        dataFormatDF = pd.DataFrame(index=self.dataDSArr, columns=self.dataComCodeArr)
        for iicode, icode in enumerate(dataTolComCode):
            if dataTolROEDic[icode].size==0:
                continue
            pubDateLis = dataTolROEDic[icode].index.tolist()
            pubDateLis.extend(list(self.dataDSArr))
            allDateArr = np.unique(pubDateLis)
            # famative date process
            icodeDF = dataTolROEDic[icode].reindex(index=allDateArr, method='ffill')
            icodeDefDF = icodeDF.loc[self.dataDSArr]
            dataFormatDF[icode] = icodeDefDF[u'ReturnOnEquity']
        dataFormatDF.columns = self.dataInnerCodeArr
        print 'ROE_Barra DF completed'
    
        return dataFormatDF

    def ROE_Barra(self):
        """
        This program is to calculate ROE formative values and then barra return.
        Netprofit is calculated as the year duration data at the newest date.
        """
        
        factName = 'ROE'
        ROESavePathMain = self.facMainDir + 'CompanyFundamentalFactors/ReturnOnEquity/'
        
        #%% 1. calculate ROE
        dataROEDF = self.ROE_BarraDFGet()
        self.UpdateFormDataGet(dataROEDF, savePath=ROESavePathMain, facName=factName+'_BarraExposure')
        
        #%% 2. Barra Return
        
        # all stock return
        ROE_A_BarraReturn = self.FactorBarraReturnGet(loadDF=dataROEDF, facPath=ROESavePathMain, facName=factName, pool='A')
        
        # HS300 return
        ROEHS300_BarraReturn = self.FactorBarraReturnGet(loadDF=dataROEDF, facPath=ROESavePathMain, facName=factName, pool='HS300')

        return None

    def ROE_FM(self):
        factName = 'ROE'
        ROESavePathMain = self.facMainDir + 'CompanyFundamentalFactors/ReturnOnEquity/'
        
        #%% 1. calculate ROE

        dataROEDic = self.ROE_FMDicGet()
        #%% 2. seperate groups, and get FM returns, FM Exposure, save file
        
        # all stock return and exposure
        ROEReturnFolderPath = self.FactorFMReturnGet(dataROEDic, savePath=ROESavePathMain, facName=factName, pool='A')
        self.FactorFMExposureGet(ROEReturnFolderPath, facName=factName, pool='A')
        
        #%% HS300 return and exposure
        ROEHS300ReturnPath = self.FactorFMReturnGet(dataROEDic, savePath=ROESavePathMain, pool='HS300', facName=factName)
        self.FactorFMExposureGet(ROEHS300ReturnPath, facName=factName, pool='HS300')
        return None

    # IA
    # --
    # NOTE: 
    # TODO: may be packaged to one function. 
    def IADicGet(self):
        # 1. get datetime series, code numbers we used
        # 2. get data from banlance sheet
        #def equityGet():
        # load non financial balance statement_new data
        pathNF = self.dataJYDBDir + 'LC_BalanceSheetNew/LC_BalanceSheetNew.mat'
        dataNFRaw = self.SheetToDF(pathNF)
        dataNFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'FixedAssets',\
         u'TotalCurrentAssets', u'TotalCurrentLiability', u'TotalAssets']
    
        # dataframe, select by company code and mark
        dataNFBalanceTolDF = dataNFRaw[dataNFColUseLis]
        dataNFBalanceUseDF = dataNFBalanceTolDF[dataNFBalanceTolDF[u'CompanyCode'].isin(self.dataComCodeArr)]  #544258
        dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceUseDF[u'Mark'].isin([1, 2])]      #287129
    
        # dropna nan and zero values
        dataNFBalanceNanInd = ((dataNFBalanceUseDF[u'FixedAssets'].notnull()) & (dataNFBalanceUseDF[u'FixedAssets'] != 0)\
         & (dataNFBalanceUseDF[u'TotalCurrentAssets'].notnull()) & (dataNFBalanceUseDF[u'TotalCurrentAssets'] != 0)\
         & (dataNFBalanceUseDF[u'TotalCurrentLiability'].notnull()) & (dataNFBalanceUseDF[u'TotalCurrentLiability'] != 0)\
         & (dataNFBalanceUseDF[u'TotalAssets'].notnull()) & (dataNFBalanceUseDF[u'TotalAssets'] != 0)  )
    
        dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceNanInd]    #285190
    
    
        # load financial balance statement_new data
        pathF = self.dataJYDBDir + 'LC_FBalanceSheetNew/LC_FBalanceSheetNew.mat'
        dataFRaw = self.SheetToDF(pathF)
        dataFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', u'FixedAssets', u'TotalAssets']
    
        # dataframe, select by company code and mark
        dataFBalanceTolDF = dataFRaw[dataFColUseLis]
        dataFBalanceUseDF = dataFBalanceTolDF[dataFBalanceTolDF[u'CompanyCode'].isin(self.dataComCodeArr)]  # 7902
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
    
    def IABarraExposureGet(self):
        dataIADic = self.IADicGet()
        print 'IADic got'
        comCodeUseLis = dataIADic.keys()
    
        # calculate IA values
        dataIAUse={}
        colNames = [u'IA', u'EndDate']
        print 'Start calculating IA_Barra DF:'
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
    
        dataFormatDF = pd.DataFrame(index=self.dataDSArr, columns=self.dataComCodeArr)
    
        for iicode, icode in enumerate(comCodeUseLis):
            if dataIAUse[icode].size==0:
                continue
            pubDateLis = dataIAUse[icode].index.tolist()
            pubDateLis.extend(list(self.dataDSArr))
            allDateArr = np.unique(pubDateLis)
            # famative date process
            icodeDF = dataIAUse[icode].reindex(index=allDateArr, method='ffill')
            icodeDefDF = icodeDF.loc[self.dataDSArr]
            dataFormatDF[icode] = icodeDefDF[u'IA']
        dataFormatDF.columns = self.dataInnerCodeArr
    
        print 'IA_Barra DF completed'
        return dataFormatDF
    
    def IAFMDicGet(self):
            # load IA data dic
        dataIADic = self.IADicGet()
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

    def IA_Barra(self):
        # calculate Investments to Assets formative values
        factName = 'IA'
        savePathMain = self.facMainDir + 'CompanyFundamentalFactors/InvestmentsToAssets/'
        #%% to formative values, save to 3D array
        IADF = self.IABarraExposureGet()
        self.UpdateFormDataGet(IADF, savePath=savePathMain, facName=factName+'_BarraExposure')
        #%% Barra Return
        # all stock return
        IA_A_BarraReturn = self.FactorBarraReturnGet(loadDF=IADF, facPath=savePathMain, facName=factName, pool='A')
        # HS300 return
        IA_HS300_BarraReturn = self.FactorBarraReturnGet(loadDF=IADF, facPath=savePathMain, facName=factName, pool='HS300')
        return None 

    def IA_FM(self):
        factName = 'IA'
        savePathMain = self.facMainDir + 'CompanyFundamentalFactors/InvestmentsToAssets/'
        
        #%% IA data dic
        dataIADic = self.IAFMDicGet()
        
        #%% all stocks return and exposure
        IAReturnFolderPath = self.FactorFMReturnGet(dataIADic, savePath=savePathMain, facName=factName, pool='A')
        self.FactorFMExposureGet(IAReturnFolderPath, facName=factName, pool='A')
        
        #%% HS300 return and exposure
        IAHS300ReturnPath = self.FactorFMReturnGet(dataIADic, savePath=savePathMain, pool='HS300', facName=factName)
        IA_HS300_Exposure = self.FactorFMExposureGet(IAHS300ReturnPath, facName=factName, pool='HS300')

        return None


if __name__ == '__main__':
    # Make a class: factor. 
    factor = Factor()
    print '\'factor\' created...\n\n'
    # Have tested, is ok~

    # Getting DailyQuote.
    print time.strftime("%H:%M:%S", time.localtime()) + '\tGetting DailyQuote...\n'
    factor.DailyQuote()
    print time.strftime("%H:%M:%S", time.localtime()) + '\tDailyQuote got~\n'
    # Have tested, is ok~

    # Getting IndexQuote. 
    print time.strftime("%H:%M:%S", time.localtime()) + '\tGetting IndexQuote...\n'
    factor.IndexQuote()
    print time.strftime("%H:%M:%S", time.localtime()) + '\tIndexQuote got~\n'
    # Have tested, is ok~

    # Getting Afloats. 
    print time.strftime("%H:%M:%S", time.localtime()) + '\tGetting Afloats...\n'
    factor.AFloatsGet()
    print time.strftime("%H:%M:%S", time.localtime()) + '\tAfloats got~\n'
    # Have tested, is ok~

    # Getting ROE_Barra. 
    print time.strftime("%H:%M:%S", time.localtime()) + '\tGetting ROE_Barra...\n'
    factor.ROE_Barra()
    print time.strftime("%H:%M:%S", time.localtime()) + '\tROE_Barra got~\n'
    # Have tested, is ok~

    # Getting ROE_FM. 
    print time.strftime("%H:%M:%S", time.localtime()) + '\tGetting ROE_Barra...\n'
    factor.ROE_FM()
    print time.strftime("%H:%M:%S", time.localtime()) + '\tROE_Barra got~\n'

    # Getting IA_Barra. 
    print time.strftime("%H:%M:%S", time.localtime()) + '\tGetting IA_Barra...\n'
    factor.IA_Barra()
    print time.strftime("%H:%M:%S", time.localtime()) + '\tIA_Barra got~\n'

    # Getting IA_FM. 
    print time.strftime("%H:%M:%S", time.localtime()) + '\tGetting IA_FM...\n'
    factor.IA_FM()
    print time.strftime("%H:%M:%S", time.localtime()) + '\tIA_FM got~\n'










