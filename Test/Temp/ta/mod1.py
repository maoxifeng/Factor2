# -*- coding: utf-8 -*-

class Person(object):
    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name
    def greet(self):
        print 'Hello, world! I am %s.'%self.name
    def gree(self):
        print 'Hello, world! I am %s.'% self.getName()


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

