# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
<<<<<<< HEAD
#'''
#Molcas Output Parser
######################
#Multiple frames are not currently supported
#'''
#import os
#import pandas as pd
#import numpy as np
#from io import StringIO
#
#from .editor import Editor
#
#from exatomic.atom import Atom
#from exatomic.basis import Overlap
#from exatomic.orbital import DensityMatrix
#from exatomic.algorithms.basis import (lmap, lorder,
#                                       spher_lml_count)
##from exatomic import Isotope
#from exa.relational.isotope import symbol_to_z, z_to_symbol
#from exatomic.basis import Overlap, lmap, rlmap, spher_lml_count
#from exatomic.orbital import DensityMatrix
#from exa.relational.isotope import symbol_to_z
#
#symbol_to_z = symbol_to_z()
#
#class Orb(Editor):
#
#    def _parse_momatrix(self):
#        print("molcas.output.Base._parse_momatrix")
#        dim = int(self[5])
#        found = self.find(_orb_orb, _orb_occ, keys_only=True)
#        ndim = dim * dim
#        orbstarts = np.array(found[_orb_orb]) + 1
#        occstart = found[_orb_occ][0] + 1
#        nrcol = len(self[orbstarts[0]].split())
#        nrcolocc = len(self[occstart].split())
#        coefs = np.empty(ndim, dtype=np.float64)
#        occvec = np.empty(dim, dtype=np.float64)
#        if nrcol == 1:
#            orbstops = np.ceil(orbstarts + dim / 4).astype(int)
#            occstop = np.ceil(occstart + dim / 4).astype(int)
#            for i, (start, stop) in enumerate(zip(orbstarts, orbstops)):
#                tmp = [[ln[chnk] for chnk in _orb_slice if ln[chnk]] for ln in self[start:stop]]
#                coefs[i*dim:i*dim + dim] = pd.DataFrame(tmp).stack().values
#            tmp = [[ln[chnk] for chnk in _orb_slice if ln[chnk]] for ln in self[occstart:occstop]]
#            occvec[:] = pd.DataFrame(tmp).stack().values
#        else:
#            orbstops = np.ceil(orbstarts + dim / nrcol).astype(int)
#            occstop = np.ceil(occstart + dim / nrcolocc).astype(int)
#            for i, (start, stop) in enumerate(zip(orbstarts, orbstops)):
#                coefs[i*dim:i*dim + dim] = self.pandas_dataframe(start, stop, nrcol).stack().values
#            occvec[:] = self.pandas_dataframe(occstart, occstop, nrcolocc).stack().values
#        momatrix = pd.DataFrame.from_dict({'coef': coefs,
#                                           'orbital': np.repeat(range(dim), dim),
#                                           'chi': np.tile(range(dim), dim),
#                                           'frame': 0})
#        self.momatrix = momatrix
#        self.occupation_vector = occvec
#
#class Grid(Base):
#
#    def parse_atom(self):
#        print("molcas.output.Grid.parse_atom")
#        fidx, nat = self.find(_re_grid_nat, keys_only=True)[0]
#        nat = int(nat.split()[-1])
#        atom = self.pandas_dataframe(fidx, fidx + nat, 4)
#        atom['frame'] = 0
#        atom.columns = ['symbol', 'x', 'y', 'z', 'frame']
#        self._atom = Atom(atom)
#
#    def parse_orbital(self):
#        print("molcas.output.Grid.parse_momatrix")
#        self.orbital = None
#
#    def parse_momatrix(self):
#        print("molcas.output.Grid.parse_momatrix")
#        self._parse_momatrix()
#
#    def __init__(self, *args, **kwargs):
#        print("molcas.output.Grid")
#        super().__init__(*args, **kwargs)
#        self.parse()
#    def to_universe(self):
#        raise NotImplementedError("No atom information given. " \
#                                  "Attach these attributes to a universe.")
#
#    def _one_el(self, starts, step, ncol):
#        func = pd.read_csv
#        kwargs = {'header': None}
#        if ncol == 1:
#            func = pd.read_fwf
#            kwargs['widths'] = [18] * 4
#        else:
#            kwargs['delim_whitespace'] = True
#        return [func(StringIO('\n'.join(self[start:start + step])),
#                     **kwargs).stack().values for start in starts]
#
#    def parse_momatrix(self):
#        dim = int(self[5])
#        ndim = dim * dim
#        found = self.find(_re_orb, _re_occ,
#                          _re_ens, keys_only=True)
#        skips = found[_re_orb]
#        start = skips[0]
#        occs = [i + 1 for i in found[_re_occ]]
#        ens = [i + 1 for i in found[_re_ens]]
#        if not found[_re_ens]: ens = False
#        ncol = len(self[start + 1].split())
#        cols = 4 if ncol == 1 else ncol
#        chnk = np.ceil(dim / cols).astype(np.int64)
#        orbdx = np.repeat(range(dim), chnk)
#        if len(occs) == 2:
#            skips.insert(dim, skips[dim] - 1)
#            orbdx = np.concatenate([orbdx, orbdx])
#        skips = [i - skips[0] for i in skips]
#        if ncol == 1:
#            coefs = pd.read_fwf(StringIO('\n'.join(self[start:occs[0]-2])),
#                                skiprows=skips, header=None, widths=[18]*4)
#            if ens: ens = self._one_el(ens, chnk, ncol)
#        else:
#            coefs = self.pandas_dataframe(start, occs[0]-2, ncol,
#                                          **{'skiprows': skips})
#            if ens:
#                echnk = np.ceil(dim / len(self[ens[0] + 1].split())).astype(np.int64)
#                ens = self._one_el(ens, echnk, ncol)
#        occs = self._one_el(occs, chnk, ncol)
#        coefs['idx'] = orbdx
#        coefs = coefs.groupby('idx').apply(pd.DataFrame.stack).drop(
#                                           'idx', level=2).values
#        mo = {'orbital': np.repeat(range(dim), dim), 'frame': 0,
#              'chi': np.tile(range(dim), dim)}
#        if ens:
#            orb = {'frame': 0, 'group': 0}
#        if len(occs) == 2:
#            mo['coef'] = coefs[:len(coefs)//2]
#            mo['coef1'] = coefs[len(coefs)//2:]
#            self.occupation_vector = {'coef': occs[0], 'coef1': occs[1]}
#            if ens:
#                orb['occupation'] = np.concatenate(occs)
#                orb['energy'] = np.concatenate(ens)
#                orb['vector'] = np.concatenate([range(dim), range(dim)])
#                orb['spin'] = np.concatenate([np.zeros(dim), np.ones(dim)])
#        else:
#            mo['coef'] = coefs
#            self.occupation_vector = occs[0]
#            if ens:
#                orb['occupation'] = occs[0]
#                orb['energy'] = ens[0]
#                orb['vector'] = range(dim)
#                orb['spin'] = np.zeros(dim)
#        self.momatrix = pd.DataFrame.from_dict(mo)
#        if ens:
#            self.orbital = pd.DataFrame.from_dict(orb)
#
#    def __init__(self, *args, **kwargs):
#        super(Orb, self).__init__(*args, **kwargs)
## Works for both
#_orb_orb = 'ORBITAL'
#_orb_occ = 'OCCUPATION NUMBERS'
#
#class Orb(Base):
#
#    def parse_momatrix(self):
#        print("molcas.output.Orb.parse_momatrix")
#        self._parse_momatrix()
#
#    def __init__(self, *args, **kwargs):
#        print("molcas.output.Orb")
#        super().__init__(*args, **kwargs)
#_re_orb = 'ORBITAL'
#_re_occ = 'OCCUPATION NUMBERS'
#_re_ens = 'ONE ELECTRON ENERGIES'
#
#
#class Output(Editor):
#
#    def parse_atom(self):
#        '''Parses the atom list generated in SEWARD.'''
#        print("molcas.output.Output.parse_atom")
#        start = self.find(_re_atom, keys_only=True)[0] + 8
#        stop = self._find_break(start, finds=['****', '--'])
#        atom = self.pandas_dataframe(start, stop, 8)
#        atom.drop([5, 6, 7], axis=1, inplace=True)
#        atom.columns = ['label', 'tag', 'x', 'y', 'z']
#        start = stop = self.find(_re_atom, keys_only=True)[0] + 8
#        while self[stop].split(): stop += 1
#        # Sometimes prints an '--' after the atoms..
#        if self[stop - 1].strip() == '--': stop -= 1
#        columns = ['label', 'tag', 'x', 'y', 'z', 5, 6, 7]
#        atom = self.pandas_dataframe(start, stop, columns).drop([5, 6, 7], axis=1)
#        atom['symbol'] = atom['tag'].str.extract('([A-z]{1,})([0-9]*)',
#                                                 expand=False)[0].str.lower().str.title()
#        atom['Z'] = atom['symbol'].map(symbol_to_z).astype(np.int64)
#        atom['label'] -= 1
#        atom['frame'] = 0
#        self.atom = atom
#
#    def parse_basis_set_order(self):
#        '''
#        Parses the shell ordering scheme if BSSHOW specified in SEWARD.
#        '''
#        print("molcas.output.Output.parse_basis_set_order")
#        start = self.find(_re_bas_order, keys_only=True)[0] + 1
#        stop = self._find_break(start)
#        basis_set_order = self.pandas_dataframe(start, stop, 4)
#        basis_set_order.drop(0, 1, inplace=True)
#        basis_set_order.columns = ['tag', 'type', 'center']
#        shls = self.basis_set.nshells
#        sets = self.atom['set']
#        funcs = self.basis_set.functions_by_shell()
#        self.basis_set_order = _fix_basis_set_order(basis_set_order, shls, sets, funcs)
#
#    def _basis_set_map(self):
#        '''
#        Breaks if there is anything in Contaminant column regarding basis sets.
#        May only work for ANO-RCC basis sets.
#        '''
#        print("molcas.output.Output._basis_set_map")
#        regex = self.regex(_re_bas_names01, _re_bas_dims, _re_bas_names02)
#        names = []
#        for i, (key, val) in enumerate(regex[_re_bas_names01]):
#            try:
#                _, val2 = regex[_re_bas_names02][i]
#            except IndexError: # In case second regex is not found
#                #key2 = key
#                val2 = val
#            try:
#                tmp = val.split(':')[1].split('.')
#                names.append([tmp[0].strip(), tmp[1].strip(), tmp[-2].strip()])
#            except IndexError: # In case first regex is not as expected
#                tmp = val2.split(':')[1].split('.')
#                names.append([tmp[0].strip(), tmp[1].strip(), tmp[-2].strip()])
#        summary = pd.DataFrame(names, columns=('tag', 'name', 'scheme'))
#        sets = []
#        tags = list(summary['tag'].values)
#        for sym, tag in zip(self.atom['symbol'], self.atom['tag']):
#            if sym.upper() in tags:
#                sets.append(tags.index(sym.upper()))
#            elif tag in tags:
#                sets.append(tags.index(tag))
#        self.atom['set'] = sets
#        dim_starts = [i[0] + 1 for i in regex[_re_bas_dims]]
#        dim_stops = [self._find_break(start) for start in dim_starts]
#        basis_map = pd.concat([self._basis_map(start, stop, seht)
#                               for start, stop, seht
#                               in zip(dim_starts, dim_stops, summary.index)])
#        basis_map.columns = ['shell', 'nprim', 'nbasis', 'set', 'spherical']
#        return basis_map
#        start = stop = self.find(_re_bas_order, keys_only=True)[0] + 1
#        while self[stop].strip(): stop += 1
#        df = self.pandas_dataframe(start, stop, ['idx', 'tag', 'type', 'center'])
#        df.drop(['idx', 'tag'], inplace=True, axis=1)
#        if 'set' not in self.atom.columns: self.parse_basis_set()
#        mldict = {'': 0, 'x': 1, 'y': -1, 'z': 0}
#        df['center'] -= 1
#        df['n'] = df['type'].str[0]
#        df['n'].update(df['n'].map({'*': 0}))
#        df['n'] = df['n'].astype(np.int64)
#        fill = df['n'] + 1
#        fill.index += 1
#        df.loc[df[df['n'] == 0].index, 'n'] = fill
#        df['L'] = df['type'].str[1].map(lmap)
#        df['ml'] = df['type'].str[2:]
#        df['ml'].update(df['ml'].map(mldict))
#        df['ml'].update(df['ml'].str[::-1])
#        df['ml'] = df['ml'].astype(np.int64)
#        funcs = self.basis_set.functions_by_shell()
#        shells = []
#        for seht in self.atom['set']:
#            tot = 0
#            lml_count = spher_lml_count
#            for l, n in funcs[seht].items():
#                for i in range(lml_count[l]):
#                    shells += list(range(tot, n + tot))
#                tot += n
#        df['shell'] = shells
#        df['frame'] = 0
#        self.basis_set_order = df
#
#
#    def parse_basis_set(self):
#        '''
#        Parses the primitive exponents, coefficients and shell if BSSHOW specified in SEWARD.
#        '''
#        print("molcas.output.Output.parse_basis_set")
#        basis_map = self._basis_set_map()
#        linenos = [i[0] + 1 for i in self.regex(_re_prims)]
#        lisdx = 0
#        lfsdx = 0
#        basis_set = pd.DataFrame()
#        blocks = []
#        sets = basis_map.groupby('set')
#        for sdx, seht in sets:
#            shfunc = 0
#            lfsdx += len(seht)
#            starts = linenos[lisdx:lfsdx]
#            lisdx = lfsdx
#            prims = []
#            for i, start in enumerate(starts):
#                prim = seht['nprim'].values[i]
#                bas = seht['nbasis'].values[i]
#                chk1 = len(self[start].split())
#                chk2 = len(self[start + 1].split())
#                if chk1 == chk2:
#                    block = self.pandas_dataframe(start, start + prim, bas + 2)
#                else:
#                    block = self[start:start + 2 * prim]
#                    most = block[::2]
#                    extr = block[1::2]
#                    ncols = len(most[0].split()) + len(extr[0].split())
#                    block = pd.read_csv(StringIO('\n'.join([i + j for i, j in zip(most, extr)])),
#                                        delim_whitespace=True, names=range(ncols))
#                alphas = pd.concat([block[1]] * bas).reset_index(drop=True).str.replace('D', 'E').astype(np.float64)
#                coeffs = block[list(range(2, bas + 2))].unstack().reset_index(drop=True)
#                primdf = pd.concat([alphas, coeffs], axis=1)
#                primdf.columns = ['alpha', 'd']
#                primdf['L'] = lorder.index(seht['shell'].values[i])
#                primdf['shell'] = np.repeat(range(shfunc, shfunc + bas), prim)
#                shfunc += bas
#                prims.append(primdf)
#            block = pd.concat(prims)
#            block['set'] = sdx
#            blocks.append(block)
#        basis_set = pd.concat(blocks).reset_index(drop=True)
#        basis_set['frame'] = 0
#        self.basis_set = basis_set
#
#    def __init__(self, *args, **kwargs):
#        print("molcas.output.Output")
#        super().__init__(*args, **kwargs)
#        found = self.find(_re_bas_0, _re_bas_1, _re_bas_2, keys_only=True)
#        bmaps = [i + 1 for i in found[_re_bas_0]]
#        atoms = [i + 2 for i in found[_re_bas_1]]
#        alphs = [i + 1 for i in found[_re_bas_2]]
#        widths = [11, 7, 8, 11, 10, 12]
#        names = _re_bas_0.split()
#        setmap, basmap = {}, []
#        for seht, (start, atst) in enumerate(zip(bmaps, atoms)):
#            stop = start
#            while self[stop].strip(): stop += 1
#            while self[atst].strip():
#                setmap[self[atst].split()[0]] = seht
#                atst += 1
#            basmap.append(pd.read_fwf(StringIO('\n'.join(self[start:stop])),
#                                      widths=widths, header=None, names=names))
#            basmap[-1]['set'] = seht
#        self.atom['set'] = self.atom['tag'].map(setmap)
#        basmap = pd.concat(basmap).reset_index(drop=True)
#        basmap['Shell'] = basmap['Shell'].map(lmap)
#        prims, pset, shell = [], 0, 0
#        for start, seht, L, nprim, nbas in zip(alphs, basmap['set'], basmap['Shell'],
#                                               basmap['nPrim'], basmap['nBasis']):
#            if pset != seht: shell = 0
#            # In case contraction coefficients overflow to next line
#            neat = len(self[start].split()) == len(self[start + 1].split())
#            if neat: block = self.pandas_dataframe(start, start + nprim, nbas + 2)
#            else:
#                stop = start + 2 * nprim
#                most = self[start:stop:2]
#                extr = self[start + 1:stop:2]
#                ncols = len(most[0].split()) + len(extr[0].split())
#                block = pd.read_csv(StringIO('\n'.join([i + j for i, j in zip(most, extr)])),
#                                    delim_whitespace=True, names=range(ncols))
#            alps = (pd.concat([block[1]] * nbas).reset_index(drop=True)
#                    .str.replace('D', 'E').astype(np.float64))
#            ds = block[list(range(2, nbas + 2))].unstack().reset_index(drop=True)
#            pdf = pd.concat([alps, ds], axis=1)
#            pdf.columns = ['alpha', 'd']
#            pdf['L'] = L
#            pdf['shell'] = np.repeat(range(shell, shell + nbas), nprim)
#            pdf['set'] = seht
#            prims.append(pdf)
#            shell += nbas
#            pset = seht
#        prims = pd.concat(prims).reset_index(drop=True)
#        prims['frame'] = 0
#        self.basis_set = prims
#
#    def __init__(self, *args, **kwargs):
#        super(Output, self).__init__(*args, **kwargs)
#
#
#_re_atom = 'Molecular structure info'
#_re_prims = 'No.      Exponent    Contraction Coefficients'
#_orb_slice = [slice(18*i, 18*i + 18) for i in range(4)]
#
#def _fix_basis_set_order(df, shls, sets, funcs):
#    print("molcas.output._fix_basis_set_order")
#    mldict = {'': 0, 'x': 1, 'y': -1, 'z': 0}
#    df['center'] -= 1
#    try:
#        df['n'] = df['type'].str[0].astype(np.int64)
#    except ValueError:
#        ns = list(df['type'].str[0].values)
#        newns = [int(ns[0])]
#        for i, j in zip(ns, ns[1:]):
#            if j == '*':
#                try:
#                    cache = int(i) + 1
#                    newns.append(cache)
#                except ValueError:
#                    newns.append(cache)
#            else:
#                try:
#                    newns.append(int(j))
#                except ValueError:
#                    newns.append(cache)
#        df['n'] = newns
#    df['L'] = df['type'].str[1].map(lmap)
#    df['ml'] = df['type'].str[2:]
#    df['ml'].update(df['ml'].map(mldict))
#    df['ml'].update(df['ml'].str[::-1])
#    df['ml'] = df['ml'].astype(np.int64)
#    shfuncs = []
#    for seht in sets:
#        tot = 0
#        #lml_count = cart_lml_count
#        lml_count = spher_lml_count
#        for l, n in funcs[seht].items():
#            for i in range(lml_count[l]):
#                shfuncs += list(range(tot, n + tot))
#            tot += n
#    df['shell'] = shfuncs
#    df['frame'] = 0
#    return df
#_re_bas_order = 'Basis Label        Type   Center'
#_re_bas_0 = 'Shell  nPrim  nBasis  Cartesian Spherical Contaminant'
#_re_bas_1 = 'Label   Cartesian Coordinates / Bohr'
#_re_bas_2 = 'No.      Exponent    Contraction Coefficients'
#
#
#def parse_molcas(fp, momatrix=None, overlap=None, occvec=None, **kwargs):
#    """
#    Will parse a Molcas output file. Optionally it will attempt
#    to parse additional information obtained from the same directory
#    from specified Orb files or the AO overlap matrix and density matrix.
#    If density keyword is specified, the momatrix keyword is ignored.
#
#    Args
#        fp (str): Path to output file
#        momatrix (str): file name of the C matrix of interest
#        overlap (str): file name of the overlap matrix
#        occvec (str): an occupation vector
#
#    Returns
#        parsed (Editor): contains many attributes similar to the
#            exatomic universe
#    """
#    print("molcas.output.parse_molcas")
#    uni = Output(fp, **kwargs)
#    adir = os.sep.join(fp.split(os.sep)[:-1])
#    if momatrix is not None:
#        fp = os.sep.join([adir, momatrix])
#        if os.path.isfile(fp):
#            orb = Orb(fp)
#            uni.momatrix = orb.momatrix
#            uni.occupation_vector = orb.occupation_vector
#            occvec = occvec if occvec is not None else orb.occupation_vector
#            d = DensityMatrix.from_momatrix(orb.momatrix, occvec)
#            uni.density = d
#        else:
#            print('Is {} in the same directory as {}?'.format(momatrix, fp))
#    if overlap is not None:
#        fp = os.sep.join([adir, overlap])
#        if os.path.isfile(fp): uni.overlap = Overlap.from_file(fp)
#        else: print('Is {} in the same directory as {}?'.format(overlap, fp))
#    return uni
=======
"""
Molcas Output Parser
#####################
Multiple frames are not currently supported
"""
import os
import pandas as pd
import numpy as np
from io import StringIO

