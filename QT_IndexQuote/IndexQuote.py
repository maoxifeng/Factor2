# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 13:22:33 2017

@author: liusl
"""

import numpy as np
import scipy.io as sio
import pandas as pd
import Common.TimeCodeGet as tc
import Common.SmaFun as cs
import os
import Common.UpdateDataGet as cu
import QT_IndexQuote.IndexQuoteGet as iq


dataDSArr = tc.dateSerArrGet()[:, 0]
dataInnerCodeArr = tc.codeDFGet().iloc[:, 0].values.astype(float)

#%% HS300 Index Close

iq.IndexQuoteGet(mar='HS300', facName='ClosePrice', items=[u'PrevClosePrice', u'ClosePrice'])

#%% HS300 Index Return

iq.IndexLogReturnGet(mar='HS300')

#%% Wind 10 year Bond Return

iq.BondReturnGet()



