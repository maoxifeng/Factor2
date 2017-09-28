# -*- coding:utf-8 -*-

import os
import numpy as np
import pandas as pd

#class c1(object):
#    '''
#    line1
#    '''
#
#    '''line2'''
#    a = 1;
#    b = 2;    
#    def f1(self):
#        su = self.a + self.b
#        return su 
#    def __init__(self, folder='./', arg1=11, arg2=22):
#        self.cons = self.f1()
#        self.ar1 = arg1 
#        self.ar2 = arg2 
##        self.fol = folder + '/'
##        if os.path.exists(self.fol):
##            print 'already exist!'        
##        else: 
##            print 'no folder'
##            os.mkdir(self.fol)
##        pass 
#    def f2(self, arg3):
#        return arg3*100


class cc(object):
    def __init__(self, a, b):
        self.sa = a + 10
        self.pro = self.sa * self.sb  # can not use before claim self.sb 
        self.sb = b + 20

cc_ins = cc(1, 2)
    
