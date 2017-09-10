# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 18:29:08 2017

@author: liusl
"""


import scipy.io as sio
import numpy as np

import FundamentalData.FunCommon.FacAnaGet as facana

facNameFM_A='ROE_FM_A'
facNameFM_HS300='ROE_FM_HS300'

facValue='ROE_Value'

savePath = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/'
facExpPath_A = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/ROE_A_StoFree_FMExposure_250regDays_array.mat'
facExpPath_HS300 = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/ROE_HS300_StoFree_FMExposure_250RDs_array.mat'

facValuePath = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/ROE/ROE_FormatValues_3DArray_arr.mat'

#%%
ROE_FM_A_A_GroReturn = facana.DivGroRetGet(loadPath=facExpPath_A, facName=facNameFM_A, divGroNum=10, pool='A', saveBool=False)
_ = facana.DivGroExcRetGraphGet(loadArr=ROE_FM_A_A_GroReturn, loadPath=savePath, facName_Pool=facNameFM_A+'_A')

#%%
ROE_FM_A_HS300_GroReturn = facana.DivGroRetGet(loadPath=facExpPath_A, facName=facNameFM_A, divGroNum=10, pool='HS300', saveBool=False)
_ = facana.DivGroExcRetGraphGet(loadArr=ROE_FM_A_HS300_GroReturn, loadPath=savePath, facName_Pool=facNameFM_A+'_HS300')

#%%
ROE_FM_HS300_A_GroReturn = facana.DivGroRetGet(loadPath=facExpPath_HS300, facName=facNameFM_HS300, divGroNum=10, pool='A', saveBool=False)
_ = facana.DivGroExcRetGraphGet(loadArr=ROE_FM_HS300_A_GroReturn, loadPath=savePath, facName_Pool=facNameFM_HS300+'_A')

#%%
ROE_FM_HS300_HS300_GroReturn = facana.DivGroRetGet(loadPath=facExpPath_HS300, facName=facNameFM_HS300, divGroNum=10, pool='HS300', saveBool=False)
_ = facana.DivGroExcRetGraphGet(loadArr=ROE_FM_HS300_HS300_GroReturn, loadPath=savePath, facName_Pool=facNameFM_HS300+'_HS300')

#%%
ROE_Value_A_GroReturn = facana.DivGroRetGet(loadPath=facValuePath, facName=facValue, divGroNum=10, pool='A', saveBool=False)
_ = facana.DivGroExcRetGraphGet(loadArr=ROE_Value_A_GroReturn, loadPath=savePath, facName_Pool=facValue+'_A')

#%%
ROE_Value_HS300_GroReturn = facana.DivGroRetGet(loadPath=facValuePath, facName=facValue, divGroNum=10, pool='HS300', saveBool=False)
_ = facana.DivGroExcRetGraphGet(loadArr=ROE_Value_HS300_GroReturn, loadPath=savePath, facName_Pool=facValue+'_HS300')


