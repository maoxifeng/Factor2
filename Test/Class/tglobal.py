# -*- coding: utf-8 -*-


go = 50

def fun1():
    global go
    print 'before:', go
    go = go + 10 
    print 'after:', go
fun1()
print 'go', go


a = 0
def fun2():
    print a
    return 

#class A():
#    count = 2
#    def __init__(self): # 这就是一个实例方法
#        A.count += 1
#
#class B():
#    count = 2
#    def __init__(self): # 这就是一个实例方法
#        print self.count
##        self.count = B.count
##        self.count += 1 
#        B.count = self.count + 1


#'''class function 1: self'''
#class Student(object):
#    '''
#    this is a Student class
#    '''
#    count = 0
#    books = []
#    def __init__(self, name, age):
#        self.name = name
#        self.age = age
#        print 'I am init.'
##        print self.printInstanceInfo() 
#
#    def printInstanceInfo(self):
#        print "%s is %d years old" %(self.name, self.age)
##    pass


#'class function 2: clc'
#class Student(object):
#    '''
#    this is a Student class
#    '''
#    count = 0
#    books = []
#    def __init__(se, name, age):
#        se.name = name
#        se.age = age
# 
#    @classmethod
#    def printClassInfo(cs):
#        print cs.__name__
#        print cs.count
#        print dir(cs)
#    pass
# 
#Student.printClassInfo()    
#wilber = Student("Wilber", 28)
#wilber.printClassInfo()


#'class function 3: static method'
#class Student(object):
#    '''
#    this is a Student class
#    '''
#    count = 0
#    books = []
#    def __init__(self, name, age):
#        self.name = name
#        self.age = age
# 
#    @staticmethod
#    def printClassAttr():
#        print Student.count
##        print self.count
#        print Student.books
##        print self.books
#    pass
# 
#Student.printClassAttr()    
#wilber = Student("Wilber", 28)
#wilber.printClassAttr()



#class long(object):
#    'Yes, I am S. L. Liu'
#    def __init__(self, a, b):
#        self.a = a
#        self.b = b
#        self.cc = self.c()
#        self.dd = long.d()
#    def c(self):
#        print 'I am c.'
#
#    @classmethod  
#    def d(sel):
#        print 'I am d'
        
#class inner(object):
#    '''I am inner.''' 
#    cons1 = 111
#    _cons2 = 222
#
#    def __init__(self, aa):
#        self._aa = aa
#        self.aaa = aa+10
#
#    def __fun(self, a):
#        print 'I am _fun.'
#        print a
#
#    def func(self, b):
#        print 'I am func.' 
#        print b
#    
#
#
#def _fun(a):
#    print 'I am _fun.'
#    print a
#
#def func(b):
#    print 'I am func.' 
#    print b



