#!python3
# yaml.py

# Corban Swain, 2021

import yaml

__all__ = ['read_yaml']


def read_yaml(filepath):
    with open(filepath, 'r') as f:
        y = yaml.safe_load(f)

    return y
