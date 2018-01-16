# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Molecular Orbital Utilities
##############################
Molecular orbitals are constructed symbolically
then evaluated on a numerical grid.
These are their stories.
'''
import numpy as np
import pandas as pd
from numba import jit
from numexpr import evaluate
from IPython.display import display
from ipywidgets import FloatProgress
from exatomic.core.field import AtomicField
from exatomic.algorithms.basis import gen_bfns


def compare_fields(uni0, uni1, rtol=5e-5, atol=1e-12, signed=True, verbose=True):
    """Compare field values of multiple universe.
    It is expected that fields are in the same order."""
    fracs, kws = [], {'rtol': rtol, 'atol': atol}
    for i, (f0, f1) in enumerate(zip(uni0.field.field_values,
                                     uni1.field.field_values)):
        n = np.isclose(f0, f1, **kws).sum()
        if not signed:
            n = max(n, np.isclose(f0, -f1, **kwargs).sum())
        fracs.append(n / f0.shape[0])
    if verbose:
        fmt = '{:<12}:{:>18}'
        print(fmt.format(len(fracs), 'Fraction'))
        fmt = fmt.replace('18', '18.12f')
        for i, f in enumerate(fracs):
            print(fmt.format(i, f))
    else:
        return fracs


def numerical_grid_from_field_params(fps):
    """Construct numerical grid arrays from field parameters."""
    if isinstance(fps, pd.DataFrame):
        fps = fps.loc[0]
    ox, nx, dx = fps.ox, int(fps.nx), fps.dxi
    oy, ny, dy = fps.oy, int(fps.ny), fps.dyj
    oz, nz, dz = fps.oz, int(fps.nz), fps.dzk
    mx = ox + (nx - 1) * dx
    my = oy + (ny - 1) * dy
    mz = oz + (nz - 1) * dz
    x = np.linspace(ox, mx, nx)
    y = np.linspace(oy, my, ny)
    z = np.linspace(oz, mz, nz)
    return _meshgrid3d(x, y, z)


def make_fps(rmin=None, rmax=None, nr=None, nrfps=1,
             xmin=None, xmax=None, nx=None, frame=0,
             ymin=None, ymax=None, ny=None, field_type=0,
             zmin=None, zmax=None, nz=None, label=0,
             ox=None, fx=None, dxi=None, dxj=None, dxk=None,
             oy=None, fy=None, dyi=None, dyj=None, dyk=None,
             oz=None, fz=None, dzi=None, dzj=None, dzk=None,
             fps=None):
    """
    Generate the necessary field parameters of a numerical grid field
    as an exatomic.field.AtomicField.

    Args
        nrfps (int): number of field parameters with same dimensions
        rmin (float): minimum value in an arbitrary cartesian direction
        rmax (float): maximum value in an arbitrary cartesian direction
        nr (int): number of grid points between rmin and rmax
        xmin (float): minimum in x direction (optional)
        xmax (float): maximum in x direction (optional)
        ymin (float): minimum in y direction (optional)
        ymax (float): maximum in y direction (optional)
        zmin (float): minimum in z direction (optional)
        zmax (float): maximum in z direction (optional)
        nx (int): steps in x direction (optional)
        ny (int): steps in y direction (optional)
        nz (int): steps in z direction (optional)
        ox (float): origin in x direction (optional)
        oy (float): origin in y direction (optional)
        oz (float): origin in z direction (optional)
        dxi (float): x-component of x-vector specifying a voxel
        dxj (float): y-component of x-vector specifying a voxel
        dxk (float): z-component of x-vector specifying a voxel
        dyi (float): x-component of y-vector specifying a voxel
        dyj (float): y-component of y-vector specifying a voxel
        dyk (float): z-component of y-vector specifying a voxel
        dzi (float): x-component of z-vector specifying a voxel
        dzj (float): y-component of z-vector specifying a voxel
        dzk (float): z-component of z-vector specifying a voxel
        label (str): an identifier passed to the widget (optional)
        field_type (str): alternative identifier (optional)

    Returns
        fps (pd.Series): field parameters
    """
    if fps is not None: return pd.concat([fps.loc[0]] * nrfps, axis=1).T
    if any((par is None for par in [rmin, rmax, nr])):
        if all((par is not None for par in (xmin, xmax, nx,
                                            ymin, ymax, ny,
                                            zmin, zmax, nz))):
            pass
        elif all((par is None for par in (ox, dxi, dxj, dxk))):
            raise Exception("Must supply at least rmin, rmax, nr or field"
                            " parameters as specified by a cube file.")
    d = {}
    allcarts = [['x', 0, xmin, xmax, nx, ox, (dxi, dxj, dxk)],
                ['y', 1, ymin, ymax, ny, oy, (dyi, dyj, dyk)],
                ['z', 2, zmin, zmax, nz, oz, (dzi, dzj, dzk)]]
    for akey, aidx, amin, amax, na, oa, da in allcarts:
        if oa is None:
            amin = rmin if amin is None else amin
            amax = rmax if amax is None else amax
            na = nr if na is None else na
        else: amin = oa
        dw = [0, 0, 0]
        if all(i is None for i in da): dw[aidx] = (amax - amin) / na
        else: dw = da
        d[akey] = [amin, na, dw]
    fp = pd.Series({
        'dxi': d['x'][2][0], 'dyj': d['y'][2][1], 'dzk': d['z'][2][2],
        'dxj': d['x'][2][1], 'dyk': d['y'][2][2], 'dzi': d['z'][2][0],
        'dxk': d['x'][2][2], 'dyi': d['y'][2][0], 'dzj': d['z'][2][1],
        'ox': d['x'][0], 'oy': d['y'][0], 'oz': d['z'][0], 'frame': frame,
        'nx': d['x'][1], 'ny': d['y'][1], 'nz': d['z'][1], 'label': label,
        'field_type': field_type
        })
    return pd.concat([fp] * nrfps, axis=1).T


def _make_field(flds, fps):
    """Return an AtomicField from field arrays and parameters."""
    try:
        nvec = flds.shape[0]
        if len(fps.index) == nvec:
            fps.reset_index(drop=True, inplace=True)
            return AtomicField(
                fps, field_values=[flds[i] for i in range(nvec)])
        return AtomicField(
            make_fps(nrfps=nvec, fps=fps),
            field_values=[flds[i] for i in range(nvec)])
    except:
        return AtomicField(
            make_fps(nrfps=1, **fps),
            field_values=[flds])


def _compute_current_density(bvs, gvx, gvy, gvz, cmatr, cmati, occvec, verbose=True):
    """Compute the current density in each cartesian direction."""
    nbas, npts = bvs.shape
    curx = np.zeros(npts, dtype=np.float64)
    cury = np.zeros(npts, dtype=np.float64)
    curz = np.zeros(npts, dtype=np.float64)
    fp = FloatProgress(description='Computing:')
    if verbose:
        display(fp)
    for mu in range(nbas):
        fp.value = mu / nbas * 100
        crmu = cmatr[mu]
        cimu = cmati[mu]
        bvmu = bvs[mu]
        gvxmu = gvx[mu]
        gvymu = gvy[mu]
        gvzmu = gvz[mu]
        for nu in range(nbas):
            crnu = cmatr[nu]
            cinu = cmati[nu]
            bvnu = bvs[nu]
            gvxnu = gvx[nu]
            gvynu = gvy[nu]
            gvznu = gvz[nu]
            cval = evaluate('-0.5 * (occvec * (crmu * cinu - cimu * crnu))').sum()
            curx = evaluate('curx + cval * (bvmu * gvxnu - gvxmu * bvnu)')
            cury = evaluate('cury + cval * (bvmu * gvynu - gvymu * bvnu)')
            curz = evaluate('curz + cval * (bvmu * gvznu - gvzmu * bvnu)')
    fp.close()
    return curx, cury, curz


def _determine_bfns(uni, frame, norm, forcecart=False):
    """Cache and return symbolic basis functions if they don't exist."""
    if hasattr(uni, 'basis_functions'):
        if frame in uni.basis_functions:
            return uni.basis_functions[frame]
        else:
            uni.basis_functions[frame] = gen_bfns(uni, frame=frame,
                                                  forcecart=forcecart)
            return uni.basis_functions[frame]
    else:
        uni.basis_functions = {frame: gen_bfns(uni, frame=frame,
                                               forcecart=forcecart)}
        return uni.basis_functions[frame]


def _determine_vector(uni, vector):
    """Find some orbital indices in a universe."""
    if isinstance(vector, int): return np.array([vector])
    typs = (list, tuple, range, np.ndarray)
    if isinstance(vector, typs): return np.array(vector)
    norb = len(uni.basis_set_order.index)
    if vector is None:
        if norb < 10:
            return np.array(range(norb))
        if hasattr(uni, 'orbital'):
            homo = uni.orbital.get_orbital().vector
        elif hasattr(uni.frame, 'N_e'):
            homo = uni.frame['N_e'].values[0]
        elif hasattr(uni.atom, 'Zeff'):
            homo = uni.atom['Zeff'].sum() // 2
        elif hasattr(uni.atom, 'Z'):
            homo = uni.atom['Z'].sum() // 2
        else:
            uni.atom['Z'] = uni.atom['symbol'].map(sym2z)
            homo = uni.atom['Z'].sum() // 2
        if homo < 5:
            return np.array(range(0, homo + 5))
        else:
            return np.array(range(homo - 5, homo + 7))
    else:
        raise TypeError('Try specifying vector as a list or int')


def _determine_fps(uni, fps, nvec):
    """Find some numerical grid parameters in a universe."""
    if fps is None:
        if hasattr(uni, 'field'):
            return make_fps(nrfps=nvec, **uni.field.loc[0])
        desc = uni.atom.describe()
        kwargs = {'xmin': desc['x']['min'] - 5,
                  'xmax': desc['x']['max'] + 5,
                  'ymin': desc['y']['min'] - 5,
                  'ymax': desc['y']['max'] + 5,
                  'zmin': desc['z']['min'] - 5,
                  'zmax': desc['z']['max'] + 5,
                  'nx': 41, 'ny': 41, 'nz': 41,
                  'nrfps': nvec}
        return make_fps(**kwargs)
    return make_fps(nrfps=nvec, **fps)


def _check_column(uni, df, key): # mocoefs, orbocc, rcoefs, icoefs):
    """Repetitive checking of columns in a universe."""
    if key is None:
        if df == 'momatrix':
            key = 'coef'
        elif df == 'orbital':
            key = 'occupation'
    err = '"{}" not in uni.{}.columns'.format
    if key not in getattr(uni, df).columns:
        raise Exception(err(key, df))
    return key


@jit(nopython=True, nogil=True, parallel=True)
def _compute_orbitals(bvs, vecs, cmat):
    """Compute orbitals from numerical basis functions."""
    ovs = np.empty((len(vecs), bvs.shape[1]), dtype=np.float64)
    for i, vec in enumerate(vecs):
        ovs[i] = np.dot(cmat[:, vec], bvs)
    return ovs

def _compute_orbitals_nojit(bvs, vecs, cmat):
    """Compute orbitals from numerical basis functions."""
    ovs = np.empty((len(vecs), bvs.shape[1]), dtype=np.float64)
    for i, vec in enumerate(vecs):
        ovs[i] = np.dot(cmat[:, vec], bvs)
    return ovs


@jit(nopython=True, nogil=True, parallel=True)
def _compute_density(ovs, occvec):
    """Sum orbitals multiplied by their occupations."""
    norb, npts = ovs.shape
    dens = np.empty(npts, dtype=np.float64)
    for i in range(norb):
        ovs[i] *= ovs[i]
    dens = np.dot(occvec, ovs)
    return dens


@jit(nopython=True, nogil=True, parallel=True)
def _compute_orb_ang_mom(rx, ry, rz, jx, jy, jz, mxs):
    """Compute the orbital angular momentum in each direction and the sum."""
    npts = rx.shape[0]
    ang_mom = np.empty((4, npts), dtype=np.float64)
    a0 = ry * jz - rz * jy
    a1 = rz * jx - rx * jz
    a2 = rx * jy - ry * jx
    ang_mom[0] = mxs[0,0] * a0 + mxs[1,0] * a1 + mxs[2,0] * a2
    ang_mom[1] = mxs[0,1] * a0 + mxs[1,1] * a1 + mxs[2,1] * a2
    ang_mom[2] = mxs[0,2] * a0 + mxs[1,2] * a1 + mxs[2,2] * a2
    ang_mom[3] = ang_mom[0] + ang_mom[1] + ang_mom[2]
    return ang_mom


@jit(nopython=True, nogil=True, parallel=True)
def _meshgrid3d(x, y, z):
    tot = len(x) * len(y) * len(z)
    xs = np.empty(tot, dtype=np.float64)
    ys = np.empty(tot, dtype=np.float64)
    zs = np.empty(tot, dtype=np.float64)
    cnt = 0
    for i in x:
        for j in y:
            for k in z:
                xs[cnt] = i
                ys[cnt] = j
                zs[cnt] = k
                cnt += 1
    return xs, ys, zs
