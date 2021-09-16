"""
Python package for working with ToneScript, a syntax for describing the characteristics of the
call progress tones used in telephony.

.. include:: ../../docs/index.md
"""

from ._parser import *
from .model import *

__all__ = [
    parse.__name__,
    unparse.__name__,
]
