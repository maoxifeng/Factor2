# -*- coding: utf-8 -*-

__author__ = 'liusl'
import logging

#logging.debug('This is debug message')
#logging.info('This is info message')
#logging.warning('This is warning message')

  
logging.basicConfig(level=logging.WARNING,  
                    filename = 'log.txt',
                    filemode = 'w',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  
# use logging  
logging.info('this is a loggging info message')  
logging.debug('this is a loggging debug message')  
logging.warning('this is loggging a warning message')  
logging.error('this is an loggging error message')  
logging.critical('this is a loggging critical message')



#logging.basicConfig(level=logging.DEBUG,
#                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                datefmt='%a, %d %b %Y %H:%M:%S',
#                filename='myapp.log',
#                filemode='w')
#    
#logging.debug('This is debug message')
#logging.info('This is info message')
#logging.warning('This is warning message')
    
    
    
    
    
    
