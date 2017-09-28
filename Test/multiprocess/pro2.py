# -*- coding: utf-8 -*-

import random
import os
from multiprocessing import Process

num = random.randint(0, 100)

def show_num():
    print("pid:{}, num is {}".format(os.getpid(), num))

if __name__ == "__main__":
    print("pid:{}, num is {}".format(os.getpid(), num))
    p = Process(target=show_num)
    p.start()
    p.join()

