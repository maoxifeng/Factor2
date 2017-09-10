# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 17:18:27 2017

@author: liusl
"""
import statsmodels.api as sm
import numpy as np

x = np.ones(10)
x2 = range(10)
X = sm.add_constant(x)
X2 = sm.add_constant(x2)

y = range(10)
result = sm.OLS(y, X).fit()
result2 = sm.OLS(y, X2).fit()



a = result.params[0]
a2 = result2.params[0]
b2 = result2.params[1]
b = result.params[1]



def aa(a, b, *c):
    return c


aa(1, 2, 3)    



