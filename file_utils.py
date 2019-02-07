#!python3
# file_utils.py

import os


def touchdir(pth):
    try:
        os.mkdir(pth)
    except FileExistsError:
        pass


def make_str_filesafe(string):
    replacements = [('\"', '[`]'),
                    ('\\', '[~]'),
                    ('/', '[~~]'),
                    ('?', '[!!]'),
                    ('<', '[^]'),
                    ('>', '[v]'),
                    ('*', '[&]'),
                    (' ', '_')]
    for a, b in replacements:
        string = string.replace(a, b)
    return string
