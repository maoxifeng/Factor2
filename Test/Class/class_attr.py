# -*- coding: utf-8 -*-


#class AAA():  
#    aaa = 10  
# 
## 情形1   
#obj1 = AAA()  
#obj2 = AAA()   
#print obj1.aaa, obj2.aaa, AAA.aaa   
# 
## 情形2  
#obj1.aaa += 2  
#print obj1.aaa, obj2.aaa, AAA.aaa   
# 
## 情形3  
#AAA.aaa += 3  
#print obj1.aaa, obj2.aaa, AAA.aaa  


class Foo(object):
    __slots__ = ('bar', )
    bar = 'spam'

class Foo2(object):
    bar2 = 'spam2'




