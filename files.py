#!python3
# files.py

import os

__all__ = ['get_filepath', 'touchdir', 'make_str_filesafe',
           'no_ext_basename', 'get_file_dir']


def no_ext_basename(f, extension_sep='.'):
    xtns = extension_sep
    return xtns.join(os.path.basename(f).split(xtns)[:-1])


def get_filepath(fle):
    """deprecated, do not use"""
    return os.path.dirname(os.path.abspath(fle))


def touchdir(pth, recur=True):
    try:
        os.mkdir(pth)
    except FileNotFoundError:
        if recur:
            head, tail = os.path.split(pth)
            if head:
                touchdir(head)
                touchdir(pth)
        else:
            raise
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


def get_file_dir(file_path):
    return os.path.realpath(os.path.dirname(file_path))
