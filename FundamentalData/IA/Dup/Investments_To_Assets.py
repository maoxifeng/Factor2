# -*- coding: utf-8 -*-


'''
#==============================================================================
# Invesetments to Assets factor return function
#==============================================================================
'''


import numpy as np
import scipy.io as sio
import pandas as pd

#%%
#==============================================================================
# 1. get datetime series, code numbers we used
#==============================================================================

pathTS =  '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat'     
dataTSRaw = sio.loadmat(pathTS)      
dataTSRaw.keys()
dataTSArr = dataTSRaw['dateSeries'][:, 0]     # 6498

pathCode = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
dataCodeRaw = sio.loadmat(pathCode)
dataCodeRaw.keys()
dataCodeArr = dataCodeRaw['data']
dataInnerCodeArr = dataCodeArr[:, 0]
dataComCodeArr = dataCodeArr[:, 1] # 3415
dataComCodeArr.shape

#pathHS300Code = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/HS300StockCode_mat.mat'
#dataHS300CodeRaw = sio.loadmat(pathHS300Code)
#dataHS300CodeArr = dataHS300CodeRaw['data']
#dataHS300InnerCodeArr = dataHS300CodeArr[:, 0]
#dataHS300ComCodeArr = dataHS300CodeArr[:, 1]
#dataHS300CodeIndArr = dataHS300CodeArr[:, 2]

#%%
#==============================================================================
# 2. get data from banlance sheet
#==============================================================================

#def equityGet():
    

# load non financial balance statement_new data
pathNF = '/data/liushuanglong/MyFiles/Data/JYDB2/LC_BalanceSheetNew/LC_BalanceSheetNew_mat.mat'
dataNFRaw = sio.loadmat(pathNF)  
dataNFColTol = [dataNFRaw['col'][0][i][0] for i in range(dataNFRaw['col'].shape[1])]
dataNFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', 'FixedAssets',\
 u'TotalCurrentAssets', u'TotalCurrentLiability', u'TotalAssets']
dataNFColUseInd = [dataNFColTol.index(i) for i in dataNFColUseLis]
dataNFBalanceTolArr = dataNFRaw['data'][:, dataNFColUseInd]


# dataframe, select by company code and mark
dataNFBalanceTolDF = pd.DataFrame(dataNFBalanceTolArr, columns=dataNFColUseLis)    # 789264
dataNFBalanceUseDF = dataNFBalanceTolDF[dataNFBalanceTolDF[u'CompanyCode'].isin(dataComCodeArr)]  #544258 
dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceUseDF[u'Mark'].isin([1, 2])]      #287129

# dropna nan and zero values
dataNFBalanceNanInd = ((dataNFBalanceUseDF[u'FixedAssets'].notnull()) & (dataNFBalanceUseDF[u'FixedAssets'] != 0)\
 & (dataNFBalanceUseDF[u'TotalCurrentAssets'].notnull()) & (dataNFBalanceUseDF[u'TotalCurrentAssets'] != 0)\
 & (dataNFBalanceUseDF[u'TotalCurrentLiability'].notnull()) & (dataNFBalanceUseDF[u'TotalCurrentLiability'] != 0)\
 & (dataNFBalanceUseDF[u'TotalAssets'].notnull()) & (dataNFBalanceUseDF[u'TotalAssets'] != 0)  )
 
dataNFBalanceUseDF = dataNFBalanceUseDF[dataNFBalanceNanInd]    #285190


# load financial balance statement_new data
pathF = '/data/liushuanglong/MyFiles/Data/JYDB2/LC_FBalanceSheetNew/LC_FBalanceSheetNew_mat.mat'
dataFRaw = sio.loadmat(pathF)  
dataFColTol = [dataFRaw['col'][0][i][0] for i in range(dataFRaw['col'].shape[1])]
dataFColUseLis = [u'CompanyCode', u'InfoPublDate', u'EndDate', u'Mark', 'FixedAssets', u'TotalAssets']
dataFColUseInd = [dataFColTol.index(i) for i in dataFColUseLis]
dataFBalanceTolArr = dataFRaw['data'][:, dataFColUseInd]


# dataframe, select by company code and mark
dataFBalanceTolDF = pd.DataFrame(dataFBalanceTolArr, columns=dataFColUseLis)    # 23090
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


