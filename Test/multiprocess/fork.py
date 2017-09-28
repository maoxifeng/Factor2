# -*- coding: utf-8 -*-


import os

#pid = os.fork()
#
#if pid < 0:
#    print 'Fail to create process'
#elif pid == 0:
#    print 'I am child process (%s) and my parent is (%s).' % (os.getpid(), os.getppid())
#else:
#    print 'I (%s) just created a child process (%s).' % (os.getpid(), pid)


# claim once, return twice: first(ID of childprocess), second(ID=0, refers to the childprocess)
pid = os.fork()
if pid < 0:
    print 'Fail to create process'
# os.getpid() :get the ID of current process
# os.getppid() :get the ID of parent process
elif pid == 0:
    print 'I am child process (%s) and my parent is (%s).' % (os.getpid(), os.getppid())
else:
    print 'I (%s) just created a child process (%s).' % (os.getpid(), pid)
    print 'I (%s) just created a child process (%s).' % (os.getpid(), os.getppid())

