# -*- coding: utf-8 -*-

#def print_deco(fun):
#    def wrapper(*args, **kw):
#        print 'Execute function:', fun.__name__
#        print 'Positional arguments:', args 
#        print 'Keyword arguments:', kw 
#        result = fun(*args, **kw)
#        print 'Result:', result 
#        return result 
#    return wrapper 
#
#@ print_deco 
#def add_ints(a, b):
#    return a+b

#co_add = print_deco(add_ints) 

#from functools import wraps
#
#def print_deco(fun):
#    @ wraps(fun)
#    def wrapper(*args, **kw):
#        print 'Execute function:', fun.__name__
#        print 'Positional arguments:', args 
#        print 'Keyword arguments:', kw 
#        result = fun(*args, **kw)
#        print 'Result:', result 
#        return result 
#    return wrapper 
#
#@ print_deco 
#def add_ints(a, b):
#    ''' i am add_ints '''
#    return a+b

import logging
def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn" :
                logging.warn("%s is running" % func.__name__)
            return func(*args)
        return wrapper
    return decorator

@use_logging(level="arn") 
def foo(name='foo'):     
	print("i am %s" % name)