# create a new df dict
dataTolBalanceUseDic = {}   
for number, code in enumerate(dataTolComCode):    
    dfBalanceCode = dataTolBalanceDic[code]
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
                dfBalanceOneCodeLYTemp = dfBalanceCode.loc[pubDateUseArr]
                dfBalanceOneCodeLYTemp = dfBalanceOneCodeLYTemp[dfBalanceOneCodeLYTemp[u'EndDate'] == lastYearDate].iloc[-1, 2:]
        #            dfBalanceOneCodeLYTemp = dfBalanceOneCodeLYTemp[:-1] / dfBalanceOneCodeLYTemp[-1]   # calculte ratio
                # last two yearend data
                dfBalanceOneCodeLLYTemp = dfBalanceCode.loc[:pubDateUseArr[-1]]
                dfBalanceOneCodeLLYTemp = dfBalanceOneCodeLLYTemp[dfBalanceOneCodeLLYTemp[u'EndDate'] == llastYearDate].iloc[-1, 2:]
        #            dfBalanceOneCodeLLYTemp = dfBalanceOneCodeLLYTemp[:-1] / dfBalanceOneCodeLLYTemp[-1]  #  calculte ratio
                
                # change
                dfBalanceOneCodeTemp = dfBalanceOneCodeLYTemp - dfBalanceOneCodeLLYTemp   # drop 'assets item'
                dfOneCodeUse.loc[year] = (dfBalanceOneCodeTemp.iloc[0] + dfBalanceOneCodeTemp.iloc[1] - dfBalanceOneCodeTemp.iloc[2]) / \
                                      dfBalanceOneCodeLYTemp.iloc[-1]  
                
            
    dataTolBalanceUseDic[code] = dfOneCodeUse

#return dataTolBalanceUseDic

#len(dataTolBalanceUseDic)
#%%

#==============================================================================
# 3 save IA values data, will be calculated later 
#==============================================================================

# create a dic contain all effective date
comCodeUseLis = dataTolBalanceUseDic.keys()
dataBalanceUseTolTimeDic = {}
for code in comCodeUseLis:
    dataOneCodeTolDF = dataTolBalanceUseDic[code].sort_index()
    dataOneCodeTSRaw = dataOneCodeTolDF.index.tolist()
    dataOneCodeTSTol = sorted(set(dataTSArr) | set(dataOneCodeTSRaw))
    dataOneCodeUseDF = dataOneCodeTolDF.reindex(dataOneCodeTSTol, method='ffill').loc[dataTSArr]
    dataBalanceUseTolTimeDic[code] = dataOneCodeUseDF
    
    
# save netprofit as 3D array   , total codes
dataTolNetProfitArr = np.zeros((3, len(dataTSArr), len(dataComCodeArr)))           # use not financial codes
itemNames = [u'Change_On_Investments_To_Assets', u'EndDate', u'Mark']

dataNetProfitValueDF = pd.DataFrame([], index=dataTSArr, columns=dataComCodeArr)
dataNetProfitEndDateDF = pd.DataFrame([], index=dataTSArr, columns=dataComCodeArr)
dataNetProfitMarkDF = pd.DataFrame([], index=dataTSArr, columns=dataComCodeArr)
for code in comCodeUseLis:
    dataNetProfitValueDF[code] = dataBalanceUseTolTimeDic[code][itemNames[0]]
    dataNetProfitEndDateDF[code] = dataBalanceUseTolTimeDic[code][itemNames[1]]
    dataNetProfitMarkDF[code] = dataBalanceUseTolTimeDic[code][itemNames[2]]
#
## save as pkl
#dicNetProfitPkl = {u'NetProfit': dataNetProfitValueDF, u'EndDate': dataNetProfitEndDateDF, u'Mark': dataNetProfitMarkDF}
#cp.dump(dicNetProfitPkl, open("/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalData/LC_IncomeStatementNew_Total_NetProfit_YearDuration_3items.pkl", "w")) 


    
# save netprofit in 3D array       
dataTolNetProfitArr[0] = dataNetProfitValueDF.values      # net profit
dataTolNetProfitArr[1] = dataNetProfitEndDateDF.values    # end date
dataTolNetProfitArr[2] = dataNetProfitMarkDF.values      # mark


itemNamesArr = np.zeros((1, len(itemNames)), dtype=object)
for i, j in enumerate(itemNames):
    itemNamesArr[0][i] = np.array([j])

dataDic = {'axis1_itemNames': itemNamesArr, \
           'axis2_indexTime': dataTSArr.reshape(len(dataTSArr), 1), \
           'axis3_colCompanyCode': dataComCodeArr, \
           'LC_IncomeStatementNew_Total_NetProfit_YearDuration': dataTolNetProfitArr}
           
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalData/LC_IncomeStatementNew_Total_NetProfit_YearDuration_arr.mat', dataDic)










#%%

#==============================================================================
# 4. seperate three groups by IA 
#==============================================================================
#def IAThreeGroupsDicGet(Flag=0):


