# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Two Body Properties Table
##################################
This module provides functions for computing interatomic distances and bonds
(i.e. two body properties). This computation depends on the type of boundary
conditions used; free or periodic boundaries. The following table provides a
guide for the types of data found in the two types of two body tables provided
by this module.

+-------------------+----------+---------------------------------------------+
| Column            | Type     | Description                                 |
+===================+==========+=============================================+
| atom0             | integer  | foreign key to :class:`~exatomic.atom.Atom` |
+-------------------+----------+---------------------------------------------+
| atom1             | integer  | foreign key to :class:`~exatomic.atom.Atom` |
+-------------------+----------+---------------------------------------------+
| distance          | float    | distance between atom0 and atom1            |
+-------------------+----------+---------------------------------------------+
| bond              | boolean  | True if bond                                |
+-------------------+----------+---------------------------------------------+
| frame             | category | non-unique integer (req.)                   |
+-------------------+----------+---------------------------------------------+
| symbols           | category | concatenated atomic symbols                 |
+-------------------+----------+---------------------------------------------+
"""
import numpy as np
import pandas as pd
from traitlets import Unicode
from exa.numerical import DataFrame, SparseDataFrame
from exa.relational.isotope import symbol_to_radius
from exatomic.math.distance import free_two_frame, periodic_two_frame


class BaseTwo(DataFrame):
    """
    Base class for two body properties.

    See Also:
        Two body data are store depending on the boundary conditions of the
        system: :class:`~exatomic.two.FreeTwo` or :class:`~exatomic.two.PeriodicTwo`.
    """
    _index = 'two'
    _columns = ['dx', 'dy', 'dz', 'atom0', 'atom1', 'distance']
    _categories = {'symbols': str, 'atom0': np.int64, 'atom1': np.int64}

    def _bond_traits(self, label_mapper):
        """
        Traits representing bonded atoms are reported as two lists of equal
        length with atom labels.
        """
        bonded = self.ix[self['bond'] == True, ['atom0', 'atom1', 'frame']]
        lbl0 = bonded['atom0'].map(label_mapper)
        lbl1 = bonded['atom1'].map(label_mapper)
        lbl = pd.concat((lbl0, lbl1), axis=1)
        lbl['frame'] = bonded['frame']
        bond_grps = lbl.groupby('frame')
        frames = self['frame'].unique().astype(np.int64)
        b0 = np.empty((len(frames), ), dtype='O')
        b1 = b0.copy()
        for i, frame in enumerate(frames):
            try:
                b0[i] = bond_grps.get_group(frame)['atom0'].astype(np.int64).values
                b1[i] = bond_grps.get_group(frame)['atom1'].astype(np.int64).values
            except Exception:
                b0[i] = []
                b1[i] = []
        b0 = Unicode(pd.Series(b0).to_json(orient='values')).tag(sync=True)
        b1 = Unicode(pd.Series(b1).to_json(orient='values')).tag(sync=True)
        return {'two_bond0': b0, 'two_bond1': b1}


class FreeTwo(BaseTwo):
    """
    Free boundary condition two body properties table.
    """
    pass


class PeriodicTwo(BaseTwo):
    """
    Periodic boundary condition two body properties table.
    """
    pass


def compute_two(universe, bond_extra=0.45):
    """
    Compute interatomic distances.
    """
    if universe.frame.is_periodic():
        return compute_periodic_two(universe, bond_extra)
    return compute_free_two(universe, bond_extra)


def compute_free_two(universe, bond_extra=0.45):
    """
    Compute free boundary condition two body properties from an input universe.
    """
    groups = universe.atom.grpd
    n = groups.ngroups
    n = universe.frame['atom_count']
    n = (n*(n - 1)//2).sum()
    dx = np.empty((n, ), dtype=np.float64)
    dy = np.empty((n, ), dtype=np.float64)
    dz = np.empty((n, ), dtype=np.float64)
    distance = np.empty((n, ), dtype=np.float64)
    atom0 = np.empty((n, ), dtype=np.int64)
    atom1 = np.empty((n, ), dtype=np.int64)
    start = 0
    stop = 0
    for frame, group in groups:
        x = group['x'].values.astype(np.float64)
        y = group['y'].values.astype(np.float64)
        z = group['z'].values.astype(np.float64)
        idx = group.index.values.astype(np.int64)
        dxx, dyy, dzz, a0, a1, dist = free_two_frame(x, y, z, idx)
        stop += len(dxx)
        dx[start:stop] = dxx
        dy[start:stop] = dyy
        dz[start:stop] = dzz
        atom0[start:stop] = a0
        atom1[start:stop] = a1
        distance[start:stop] = dist
        start = stop
    atom0 = pd.Series(atom0, dtype='category')
    atom1 = pd.Series(atom0, dtype='category')
    two = pd.DataFrame.from_dict({'dx': dx, 'dy': dy, 'dz': dz, 'distance': distance,
                                  'atom0': atom0, 'atom1': atom1})
    mapper = universe.atom['symbol'].astype(str).map(symbol_to_radius())
    radius0 = two['atom0'].map(mapper)
    radius1 = two['atom1'].map(mapper)
    two['mbl'] = radius0 + radius1 + bond_extra
    two['bond'] = two['distance'] < two['mbl']
    del two['mbl']
    return two


def compute_periodic_two(universe, bond_extra=0.45):
    """
    Compute periodic two body properties.
    """
    grps = universe.atom[['x', 'y', 'z', 'frame']].copy()
    grps['frame'] = grps['frame'].astype(np.int64)
    grps.update(universe.unit_atom)
    grps = grps.groupby('frame')
    n = universe.frame['atom_count']
    n = 27*(n*(n-1)//2).sum()
    dx = np.empty((n, ), dtype=np.float64)
    dy = np.empty((n, ), dtype=np.float64)
    dz = np.empty((n, ), dtype=np.float64)
    atom0 = np.empty((n, ), dtype=np.int64)
    atom1 = np.empty((n, ), dtype=np.int64)
    distance = np.empty((n, ), dtype=np.float64)
    px = np.empty((n, ), dtype=np.float64)
    py = np.empty((n, ), dtype=np.float64)
    pz = np.empty((n, ), dtype=np.float64)
    start = 0
    stop = 0
    for frame, grp in grps:
        ux = grp['x'].values.astype(np.float64)
        uy = grp['y'].values.astype(np.float64)
        uz = grp['z'].values.astype(np.float64)
        idx = grp.index.values.astype(np.int64)
        rx, ry, rz = universe.frame.ix[frame, ['rx', 'ry', 'rz']]
        dxx, dyy, dzz, d, a0, a1, pxx, pyy, pzz = periodic_two_frame(ux, uy, uz, rx, ry, rz, idx)
        stop += len(dxx)
        dx[start:stop] = dxx
        dy[start:stop] = dyy
        dz[start:stop] = dzz
        distance[start:stop] = d
        atom0[start:stop] = a0
        atom1[start:stop] = a1
        px[start:stop] = pxx
        py[start:stop] = pyy
        pz[start:stop] = pzz
        start = stop
    atom0 = pd.Series(atom0, dtype='category')
    atom1 = pd.Series(atom0, dtype='category')
    two = pd.DataFrame.from_dict({'dx':dx, 'dy': dy, 'dz': dz, 'distance': distance,
                                  'atom0': atom0, 'atom1': atom1})
    patom = pd.DataFrame.from_dict({'x': px, 'y': py, 'z': pz})
    mapper = universe.atom['symbol'].astype(str).map(symbol_to_radius())
    radius0 = two['atom0'].map(mapper)
    radius1 = two['atom1'].map(mapper)
    two['mbl'] = radius0 + radius1 + bond_extra
    two['bond'] = two['distance'] < two['mbl']
    del two['mbl']
    return two, patom


def compute_bond_count(universe):
    """
    Computes bond count (number of bonds associated with a given atom index).

    Args:
        universe (:class:`~exatomic.universe.Universe`): Atomic universe

    Returns:
        counts (:class:`~numpy.ndarray`): Bond counts

    Note:
        For both periodic and non-periodic universes, counts returned are
        atom indexed. Counts for projected atoms have no meaning/are not
        computed during two body property calculation.
    """
    stack = universe.two.ix[universe.two['bond'] == True, ['atom0', 'atom1']].stack()
    return stack.value_counts().sort_index()


#def bond_summary_by_label_pairs(universe, *labels, length='A', stdev=False,
#                                stderr=False, variance=False, ncount=False):
#    """
#    Compute a summary of bond lengths by label pairs
#
#    Args:
#        universe: The atomic container
#        \*labels: Any number of label pairs (e.g. ...paris(uni, (0, 1), (1, 0), ...))
#        length (str): Output length unit (default Angstrom)
#        stdev (bool): Compute the standard deviation of the mean (default false)
#        stderr (bool): Compute the standard error in the mean (default false)
#        variance (bool): Compute the variance in the mean (default false)
#        ncount (bool): Include the data point count (default false)
#
#    Returns:
#        summary (:class:`~pandas.DataFrame`): Bond length dataframe
#    """
#    l0, l1 = list(zip(*labels))
#    l0 = np.array(l0, dtype=np.int64)
#    l1 = np.array(l1, dtype=np.int64)
#    ids = unordered_pairing(l0, l1)
#    bonded = universe.two[universe.two['bond'] == True].copy()
#    if universe.is_periodic:
#        bonded['atom0'] = bonded['prjd_atom0'].map(universe.projected_atom['atom'])
#        bonded['atom1'] = bonded['prjd_atom1'].map(universe.projected_atom['atom'])
#    bonded['label0'] = bonded['atom0'].map(universe.atom['label'])
#    bonded['label1'] = bonded['atom1'].map(universe.atom['label'])
#    bonded['id'] = unordered_pairing(bonded['label0'].values.astype(np.int64),
#                                     bonded['label1'].values.astype(np.int64))
#    return bonded[bonded['id'].isin(ids)]
#    grps = bonded[bonded['id'].isin(ids)].groupby('id')
#    df = grps['distance'].mean().reset_index()
#    if variance:
#        df['variance'] = grps['distance'].var().reset_index()['distance']
#        df['variance'] *= Length['au', length]
#    if stderr:
#        df['stderr'] = grps['distance'].std().reset_index()['distance']
#        df['stderr'] /= np.sqrt(grps['distance'].size().values[0])
#        df['stderr'] *= Length['au', length]
#    if stdev:
#        df['stdev'] = grps['distance'].std().reset_index()['distance']
#        df['stdev'] *= Length['au', length]
#    if ncount:
#        df['count'] = grps['distance'].size().reset_index()[0]
#    mapper = bonded.drop_duplicates('id').set_index('id')
#    df['symbols'] = df['id'].map(mapper['symbols'])
#    df['distance'] *= Length['au', length]
#    df['label0'] = df['id'].map(mapper['label0'])
#    df['label1'] = df['id'].map(mapper['label1'])
#    del df['id']
#    return df
#
#
#def n_nearest_distances_by_symbols(universe, a, b, n, length='A', stdev=False,
#                                   stderr=False, variance=False, ncount=False):
#    """
#    Compute a distance summary of the n nearest pairs of symbols, (a, b).
#
#    Args:
#        universe: The atomic universe
#        a (str): Symbol string
#        b (str): Symbol string
#        n (int): Number of distances to include
#        stdev (bool): Compute the standard deviation of the mean (default false)
#        stderr (bool): Compute the standard error in the mean (default false)
#        variance (bool): Compute the variance in the mean (default false)
#        ncount (bool): Include the data point count (default false)
#
#    Returns:
#        summary (:class:`~pandas.DataFrame`): Distance summary dataframe
#    """
#    def compute(group):
#        return group.sort_values('distance').iloc[:n]
#
#    df = universe.two[universe.two['symbols'].isin([a+b, b+a])]
#    df = df.groupby('frame').apply(compute)
#    df['pair'] = list(range(n)) * (len(df) // n)
#    pvd = df.pivot('frame', 'pair', 'distance')
#    df = pvd.mean(0).reset_index()
#    df.columns = ['pair', 'distance']
#    df['distance'] *= Length['au', length]
#    if stdev:
#        df['stdev'] = pvd.std().reset_index()[0]
#        df['stdev'] *= Length['au', length]
#    if stderr:
#        df['stderr'] = pvd.std().reset_index()[0]
#        df['stderr'] /= np.sqrt(len(pvd))
#        df['stderr'] *= Length['au', length]
#    if variance:
#        df['variance'] = pvd.var().reset_index()[0]
#        df['variance'] *= Length['au', length]
#    if ncount:
#        df['count'] = pvd.shape[0]
#    return df
#
