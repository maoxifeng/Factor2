# -*- coding: utf-8 -*-

#a = []
#def func():
#    for i in range(5):
#        a.append(i)
#        print a


#a = 333  
#def bind_a_variable():
#    # global a
#    # a = []
#    a = 1 
#bind_a_variable()

#def make_closure(a):
#    def closure():
#        print 'I know the secret: %d' %a
#    return closure 
#
#closure = make_closure(5)
#closu = make_closure(10)

e = 10
def make_closure(a):
    b = 3
    def closure(xx, yy, dd=30):
        c = 30
        print 'I know the secret: %d' %a
        print 'b: %s' %b
        print 'c: %s' %c
        print 'e: %s' %e
        return xx + yy + b
    return closure 

closure = make_closure(5)
closu = make_closure(10)


#def make_watcher():
#    have_seen = {} 
#    
#    def has_been_seen(x):
#        if x in have_seen:
#            return True 
#        else:
#            have_seen[x] = True 
#            return False 
#
#    return has_been_seen 
#
#watcher = make_watcher()
#vals = [12, 43, 434, 545, 90]
#print [watcher(x) for x in vals]


#def make_counter():
#    count = [0]
#    def counter():
#        count[0] += 1
#        return count[0]
#    return counter 
#cou = make_counter()

#def say_hello_then_call_f(f, *args, **kw):
#    print 'args is ', args 
#    print 'kw is ', kw
#    print 'Hello! Now I am going to call %s' %f
#    return f(*args, **kw)
#
#def g(x, y, z=1):
#    return (x+y)/z 

# generater
#def squares(n=10):
#    print 'Generating squares from 1 to %d' %(n**2)
#    for i in xrange(1, n+1):
#        yield i**2
#
#
#def squares2(n=18):
#    print 'Generating squares from 1 to %d' %(n**2)
#    return n**2



















