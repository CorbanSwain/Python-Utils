#!python3
# files.py

import os

__all__ = ['touchdir', 'make_str_filesafe']


def touchdir(pth):
    try:
        os.mkdir(pth)
    except FileExistsError:
        pass


def make_str_filesafe(string):
    filesafe_replacements = [
        ('\"', '[`]'),
        ('\\', '[~]'),
        ('/', '[~~]'),
        ('?', '[!!]'),
        ('<', '[^]'),
        ('>', '[v]'),
        ('*', '[&]'),
        (':', '[#]'),
        (' ', '_'), ]
    for a, b in filesafe_replacements:
        string = string.replace(a, b)
    return string