dataIAYearUseDF = pd.DataFrame()
comCodeUseLis = dataTolBalanceUseDic.keys()
innerCodeUseArr = np.zeros_like(comCodeUseLis)

# use innercode as columns names
for i, j in enumerate(comCodeUseLis):
    innerCodeUseArr[i] = dataInnerCodeArr[dataComCodeArr == j][0]


# concat IA data by year
dataIAYearUseDF = pd.DataFrame()
for i, code in enumerate(comCodeUseLis):
    dataTolBalanceUseDic[code].columns = innerCodeUseArr[[i]]
    dataIAYearUseDF = pd.concat([dataIAYearUseDF, dataTolBalanceUseDic[code]], axis = 1)


thrNum = 100

#if Flag == 1:
#    dataIAYearUseDF = dataIAYearUseDF[dataHS300InnerCodeArr]
#    dataIAYearUseDF = dataIAYearUseDF.dropna(how='all')
#    thrNum = 20
dataYearUseLis = dataIAYearUseDF.index.tolist()       # 27

groupLowIADic = {}
groupMedIADic = {}
groupHigIADic = {}
groupAllIADic = {}

#dfpercent2 = dataIAYearDF.quantile([0.3, 0.75], axis=1).T   #  why? !!!
dfpercent = pd.DataFrame(index=dataYearUseLis, columns=[0.3, 0.7])
for year in dataYearUseLis:
    dfpercent.loc[year] = dataIAYearUseDF.loc[year].quantile([0.3, 0.7])
    
for year in dataYearUseLis:
    dataIAYearUseTemp = dataIAYearUseDF.loc[year]
    if len(dataIAYearUseTemp.dropna()) >= thrNum:  # keep stocks groups when counts >=100
        groupAllIADic[year] = dataIAYearUseTemp.dropna().index.tolist()
        per = dfpercent.loc[year]
        groupLowIADic[year] = dataIAYearUseTemp[dataIAYearUseTemp<=per[0.3]].index.tolist()
        groupMedIADic[year] = dataIAYearUseTemp[(dataIAYearUseTemp>=per[0.3]) & (dataIAYearUseTemp<per[0.7])].index.tolist()
        groupHigIADic[year] = dataIAYearUseTemp[dataIAYearUseTemp>=per[0.7]].index.tolist()

threeGroupsDic = {'low': groupLowIADic, 'median': groupMedIADic, 'high':groupHigIADic, 'all':groupAllIADic}
#return threeGroupsDic

#IAThreeGroupsDicGetTest = IAThreeGroupsDicGet()
#IA_HS300ThreeGroupsDicGetTest = IAThreeGroupsDicGet(Flag=1)
#%%

#==============================================================================
# 5. calculate the IA value-weighted stock return
#==============================================================================

#def IAReturnGet(Flag=0):    
    
## 5.1 load 3 stock groups by IA, stoct daily returns, stock daily volumne, stock AFloats
 
    # load 3 stock groups by IA
#    threeGroupsDic = IAThreeGroupsDic()
#threeGroupsDic  = IA_HS300ThreeGroupsDicGetTest      # test
yearGroupLis = sorted(threeGroupsDic['low'].keys())

## load stoct daily returns
pathReturn = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_mat.mat'
dataReturnRaw = sio.loadmat(pathReturn)
dataReturnArr = dataReturnRaw['DailyQuote_LogReturn']

## load stock daily volumne
pathVol = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_TurnoverVolume_mat.mat'
dataVolRaw = sio.loadmat(pathVol)
dataVolArr = dataVolRaw['DailyQuote_TurnoverVolume']  # columns: inner code

## load stock AFloats
pathAF = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_AFloats_mat.mat'
dataAFloatsRaw = sio.loadmat(pathAF)
dataAFloats3DArr = dataAFloatsRaw['LC_AFloats']
dataAFloatsArr = dataAFloats3DArr[0]

## 5.2 calculate grouped IA daily return
# keep effective data
dataInnerCodeUseArr = dataInnerCodeArr

#if Flag == 1:  # HS300 stock
#    dataInnerCodeUseArr = dataHS300InnerCodeArr
#    dataReturnArr = dataReturnArr[:, dataHS300CodeIndArr]    
#    dataVolArr = dataVolArr[:, dataHS300CodeIndArr]    
#    dataAFloatsArr = dataAFloatsArr[:, dataHS300CodeIndArr]    
   
