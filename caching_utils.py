#!python3
# caching_utils.py

import os
import functools
import pickle
import copy
from file_utils import make_str_filesafe, touchdir

# Constants
PICKLE_EXT = '.pkl'


def load_from_disk(file_path):
    file_path += '' if file_path.endswith(PICKLE_EXT) else PICKLE_EXT
    with open(file_path, 'rb') as cache_file:
        return pickle.load(cache_file)


def save_to_disk(obj, file_path):
    file_path += '' if file_path.endswith(PICKLE_EXT) else PICKLE_EXT
    with open(file_path, 'wb+') as cache_file:
        pickle.dump(obj, cache_file, protocol=pickle.HIGHEST_PROTOCOL)


def disk_cache(cache_dir):
    def disk_cache_decorator(func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            input_str = make_str_filesafe(repr((args, kwargs)))
            save_dir = os.path.join(cache_dir,
                                    make_str_filesafe(func.__name__))
            touchdir(save_dir)
            full_path = os.path.join(save_dir, input_str)
            try:
                output = load_from_disk(full_path)
            except FileNotFoundError:
                output = func(*args, **kwargs)
                save_to_disk(output, full_path)
            finally:
                return output
        return func_wrapper
    return disk_cache_decorator


mem_cache = {}


def cache(func):
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        input_str = repr((args, kwargs))
        try:
            func_dict = mem_cache[func.__name__]
        except KeyError:
            mem_cache[func.__name__] = {}
            func_dict = mem_cache[func.__name__]
        try:
            return func_dict[input_str]
        except KeyError:
            func_dict[input_str] = func(*args, **kwargs)
            return func_dict[input_str]
    return func_wrapper


def cache_yield_copy(func):
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        cache_func = cache(func)
        return copy.deepcopy(cache_func(*args, **kwargs))
    return func_wrapper
