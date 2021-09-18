"""
Python package for working with ToneScript, a syntax for describing the characteristics of the
call progress tones used in telephony.

.. include:: ../../docs/index.md
"""

from ._parser import parse
from ._parser import unparse
from ._wave import render


__all__ = [
    parse.__name__,
    render.__name__,
    unparse.__name__,
]
