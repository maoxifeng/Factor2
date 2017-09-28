# -*- coding: utf-8 -*-


import os, time
from multiprocessing import Pool

def foo(x):

    print time.strftime("%H:%M:%S", time.localtime()), '\t',
    print 'Run task %s (pid:%s)...' % (x, os.getpid())
    time.sleep(2)
    print time.strftime("%H:%M:%S", time.localtime()), '\t',
    print 'Task %s result is: %s' % (x, x * x)
    
    return x**2

if __name__ == '__main__':
    print '\n', time.strftime("%H:%M:%S", time.localtime()), '\t',
    print 'Parent process %s.' % os.getpid()
    p = Pool(4)         # 设置进程数
    res = []
    for i in range(10):
        res.append(p.apply_async(foo, args=(i,)))    # 设置每个进程要执行的函数和参数
    print '\n', time.strftime("%H:%M:%S", time.localtime()), '\t',
    print 'Waiting for all subprocesses done...', '\n'
    p.close()
    p.join()
    print '\n', time.strftime("%H:%M:%S", time.localtime()), '\t',
    print 'All subprocesses done.', '\n'
    res = map(lambda ret: ret.get(), res)

