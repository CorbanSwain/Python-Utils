#!python3
# testing.py

# Project: c_swain_python_utils
# by Corban Swain 2019

import timeit
import time
import functools

__all__ = ['time_func', 'timed', ]


def time_func(func, n=1000, logger=None):
    log = logger.info if logger else print
    timeit.timeit()
    t = timeit.Timer(func)
    n_seconds = t.timeit(int(n))
    log('Time elapsed for %.0e repeats: %12.5f s' % (n, n_seconds))


def timed(logger=None):
    log = logger.info if logger else print

    def timed_decorator(func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            log('%15s took %12.6f s.' % (func.__name__, end - start))
            return result
        return func_wrapper
    return timed_decorator
