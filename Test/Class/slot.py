# -*- coding: utf-8 -*-


#class Student(object):
#    __slots__ = ("name", "age")
#    def __init__(self, name, age):
#        self.name = name
#        self.age = age
# 
#s = Student("Wilber", 28)        
#print "%s is %d years old" %(s.name, s.age)
#s.score = 96


#class Person(object):
#    __slots__ = ("name", "age")
#    pass
#
#class Student(Person):
#    pass
#
#s = Student()
#s.name, s.age = "Wilber", 28
#s.score = 100
#
#print "%s is %d years old, score is %d" %(s.name, s.age, s.score)


class Person(object):
    __slots__ = ("name", "age")
    pass

class Student(Person):
    __slots__ = ("score", )
    pass

s = Student()
s.name, s.age = "Wilber", 28
s.score = 100

print "%s is %d years old, score is %d" %(s.name, s.age, s.score)
print s.__slots__

s.city = "Shanghai"




