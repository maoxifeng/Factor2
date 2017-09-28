# -*- coding: utf-8 -*-
#Student.books.extend(["python", "javascript"])  
#print "Student book list: %s" %Student.books    
## class can add class attribute after class defination
#Student.hobbies = ["reading", "jogging", "swimming"]
#print "Student hobby list: %s" %Student.hobbies    
#print dir(Student)
"""
Created on Thu Aug 24 21:40:46 2017

@author: xun
"""




class Person(object):
    def __init__(self):
        self._att ='att'
        self.nn = 'name'
        self.aa = self.getName()
        self.bb = self.getNum()
        self.greet()
        self._fun1()

    def _fun1(self, a=1):
        print a
        self._ff = a

    def getNum(self):
        return 10000
    def getName(self):
        print 'getName function: '
        return self.nn + '_getname'
    def greet(self):
        print 'Hello, world! I am %s.'%self.aa
    def setName(self, nnn='name'):
        self.name = nnn
    def gree(self):
        print 'Hello, world! I am %s.'% self.aa   



class Person(object):
    def __init__(self):
        self._att ='att'
        self.fun_one()
        self.cons_two = self.fun_two()

    def fun_two(self):
        print 'fun_two'
        return [self.cons_one] + [100]

    def fun_one(self, a=1):
        print a
        self.cons_one = a


		
class Student1(object):
    count = 0
    books = []
    def __init__(self, name, age):
        self.name = name
        self.age = age
    pass

class Student2():
    count = 0
    books = []
    def __init__(self, name, age):
        self.name = name
        self.age = age
    pass

class Student3:
    count = 0
    books = []
    def __init__(self, name, age):
        self.name = name
        self.age = age
    pass

#%%
#Student.books.extend(["python", "javascript"])  
#print "Student book list: %s" %Student.books    
## class can add class attribute after class defination
#Student.hobbies = ["reading", "jogging", "swimming"]
#print "Student hobby list: %s" %Student.hobbies    
#print dir(Student)