dataVolUseArr = np.zeros((len(dataTSArr), len(dataInnerCodeUseArr)))
dataReturnUseArr = np.zeros((len(dataTSArr), len(dataInnerCodeUseArr)))
dataAFloatsUseArr = np.zeros((len(dataTSArr), len(dataInnerCodeUseArr)))
dataReturnUseArr[:] = np.nan
dataVolUseArr[:] = np.nan
dataAFloatsUseArr[:] = np.nan

#bool1Arr = np.where((~np.isnan(dataVolArr[1])) & (dataVolArr[1]!=0))
for i in range(len(dataTSArr)):
    posUseArr = np.where((~np.isnan(dataVolArr[i])) & (dataVolArr[i]!=0))
    dataVolUseArr[i][posUseArr] = dataVolArr[i][posUseArr]
    dataReturnUseArr[i][posUseArr] = dataReturnArr[i][posUseArr]
    dataAFloatsUseArr[i][posUseArr] = dataAFloatsArr[i][posUseArr]

dataReturnDF = pd.DataFrame(dataReturnUseArr, index=dataTSArr, columns=dataInnerCodeUseArr)
dataAFloatsDF = pd.DataFrame(dataAFloatsUseArr, index=dataTSArr, columns=dataInnerCodeUseArr)

# 3 groups return
dataIAReturnDF = pd.DataFrame([], index=dataTSArr, columns=['low', 'median', 'high', 'HML'])

counts = 0
for year in yearGroupLis:
    groupTemLis = [threeGroupsDic[i][year] for i in ['low', 'median', 'high']]
    for date in dataTSArr[(dataTSArr>(year*10000+430)) & (dataTSArr<((year+1)*10000+501))]:
        for i, group in enumerate(groupTemLis):
            dataOGTemDF = pd.DataFrame(index=group, columns=['return', 'aFloats', 'weight', 'wReturn'])
            dataOGTemDF['return'] = dataReturnDF.loc[date][group]
            dataOGTemDF['aFloats'] = dataAFloatsDF.loc[date][group]
            dataOGTemDF['weight'] = dataOGTemDF['aFloats'] / dataOGTemDF['aFloats'].sum()
            dataOGTemDF['wReturn'] = dataOGTemDF['return'] * dataOGTemDF['weight']				
            dataIAReturnDF.loc[date].iloc[i] = dataOGTemDF['wReturn'].sum()
        counts = counts + 1    
        if counts%50 == 0:
            print date, 

dataIAReturnDF['HML'] = dataIAReturnDF['high'] - dataIAReturnDF['low']

#return dataIAReturnDF
#    dataIAReturnDF.describe()
#    dataIAIAReturnDF.corr()

#IAReturnGetTest = IAReturnGet()
#IA_HS300ReturnGetTest = IAReturnGet(Flag=1)
#%%

#==============================================================================
# 6. save IA return data
#==============================================================================

# save 3 groups IA return
dataIAReturn = dataIAReturnDF
colArr = np.zeros((1, len(dataIAReturn.columns)), dtype=object)
for i, j in enumerate(dataIAReturn.columns):
    colArr[0][i] = np.array([j])

dataDic = {'colItems': colArr, \
           'indexTime': dataTSArr.reshape(len(dataTSArr), 1), \
           'LC_YearDuration_IA_3Groups_Return': dataIAReturn.values.astype(np.float64)}

#sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/InvestmentsToAssets/LC_YearDuration_IA_3Groups_Return_arr.mat', dataDic)


#%%
#==============================================================================
# 7. IA exposure
#==============================================================================
import statsmodels.api as sm

## 7.1 load bond log return, stock log return 
# bond log return
pathBond = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/Wind_Daily_10YearBond_LogReturn_mat.mat'
dataBondRaw = sio.loadmat(pathBond)
dataBondArr = dataBondRaw['daily_10YearBond_LogReturn']

#
## ROE return 
#pathROEReturn = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_YearDuration_ROE_3Groups_Return_2_mat.mat'
#dataROEReturnRaw = sio.loadmat(pathROEReturn)
#dataROEReturnRaw.keys()
#dataROEReturnArr = dataROEReturnRaw['LC_YearDuration_ROE_3Groups_Return_2_mat']
#dataROEReturnArr.shape


# load stock log return
pathStoReturn = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_mat.mat'
dataStoReturnRaw = sio.loadmat(pathStoReturn) 
dataStoReturnArr = dataStoReturnRaw['DailyQuote_LogReturn']
dataStoReturnArr.shape

## 7.2 calculate stock free return, IA free return
effTSNumber = len(set(dataTSArr) & set(dataBondArr[:, 0]))
dataTSEffArr = dataTSArr[-effTSNumber:]  # 3764

