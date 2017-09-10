# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 14:31:44 2017

@author: liusl
"""

import numpy as np
import scipy.io as sio
import pandas as pd
import Common.TimeCodeGet as tc
import os
import Common.SmaFun as cs

import QT_DailyQuote.DailyQuoteGet as dq


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
#%% Close             
                           
_ = dq.DailyQuoteGet(u'ClosePrice')

#%% Volume

_ = dq.DailyQuoteGet(u'TurnoverVolume')

#%% Turnover value

_ = dq.DailyQuoteGet(u'TurnoverValue')

#%% Adjusting price factors

_ = dq.RAFactorGet()

#%% Adjusted Close

_ = dq.AdjCloseGet()

#%% 


#%% stock log return

dq.StoReturnGet()












