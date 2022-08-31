#!python3
# dicts.py

# Project: c_swain_python_utils
# by Corban Swain 2019

__all__ = ['sort_dict', ]


def sort_dict(d: dict, *, recursive: bool = False, key=repr) -> dict:
    if recursive:
        output_d = dict()
        for k in sorted(d.keys(), key=key):
            if isinstance(d[k], dict):
                output_d[k] = sort_dict(d[k], recursive=True)
            else:
                output_d[k] = d[k]
        return output_d
    else:
        return {k: d[k] for k in sorted(d.keys(), key=key)}
