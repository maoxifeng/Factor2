# -*- coding: utf-8 -*-

# funtion of class

# function 1
class Student( object):
    '''
    this is a Student class
    '''
    count = 0
    books = []
    def __init__( self, name, age):
        self.name = name                     
        self.age = age
        self.__address = 'Shanghai' 
    def printInstanceInfo( self):
        print "%s is %d years old" %( self.name, self.age) 
        pass 

wilber = Student( "Wilber", 28)
wilber.printInstanceInfo( )



# function 2
class Student( object):
    '''
    this is a Student class
    '''
    count = 0
    books = []
    def __init__( self, name, age):
        self.name = name 
        self.age = age 
    @classmethod 
    def printClassInfo( cls):
        print cls.__name__ 
        print dir( cls)
        pass

Student.printClassInfo( ) 
wilber = Student( "Wilber", 28)
wilber.printClassInfo( )


# function 3
class Student( object):
    '''
    this is a Student class 
    '''
    count = 0
    books = []
    def __init__( self, name, age):
        self.name = name 
        self.age = age 

    @staticmethod 
    def printClassAttr( ):
        print Student.count 
        print Student.books 
        pass
        
Student.printClassAttr( )    
wilber = Student( "Wilber", 28)
wilber.printClassAttr( )







