# -*- coding: utf-8 -*-

# subclass example

#class Parent(object):
#    '''
#    parent class
#    '''
#    numList = []
#    def numAdd(self, a, b):
#        return a+b
# 
#class Child(Parent):
#    pass
# 
#c = Child()    
## subclass will inherit attributes from parent class    
#Child.numList.extend(range(10))
#print Child.numList
#print "2 + 5 =", c.numAdd(2, 5)
# 
## built-in function issubclass() 
#print issubclass(Child, Parent)
#print issubclass(Child, object)
# 
## __bases__ can show all the parent classes
#print Child.__bases__
# 
## doc string will not be inherited
#print Parent.__doc__
#print Child.__doc__


#class Parent(object):
#    def __init__(self, data):
#        self.data = data
#        print "create an instance of:", self.__class__.__name__
#        print "create an instance of:", self.__class__
#        print dir(self.__class__)
#        print dir(self)
#       # print "create an instance of:", self.__name__ 
#        print "data attribute is:", self.data
# 
#class Child(Parent):
#    pass
# 
#c = Child("init Child") 
#print    
#c = Child()


#class Parent(object):
#    def __init__(self, data):
#        self.data = data
#        print "create an instance of:", self.__class__.__name__
#        print "data attribute is:", self.data
# 
#class Child(Parent):
#    def __init__(self):
#        print "call __init__ from Child class"
# 
#c = Child()    
#print c.data



#class Parent(object):
#    def __init__(self, data):
#        self.data = data
#        print "create an instance of:", self.__class__.__name__
#        print "data attribute is:", self.data
# 
#class Child(Parent):
#    def __init__(self):
#        print "call __init__ from Child class"
#        super(Child, self).__init__("data from Child")
# 
#c = Child()    
#print c.data


#class Parent(object):
#    fooValue = "Hi, Parent foo value"
#    def foo(self):
#        print "This is foo from Parent"
# 
#class Child(Parent):
#    fooValue = "Hi, Child foo value"
#    def foo(self):
#        print "This is foo from Child"
# 
#c = Child()    
#c.foo()
#print Child.fooValue


#class Parent(object):
#    fooValue = "Hi, Parent foo value"
#    def foo(self):
#        print "This is foo from Parent"
# 
#class Child(Parent):
#    fooValue = "Hi, Child foo value"
#    def foo(self):
#        print "This is foo from Child"
#        print Parent.fooValue
#        # use Parent class name and self as an argument
#        Parent.foo(self)
# 
#c = Child()    
#c.foo()



#class Parent(object):
#    fooValue = "Hi, Parent foo value"
#    def foo(self):
#        print "This is foo from Parent"
# 
#class Child(Parent):
#    fooValue = "Hi, Child foo value"
#    def foo(self):
#        print "This is foo from Child"
#        # use super to access Parent attribute
#        print super(Child, self).fooValue
#        super(Child, self).foo()
# 
#c = Child()    
#c.foo()





#class A(object):
#    def __init__(self):
#        print "   ->Enter A"
#        print "   <-Leave A" 
# 
#class B(A):
#    def __init__(self):
#        print "  -->Enter B"
#        A.__init__(self)
#        print "  <--Leave B"
# 
#class C(A):
#    def __init__(self):
#        print " --->Enter C"
#        A.__init__(self)
#        print " <---Leave C"
# 
#class D(B, C):
#    def __init__(self):
#        print "---->Enter D"
#        B.__init__(self)
#        C.__init__(self)
#        print "<----Leave D"
# 
#d = D()


class A(object):
    def __init__(self):
        print "   ->Enter A"
        print "   <-Leave A" 
 
class B(A):
    def __init__(self):
        print "  -->Enter B"
        super(B, self).__init__()
        print "  <--Leave B"
 
class C(A):
    def __init__(self):
        print " --->Enter C"
        super(C, self).__init__()
        print " <---Leave C"
 
class D(B, C):
    def __init__(self):
        print "---->Enter D"
        super(D, self).__init__()
        print "<----Leave D"
 
class E(B):
    def __init__(self):
        print "---->Enter E"
        super(E, self).__init__()
        print "<----Leave E"
 
class F(D):
    def __init__(self):
        print "---->Enter F"
        super(F, self).__init__()
        print "<----Leave F"
d = D()