from .editor import Editor

from exatomic.core.basis import Overlap, lmap, rlmap, spher_lml_count
from exatomic.core.orbital import DensityMatrix
from exatomic.base import sym2z


class Orb(Editor):
    def to_universe(self):
        raise NotImplementedError("No atom information given. " \
                                  "Attach these attributes to a universe.")

    def _one_el(self, starts, step, ncol):
        func = pd.read_csv
        kwargs = {'header': None}
        if ncol == 1:
            func = pd.read_fwf
            kwargs['widths'] = [18] * 4
        else:
            kwargs['delim_whitespace'] = True
        return [func(StringIO('\n'.join(self[start:start + step])),
                     **kwargs).stack().values for start in starts]

    def parse_momatrix(self):
        dim = int(self[5])
        ndim = dim * dim
        found = self.find(_re_orb, _re_occ,
                          _re_ens, keys_only=True)
        skips = found[_re_orb]
        start = skips[0]
        occs = [i + 1 for i in found[_re_occ]]
        ens = [i + 1 for i in found[_re_ens]]
        if not found[_re_ens]: ens = False
        ncol = len(self[start + 1].split())
        cols = 4 if ncol == 1 else ncol
        chnk = np.ceil(dim / cols).astype(np.int64)
        orbdx = np.repeat(range(dim), chnk)
        if len(occs) == 2:
            skips.insert(dim, skips[dim] - 1)
            orbdx = np.concatenate([orbdx, orbdx])
        skips = [i - skips[0] for i in skips]
        if ncol == 1:
            coefs = pd.read_fwf(StringIO('\n'.join(self[start:occs[0]-2])),
                                skiprows=skips, header=None, widths=[18]*4)
            if ens: ens = self._one_el(ens, chnk, ncol)
        else:
            coefs = self.pandas_dataframe(start, occs[0]-2, ncol,
                                          **{'skiprows': skips})
            if ens:
                echnk = np.ceil(dim / len(self[ens[0] + 1].split())).astype(np.int64)
                ens = self._one_el(ens, echnk, ncol)
        occs = self._one_el(occs, chnk, ncol)
        coefs['idx'] = orbdx
        coefs = coefs.groupby('idx').apply(pd.DataFrame.stack).drop(
                                           'idx', level=2).values
        mo = {'orbital': np.repeat(range(dim), dim), 'frame': 0,
              'chi': np.tile(range(dim), dim)}
        if ens:
            orb = {'frame': 0, 'group': 0}
        if len(occs) == 2:
            mo['coef'] = coefs[:len(coefs)//2]
            mo['coef1'] = coefs[len(coefs)//2:]
            self.occupation_vector = {'coef': occs[0], 'coef1': occs[1]}
            if ens:
                orb['occupation'] = np.concatenate(occs)
                orb['energy'] = np.concatenate(ens)
                orb['vector'] = np.concatenate([range(dim), range(dim)])
                orb['spin'] = np.concatenate([np.zeros(dim), np.ones(dim)])
        else:
            mo['coef'] = coefs
            self.occupation_vector = occs[0]
            if ens:
                orb['occupation'] = occs[0]
                orb['energy'] = ens[0]
                orb['vector'] = range(dim)
                orb['spin'] = np.zeros(dim)
        self.momatrix = pd.DataFrame.from_dict(mo)
        if ens:
            self.orbital = pd.DataFrame.from_dict(orb)

    def __init__(self, *args, **kwargs):
        super(Orb, self).__init__(*args, **kwargs)


_re_orb = 'ORBITAL'
_re_occ = 'OCCUPATION NUMBERS'
_re_ens = 'ONE ELECTRON ENERGIES'


class Output(Editor):

    def parse_atom(self):
        """Parses the atom list generated in SEWARD."""
        start = stop = self.find(_re_atom, keys_only=True)[0] + 8
        while self[stop].split(): stop += 1
        # Sometimes prints an '--' after the atoms..
        if self[stop - 1].strip() == '--': stop -= 1
        columns = ['label', 'tag', 'x', 'y', 'z', 5, 6, 7]
        atom = self.pandas_dataframe(start, stop, columns).drop([5, 6, 7], axis=1)
        atom['symbol'] = atom['tag'].str.extract('([A-z]{1,})([0-9]*)',
                                                 expand=False)[0].str.lower().str.title()
        atom['Z'] = atom['symbol'].map(sym2z).astype(np.int64)
        atom['label'] -= 1
        atom['frame'] = 0
        self.atom = atom

    def parse_basis_set_order(self):
        """
        Parses the shell ordering scheme if BSSHOW specified in SEWARD.
        """
        start = stop = self.find(_re_bas_order, keys_only=True)[0] + 1
        while self[stop].strip(): stop += 1
        df = self.pandas_dataframe(start, stop, ['idx', 'tag', 'type', 'center'])
        df.drop(['idx', 'tag'], inplace=True, axis=1)
        if 'set' not in self.atom.columns: self.parse_basis_set()
        mldict = {'': 0, 'x': 1, 'y': -1, 'z': 0}
        df['center'] -= 1
        df['n'] = df['type'].str[0]
        df['n'].update(df['n'].map({'*': 0}))
        df['n'] = df['n'].astype(np.int64)
        fill = df['n'] + 1
        fill.index += 1
        df.loc[df[df['n'] == 0].index, 'n'] = fill
        df['L'] = df['type'].str[1].map(lmap)
        df['ml'] = df['type'].str[2:]
        df['ml'].update(df['ml'].map(mldict))
        df['ml'].update(df['ml'].str[::-1])
        df['ml'] = df['ml'].astype(np.int64)
        funcs = self.basis_set.functions_by_shell()
        shells = []
        for seht in self.atom['set']:
            tot = 0
            lml_count = spher_lml_count
            for l, n in funcs[seht].items():
                for i in range(lml_count[l]):
                    shells += list(range(tot, n + tot))
                tot += n
        df['shell'] = shells
        df['frame'] = 0
        self.basis_set_order = df


    def parse_basis_set(self):
        """
        Parses the primitive exponents, coefficients and shell if BSSHOW specified in SEWARD.
        """
        found = self.find(_re_bas_0, _re_bas_1, _re_bas_2, keys_only=True)
        bmaps = [i + 1 for i in found[_re_bas_0]]
        atoms = [i + 2 for i in found[_re_bas_1]]
        alphs = [i + 1 for i in found[_re_bas_2]]
        widths = [11, 7, 8, 11, 10, 12]
        names = _re_bas_0.split()
        setmap, basmap = {}, []
        for seht, (start, atst) in enumerate(zip(bmaps, atoms)):
            stop = start
            while self[stop].strip(): stop += 1
            while self[atst].strip():
                setmap[self[atst].split()[0]] = seht
                atst += 1
            basmap.append(pd.read_fwf(StringIO('\n'.join(self[start:stop])),
                                      widths=widths, header=None, names=names))
            basmap[-1]['set'] = seht
        self.atom['set'] = self.atom['tag'].map(setmap)
        basmap = pd.concat(basmap).reset_index(drop=True)
        basmap['Shell'] = basmap['Shell'].map(lmap)
        prims, pset, shell = [], 0, 0
        for start, seht, L, nprim, nbas in zip(alphs, basmap['set'], basmap['Shell'],
                                               basmap['nPrim'], basmap['nBasis']):
            if pset != seht: shell = 0
            # In case contraction coefficients overflow to next line
            neat = len(self[start].split()) == len(self[start + 1].split())
            if neat: block = self.pandas_dataframe(start, start + nprim, nbas + 2)
            else:
                stop = start + 2 * nprim
                most = self[start:stop:2]
                extr = self[start + 1:stop:2]
                ncols = len(most[0].split()) + len(extr[0].split())
                block = pd.read_csv(StringIO('\n'.join([i + j for i, j in zip(most, extr)])),
                                    delim_whitespace=True, names=range(ncols))
            alps = (pd.concat([block[1]] * nbas).reset_index(drop=True)
                    .str.replace('D', 'E').astype(np.float64))
            ds = block[list(range(2, nbas + 2))].unstack().reset_index(drop=True)
            pdf = pd.concat([alps, ds], axis=1)
            pdf.columns = ['alpha', 'd']
            pdf['L'] = L
            pdf['shell'] = np.repeat(range(shell, shell + nbas), nprim)
            pdf['set'] = seht
            prims.append(pdf)
            shell += nbas
            pset = seht
        prims = pd.concat(prims).reset_index(drop=True)
        prims['frame'] = 0
        self.basis_set = prims

    def __init__(self, *args, **kwargs):
        super(Output, self).__init__(*args, **kwargs)


_re_atom = 'Molecular structure info'
_re_bas_order = 'Basis Label        Type   Center'
_re_bas_0 = 'Shell  nPrim  nBasis  Cartesian Spherical Contaminant'
_re_bas_1 = 'Label   Cartesian Coordinates / Bohr'
_re_bas_2 = 'No.      Exponent    Contraction Coefficients'


def parse_molcas(fp, momatrix=None, overlap=None, occvec=None, **kwargs):
    """
    Will parse a Molcas output file. Optionally it will attempt
    to parse additional information obtained from the same directory
    from specified Orb files or the AO overlap matrix and density matrix.
    If density keyword is specified, the momatrix keyword is ignored.

    Args
        fp (str): Path to output file
        momatrix (str): file name of the C matrix of interest
        overlap (str): file name of the overlap matrix
        occvec (str): an occupation vector

    Returns
        parsed (Editor): contains many attributes similar to the
            exatomic universe
    """
    uni = Output(fp, **kwargs)
    adir = os.sep.join(fp.split(os.sep)[:-1])
    if momatrix is not None:
        fp = os.sep.join([adir, momatrix])
        if os.path.isfile(fp):
            orb = Orb(fp)
            uni.momatrix = orb.momatrix
            uni.occupation_vector = orb.occupation_vector
            occvec = occvec if occvec is not None else orb.occupation_vector
            d = DensityMatrix.from_momatrix(orb.momatrix, occvec)
            uni.density = d
        else:
            print('Is {} in the same directory as {}?'.format(momatrix, fp))
    if overlap is not None:
        fp = os.sep.join([adir, overlap])
        if os.path.isfile(fp): uni.overlap = Overlap.from_file(fp)
        else: print('Is {} in the same directory as {}?'.format(overlap, fp))
    return uni
>>>>>>> 1c37655b6be3dca60b2adbeee8ca3767e5477943
