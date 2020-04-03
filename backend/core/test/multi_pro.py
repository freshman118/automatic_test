# -*- coding: utf-8 -*-
import os
from multiprocessing import Pool, Process


def f(name):
    info('function f')
    print('hello' + name)


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent name:', os.getppid())
    print('prcess id:', os.getpid())


def test_pool():
    with Pool(processes=5) as p:
        p.map()


if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('JackC',))
    p.start()
    p.join()
