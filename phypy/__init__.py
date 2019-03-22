# -*- coding: utf-8 -*-

"""Top-level package for phypy."""

__author__ = """Chance Tarver"""
__email__ = 'tarver.chance@gmail.com'
__version__ = '0.2.7'

from . import analog
from . import corrections
from . import modulators
from . import dsp

__all__ = ['analog', 'corrections', 'modulators', 'dsp', 'structures']
