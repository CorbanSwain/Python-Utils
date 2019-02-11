#!python3
# plotting.py

# Project: c_swain_python_utils
# by Corban Swain 2019

import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import time
from matplotlib.backends.backend_pdf import PdfPages

__all__ = ['despine', 'despine_all', 'save_figures', 'set_mpl_defaults']


def despine_all(ax):
    despine(ax, **{pos: True for pos in ('left', 'right', 'top', 'bottom')})


def despine(ax, **kwargs):
    [ax.spines[k].set_visible(not v) for k, v in kwargs.items()]


def save_figures(filename=None, figs=None, dpi=200, fmt='pdf'):
    if filename is None:
        filename = 'all_figures'
    filename = filename + '_' + time.strftime('%y%m%d-%H%M')

    if figs is None:
        figs = [plt.figure(n) for n in plt.get_fignums()]

    file_path = os.path.join('figures', filename)
    if fmt == 'pdf':
        file_path += '.pdf'
        with PdfPages(file_path) as pp:
            for fig in figs:
                fig.savefig(pp, format='pdf', dpi=dpi)
    else:
        for i, fig in enumerate(figs):
            fig.savefig('%s_%d.%s' % (file_path, i, fmt), format=fmt, dpi=dpi)


def set_mpl_defaults():
    mpl.rcdefaults()
    tex_preamble = r'''
    \usepackage{sansmathfonts}
    \usepackage{helvet}
    \renewcommand{\rmdefault}{\sfdefault}
    \usepackage{units}
    '''
    mpl.rc('text', usetex=True)
    mpl.rc('text.latex', preamble=tex_preamble)