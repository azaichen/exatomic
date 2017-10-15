# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exatomic
#############
This package provides a unified data format for organizing, analyzing, and
visualizing data coming from the most common computational chemistry software
programs.

Warning:
    This package uses the `atomic`_ unit system (Hartree) by default.

.. _atomic: https://en.wikipedia.org/wiki/Atomic_units
"""

def _jupyter_nbextension_paths():
    """
    Automatically generated by the `cookiecutter`_.
    .. _cookiecutter: https://github.com/jupyter/widget-cookiecutter
    """
    return [{
        'section': "notebook",
        'src': "static",
        'dest': "jupyter-exatomic",
        'require': "jupyter-exatomic/extension"
    }]

__js_version__ = "0.3.9"
from ._version import __version__
from . import core
#from .core import Editor
#from .interfaces import XYZ, Cube
