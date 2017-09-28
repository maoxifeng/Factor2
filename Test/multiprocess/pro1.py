# -*- coding: utf-8 -*-

import os
from multiprocessing import Process


# 子进程要执行的代码
def child_proc(name):
    print 'Run child process %s (%s)...' % (name, os.getpid())

if __name__ == '__main__':
    print 'Parent process %s.' % os.getpid()
    p = Process(target=child_proc, args=('test',))
    print 'Process will start.'
    p.start()
    p.join()
    print 'Process end.'

