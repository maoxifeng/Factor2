# -*- coding: utf-8 -*-

__author__ = 'liusl'
import logging



## print to console 
#logging.debug('This is debug message')
#logging.info('This is info message')
#logging.warning('This is warning message')

  
## print to file 1 
#logging.basicConfig(level=logging.WARNING,  
#                    filename = 'log.txt',
#                    filemode = 'w',
#                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  
## use logging  
#logging.info('this is a loggging info message')  
#logging.debug('this is a loggging debug message')  
#logging.warning('this is loggging a warning message')  
#logging.error('this is an loggging error message')  
#logging.critical('this is a loggging critical message')



## print to file 2 
#logging.basicConfig(level=logging.DEBUG,
#                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                datefmt='%a, %d %b %Y %H:%M:%S',
#                filename='myapp.log',
#                filemode='w')
#    
#logging.debug('This is debug message')
#logging.info('This is info message')
#logging.warning('This is warning message')
    
    
    
    
# print to file and console, waiting: 
#将日志同时输出到文件和屏幕
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')
                                                                               
