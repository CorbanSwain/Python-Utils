#!python3
# numpy.py

# Corban Swain, 2021

import numpy as np

__all__ = ['zero_center_range']


def zero_center_range(length):
    return np.arange(length) - ((length - 1) / 2)
