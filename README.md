<<<<<<< HEAD
[![exatomic logo](docs/source/static/logo.png)](https://exa-analytics.github.io)  
*A unified platform for theoretical and computational chemists*


# Installation
[![conda Badge](https://anaconda.org/exaanalytics/exatomic/badges/installer/conda.svg)](https://conda.anaconda.org/exaanalytics)  
[![pypi badge](https://badge.fury.io/py/exatomic.svg)](https://badge.fury.io/py/exatomic)  
=======
[![exatomic logo](docs/source/static/logo.png)](https://exa-analytics.github.io)
*A unified platform for computational chemists*


# Installation
[![conda Badge](https://anaconda.org/exaanalytics/exatomic/badges/installer/conda.svg)](https://conda.anaconda.org/exaanalytics)
[![pypi badge](https://badge.fury.io/py/exatomic.svg)](https://badge.fury.io/py/exatomic)
>>>>>>> 1c37655b6be3dca60b2adbeee8ca3767e5477943
Exa is available through [anaconda](https://www.continuum.io/downloads)

    $ conda install -c exaanalytics exatomic

or [pypi](https://pypi.python.org/pypi).

    $ pip install exatomic
<<<<<<< HEAD
    $ jupyter nbextension enable --py --sys-prefix exatomic


# Getting Started
[![docs](https://readthedocs.org/projects/exatomic/badge/?version=latest)](https://exa-analytics.github.io/exatomic/)  
[![gitter](https://badges.gitter.im/exa-analytics/exatomic.svg)](https://gitter.im/exa-analytics/exatomic)  
Building the docs requires [sphinx](http://www.sphinx-doc.org/en/stable).
On Linux or Mac OS:

    $ cd docs
    $ make html

On Windows:

    $ cd docs
    $ ./make.bat html


# Contributing
[![travis](https://travis-ci.org/exa-analytics/exatomic.svg?branch=master)](https://travis-ci.org/exa-analytics/exatomic)  
[![Coverage](https://coveralls.io/repos/github/exa-analytics/exatomic/badge.svg?branch=master)](https://coveralls.io/github/exa-analytics/exatomic?branch=master)  
[![Codacy](https://api.codacy.com/project/badge/Grade/221e700665c74c85b8255e5b399490d4)](https://www.codacy.com/app/alexvmarch/exatomic?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=exa-analytics/exatomic&amp;utm_campaign=Badge_Grade)  

For a development ready installation:

    $ git clone https://github.com/exa-analytics/exatomic.git
    $ cd exatomic
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix exatomic
    $ jupyter nbextension enable --py --sys-prefix exatomic

Note that this requires npm. On Windows, symlinks will not work but as a work-
around, extensions can be recompiled and reinstalled upon edits without the
need to reinstall the package.


# Reference
[![DOI](https://zenodo.org/badge/23807/exa-analytics/exatomic.svg)](https://zenodo.org/badge/latestdoi/23807/exa-analytics/exatomic)  


# Legal
[![Apache License 2.0](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0)  
Copyright (c) 2015-2016, Exa Analytics Development Team  
Distributed under the terms of the Apache License 2.0  
=======


# Getting Started
[![docs](https://readthedocs.org/projects/exatomic/badge/?version=latest)](https://exa-analytics.github.io/exatomic/)
[![gitter](https://badges.gitter.im/exa-analytics/exatomic.svg)](https://gitter.im/exa-analytics/exatomic)
Building the docs requires [sphinx](http://www.sphinx-doc.org/en/stable).

    $ cd docs
    $ make html           # .\make.bat html


# Development
[![Travis-CI](https://travis-ci.org/exa-analytics/exatomic.svg?branch=master)](https://travis-ci.org/exa-analytics/exatomic)
[![Appveyor](https://ci.appveyor.com/api/projects/status/5palls4vcdipkv00/branch/master?svg=true)](https://ci.appveyor.com/project/avmarchenko/exatomic/branch/master)
[![Coveralls](https://coveralls.io/repos/github/exa-analytics/exatomic/badge.svg)](https://coveralls.io/github/exa-analytics/exatomic)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ac0112a9a8b9496e8b74f0ab618386ce)](https://www.codacy.com/app/alexvmarch/exatomic?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=avmarchenko/exatomic&amp;utm_campaign=Badge_Grade)

For a development ready installation (requires node package manager):

    $ git clone https://github.com/exa-analytics/exatomic.git
    $ cd exatomic/js
    $ ./js.sh    # .\js.bat
    $ cd ../
    $ pip install -e .


# Reference
[![DOI](https://zenodo.org/badge/49284471.svg)](https://zenodo.org/badge/latestdoi/49284471)


# Legal
[![Apache License 2.0](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0)
Copyright (c) 2015-2017, Exa Analytics Development Team
Distributed under the terms of the Apache License 2.0
>>>>>>> 1c37655b6be3dca60b2adbeee8ca3767e5477943
