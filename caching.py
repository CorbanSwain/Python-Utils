#!python3
# caching.py

import os
import functools
import pickle
import copy
from hashlib import blake2b
from c_swain_python_utils.files import make_str_filesafe, touchdir
from c_swain_python_utils.dicts import sort_dict

__all__ = ['load_from_disk', 'save_to_disk', 'disk_cache', 'cache',
           'cache_yield_copy', 'clear_cache']


def load_from_disk(file_path):
    pickle_ext = '.pkl'
    file_path += '' if file_path.endswith(pickle_ext) else pickle_ext
    with open(file_path, 'rb') as cache_file:
        return pickle.load(cache_file)


def save_to_disk(obj, file_path):
    pickle_ext = '.pkl'
    file_path += '' if file_path.endswith(pickle_ext) else pickle_ext
    with open(file_path, 'wb+') as cache_file:
        pickle.dump(obj, cache_file, protocol=pickle.HIGHEST_PROTOCOL)


def quick_hash(string):
    h = blake2b(digest_size=25)
    h.update(string.encode(encoding='UTF-8', errors='strict'))
    return h.hexdigest()


def disk_cache(cache_dir):
    def disk_cache_decorator(func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            input_str = quick_hash(repr((args, sort_dict(kwargs))))
            save_dir = os.path.join(cache_dir,
                                    make_str_filesafe(func.__name__))
            touchdir(save_dir)
            full_path = os.path.join(save_dir, input_str)
            try:
                output = load_from_disk(full_path)
            except FileNotFoundError:
                do_calculate_output = True
            else:
                do_calculate_output = False

            if do_calculate_output:
                output = func(*args, **kwargs)
                save_to_disk(output, full_path)
            return output
        return func_wrapper
    return disk_cache_decorator


mem_cache = {}


def cache(func):
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        global mem_cache
        input_str = quick_hash(repr((args, sort_dict(kwargs))))
        try:
            func_dict = mem_cache[func.__name__]
        except KeyError:
            mem_cache[func.__name__] = {}
            func_dict = mem_cache[func.__name__]
        try:
            output = func_dict[input_str]
        except KeyError:
            do_calculate_output = True
        else:
            do_calculate_output = False

        if do_calculate_output:
            output = func_dict[input_str] = func(*args, **kwargs)
        return output
    return func_wrapper


def cache_yield_copy(func):
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        cache_func = cache(func)
        return copy.deepcopy(cache_func(*args, **kwargs))
    return func_wrapper


def clear_cache():
    global mem_cache
    mem_cache = {}
