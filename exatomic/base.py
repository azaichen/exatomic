# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
<<<<<<< HEAD
Global Functionality
########################
=======
Base Functionality
############################
>>>>>>> 1c37655b6be3dca60b2adbeee8ca3767e5477943
"""
from exa.util import isotopes


<<<<<<< HEAD
# Mappers
sym2z = isotopes.as_df()
sym2z = sym2z.drop_duplicates("symbol").set_index("symbol")["Z"].to_dict()
z2sym = {v: k for k, v in sym2z.items()}
=======
isotopedf = isotopes.as_df()

sym2z = isotopedf.drop_duplicates("symbol").set_index("symbol")["Z"].to_dict()
z2sym = {v: k for k, v in sym2z.items()}

sym2mass = {}
sym2radius = {}
sym2color = {}
for k, v in vars(isotopes).items():
    if isinstance(v, isotopes.Element):
        sym2mass[k] = v.mass
        sym2radius[k] = v.radius
        sym2color[k] = v.color
>>>>>>> 1c37655b6be3dca60b2adbeee8ca3767e5477943