#dataBondDF = pd.DataFrame(dataBondArr, columns=['date', 'logReturn'])
#dataBondDF.set_index('date', inplace=True)
#dataBondUseDF = dataBondDF.reindex(dataTSArr)
#dataBondUseDF.shape

dataBondUseArr = dataBondArr[:effTSNumber, [1]]

# stock free return
dataStoFreeReturnUseArr = dataStoReturnArr[-effTSNumber:, :]   
dataStoFreeReturnUseArr = dataStoFreeReturnUseArr - dataBondUseArr    
#dataStoFreeReturnUseArr.shape
# IA 
dataIAReturnArr = dataIAReturn.values.astype(np.float64)
dataIAReturnUseArr = dataIAReturnArr[-effTSNumber:, :]      
#dataIAReturnUseArr.shape

#==============================================================================
# calculate every stock IA exposure
#==============================================================================
import time
#def IAExposureGet(day=100):
day = 250
percent = 0.2
dataIAReturnUseArr.dtype = float
X = sm.add_constant(dataIAReturnUseArr[:, 3])
#X.shape    


dataIABetaArr = np.ones_like(dataStoFreeReturnUseArr)
dataIABetaArr[:] = np.nan
dataIAAlpArr = np.ones_like(dataStoFreeReturnUseArr)
dataIAAlpArr[:] = np.nan

print time.strftime("%H:%M:%S", time.localtime())
for d in range(day-1, effTSNumber):
    arrTemp = dataStoFreeReturnUseArr[(d-day+1):(d+1)]
    Xtemp = X[(d-day+1):(d+1)]
    for s in range(len(dataInnerCodeArr)):
        useIndArr = np.where(~np.isnan(arrTemp[:, s]))[0]
        if len(useIndArr) > (day * percent):
            result = sm.OLS(arrTemp[useIndArr, s], Xtemp[useIndArr]).fit()
            dataIAAlpArr[d, s] = result.params[0]
            dataIABetaArr[d, s] = result.params[1]
    if d%20 == 0:
        print d, time.strftime("%H:%M:%S", time.localtime())
dataExposure = {'alpha': dataIAAlpArr, 'beta': dataIABetaArr }        

dataDic = {'alpha': dataIAAlpArr, 'beta': dataIABetaArr, \
            'timeIndex': dataTSEffArr.reshape((len(dataTSEffArr), 1)), 'innerCode': dataInnerCodeArr.reshape((1, len(dataInnerCodeArr)))}
            
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/InvestmentsToAssets/IAExposure_arr.mat', dataDic)        
import cPickle as cp
cp.dump(dataExposure, open('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/InvestmentsToAssets/IAExposure.pkl' ,'w'))
# save data

#
#colArr = np.zeros((1, 1)), dtype=object)
#for i, j in enumerate(['IABeta']):
#    colArr[0][i] = np.array([j])

#dataDic = {'col': colArr, 'IABeta':dataIABetaArr}
#
#dic = {'IABeta':  dataIABetaArr, 'IAAlpha': dataIAAlpArr}
#cp.dump(dic, open('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/IAExposure100day.pkl', 'w'))

#%%











#
#import matplotlib.pyplot as plt
#
#fig = plt.figure(figsize=(20, 8))
#ax1 = fig.add_subplot(411)
#ax2 = fig.add_subplot(412)
#ax3 = fig.add_subplot(413)
#ax4 = fig.add_subplot(414)
#ax1.plot(range(len(dataIAReturn.index)), dataIAReturn['HML'].values, label='HML')
#ax2.plot(range(len(dataIAReturn.index)), dataIAReturn['low'].values, label='low')
#ax3.plot(range(len(dataIAReturn.index)), dataIAReturn['median'].values, label='median')
#ax4.plot(range(len(dataIAReturn.index)), dataIAReturn['high'].values ,label='high')
#
#tickUseInd = np.arange(600, len(dataTSArr), 600)
#ax1.set_xticks(tickUseInd)
#ax1.set_xticklabels(dataTSArr[tickUseInd], rotation=30)
##ax1.set_xlabel('Stages')
#ax2.set_xticks(tickUseInd)
#ax2.set_xticklabels(dataTSArr[tickUseInd], rotation=30)
#ax3.set_xticks(tickUseInd)
#ax3.set_xticklabels(dataTSArr[tickUseInd], rotation=30)
#ax4.set_xticks(tickUseInd)
#ax4.set_xticklabels(dataTSArr[tickUseInd], rotation=30)
#ax1.legend(loc='best')
#ax2.legend(loc='best')
#ax3.legend(loc='best')
#ax4.legend(loc='best')
#plt.savefig('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/HS300_IAReturn.png', dpi=600)
    
    
        
    
    
    
    
    
    
    
    
    



