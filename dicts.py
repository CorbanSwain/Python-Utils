#!python3
# dicts.py

# Project: c_swain_python_utils
# by Corban Swain 2019

__all__ = ['sort_dict', ]


def sort_dict(d):
    return {k: d[k] for k in sorted(d.keys())}
