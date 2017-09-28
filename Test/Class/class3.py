# -*- coding: utf-8 -*-

#class A(object):
#    def __init__(self,*args, **kwargs):
#        print "init %s" %self.__class__
#    def __new__(cls,*args, **kwargs):
#        print "new %s" %cls
#        return object.__new__(cls, *args, **kwargs)
# 
#a = A()
# 
#class B(object):
#    pass 
 
 
#class Foo(object):
#    def __new__(cls, *args, **kwargs):
#        obj = object.__new__(cls, *args, **kwargs)   
#        # 这里的object.__new__(cls, *args, **kwargs)   等价于
#        # super(Foo, cls).__new__(cls, *args, **kwargs)   
#        # object.__new__(Foo, *args, **kwargs)
#        # Bar.__new__(cls, *args, **kwargs)
#        # Student.__new__(cls, *args, **kwargs)，即使Student跟Foo没有关系，也是允许的，因为Student是从object派生的新式类
#
#        # 在任何新式类，不能调用自身的“__new__”来创建实例，因为这会造成死循环
#        # 所以要避免return Foo.__new__(cls, *args, **kwargs)或return cls.__new__(cls, *args, **kwargs)
#        print "Call __new__ for %s" %obj.__class__
#        return obj    
#
#class Bar(Foo):
#    def __new__(cls, *args, **kwargs):
#        obj = object.__new__(cls, *args, **kwargs)   
#        print "Call __new__ for %s" %obj.__class__
#        return obj   
#
#class Student(object):
#    # Student没有“__new__”方法，那么会自动调用其父类的“__new__”方法来创建实例，即会自动调用 object.__new__(cls)
#    pass
#
#class Car(object):
#    def __new__(cls, *args, **kwargs):
#        # 可以选择用Bar来创建实例
#        obj = object.__new__(Bar, *args, **kwargs)   
#        print "Call __new__ for %s" %obj.__class__
#        return obj
#
#foo = Foo()
#bar = Bar()
#car = Car()


#class A(object):
#    def __init__(self, *args, **kwargs):
#        print "Call __init__ from %s" %self.__class__
#        print 'class A'
# 
#    def __new__(cls, *args, **kwargs):
#        obj = object.__new__(cls, *args, **kwargs)
#        print "Call __new__ for %s" %obj.__class__
#        return obj   
# 
#class B(object):
#    def __init__(self, *args, **kwargs):
#        print "Call __init__ from %s" %self.__class__
#        print 'class B' 
#    def __new__(cls, *args, **kwargs):
#        obj = object.__new__(A, *args, **kwargs)
#        print "Call __new__ for %s" %obj.__class__
#        return obj      
# 
#class C(object):
#    def __init__(self, *args, **kwargs):
#        print "Call __init__ from %s" %self.__class__
#        print 'class C' 
#    def __new__(cls, *args, **kwargs):
#        obj = object.__new__(cls, *args, **kwargs)
#        print "Call __new__ for %s" %obj.__class__
#        return obj      
#b = B()
#print type(b)




class Round2Float(float):
    def __new__(cls, num):
        num = round(num, 2)
        #return super(Round2Float, cls).__new__(cls, num)
        return float.__new__(Round2Float, num)
 
f = Round2Float(4.14159)
print f




