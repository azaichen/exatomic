# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
A unified data anlaysis and visualization platform for computational and
theoretical chemists, physicists, etc. Support for molecular geometry and
orbital visualization is provided via the `Jupyter`_ notebook, a web-browser
based interactive (multi-programming language) environment.

<<<<<<< HEAD
.. extended description (todo)

=======
Warning:
    This package uses the `atomic`_ unit system (Hartree) by default.
>>>>>>> 1c37655b6be3dca60b2adbeee8ca3767e5477943

Supported Software
---------------------
The list below contains third-party software that is supported by this package.
For specific features supported (per software), see the appropriate description
below.

- :mod:`~exatomic.adf.__init__`: `Amsterdam Density Functional`_
- :mod:`~exatomic.gaussian.__init__`: `Gaussian`_
- :mod:`~exatomic.molcas.__init__`: `OpenMolcas`_
- :mod:`~exatomic.nbo.__init__`: `NBO`_
- :mod:`~exatomic.nwchem.__init__`: `NWChem`_
- :mod:`~exatomic.qe.__init__`: `Quantum ESPRESSO`_
- :mod:`~exatomic.interfaces.__init__`: Additional 3rd party support

.. _Jupyter: https://jupyter.org
.. _Amsterdam Density Functional: https://www.scm.com
.. _Gaussian: http://gaussian.com/
.. _OpenMolcas: https://gitlab.com/Molcas/OpenMolcas
.. _NBO: http://nbo6.chem.wisc.edu/
.. _NWChem: http://www.nwchem-sw.org/index.php/Main_Page
.. _Quantum ESPRESSO: http://www.quantum-espresso.org/
"""
def _jupyter_nbextension_paths():
    """Jupyter notebook extension directory paths."""
    return [{
        'section': "notebook",
        'src': "static",
        'dest': "jupyter-exatomic",
        'require': "jupyter-exatomic/extension"
    }]

<<<<<<< HEAD
from ._version import __version__
from .core import Atom
from .core import Universe
from .interfaces import XYZ




#from ._version import __exatomic_version__, __js_exatomic_version__
#__version__ = __exatomic_version__
#__js_version__ = __js_exatomic_version__
#
#try:
#    from exa.cms import (Length, Mass, Time, Current, Amount, Luminosity, Isotope,
#                         Dose, Acceleration, Charge, Dipole, Energy, Force,
#                         Frequency, MolarMass)
#except:
#    from exa.relational import Isotope, Length, Energy, Time, Amount, Constant, Mass
#from exatomic import _config
#from exatomic import error
#
## User API
#from exatomic.container import Universe, basis_function_contributions
#from exatomic.editor import Editor
#from exatomic.filetypes import XYZ, Cube
#
#from exatomic import tests
#from exatomic.algorithms import delocalization
#from exatomic.algorithms import neighbors
#from exatomic.algorithms import diffusion
#from exatomic.algorithms import pcf
#
#from exatomic import molcas
#from exatomic import nwchem
#from exatomic import gaussian
#from exatomic import adf
#from exatomic import nbo
#from exatomic import mpl
#
#from exatomic.widget import TestContainer, TestUniverse, UniverseWidget
=======
__js_version__ = "0.3.9"
from ._version import __version__
from . import core
from .core import Universe, Editor, Atom, AtomicField, Frame
from .interfaces import XYZ, Cube
from .widget import TestContainer, TestUniverse, UniverseWidget
>>>>>>> 1c37655b6be3dca60b2adbeee8ca3767e5477943
