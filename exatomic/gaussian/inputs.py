# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Gaussian Input Generator
###########################
Editor class and helper function for writing input files.
"""
#
#import os
#import numpy as np
#from .editor import Editor
#from exatomic import __version__
#
#_template = """\
#{link0}
#{route}
#
#{title}
#
#{charge} {mult}
#{atom}
#
#{basis}{ecp}{options}
#
#"""
#
#class Input(Editor):
#
#    @classmethod
#    def from_universe(cls, uni, link0='', route='#P HF/6-31G(d)', title='', name='',
#                      charge=0, mult=1, basis='', ecp='', options='', writedir=None):
#        """
#        Generate an input Editor from a universe. Arguments can either be strings
#        or iterables of key, value pairs (dict, list, tuple) and/or just strings.
#        """
#        kwargs = {}
#        kwargs['mult'] = mult
#        kwargs['charge'] = charge
#        kwargs['atom'] = uni.atom.to_xyz()[:-1]
#        kwargs['link0'] = _handle_args('link0', link0)
#        kwargs['route'] = _handle_args('route', route)
#        kwargs['basis'] = _handle_args('basis', basis)
#        kwargs['ecp'] = _handle_args('ecp', ecp)
#        kwargs['options'] = options
#        if name and not title: title = name
#        elif title and not name: name = title + '.g09'
#        kwargs['title'] = '{} -- generated by exatomic.v{}'.format(
#                                                title, __version__)
#        fl = cls(_template)
#        fl.name = name
#        fl.format(inplace=True, **kwargs)
#        if writedir:
#            if (not name and not title):
#                print('Must supply name or title to write input file.')
#            else:
#                if not writedir.endswith(os.sep):
#                    writedir += os.sep
#                fl.write(writedir + fl.name)
#        return fl
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#
#
#def _handle_args(kwarg, args):
#    if isinstance(args, str): return args
#    if isinstance(args, dict): args = args.items()
#    clean = []
#    for arg in args:
#        try:
#            k, v = arg
#            clean.append((k, v))
#        except ValueError:
#            clean.append((str(arg), ''))
#    if kwarg == 'link0':
#        return ''.join([''.join(['%', key, '=', str(arg), '\n'])
#                       for key, arg in clean])[:-1]
#    elif kwarg == 'route':
#        return ''.join(['#P '] + [''.join([key, '(', arg, ') '])
#                       if arg else key + ' ' for key, arg in clean])
#    elif kwarg == 'basis':
#        return ''.join([''.join([key, '   0\n', arg, '\n****\n'])
#                       if arg else key + '\n\n' for key, arg in clean])
#    elif kwarg == 'ecp':
#        return ''.join([''.join([key, '   0\n', arg, '\n'])
#                       for key, arg in clean])
#    else:
#        raise NotImplementedError('{} keyword is not currently '
#                                  'supported'.format(key))
#
#
#def tuning_inputs(uni, name, mult, charge, basis, gammas, alphas,
#                  route=[('Pop', 'full')], link0=None, nproc=4, mem=4,
#                  field=None, writedir=None, deep=False):
#    """
#    Provided a universe, generate input files for functional tuning.
#    Includes input keywords for orbital visualization within exatomic.
#    Assumes you will copy restart checkpoint files to have the same
#    names as the input files.
#
#    Args
#        uni (exatomic.container.Universe): molecular specification
#        name (str): prefix for job names
#        mult (int): spin multiplicity
#        charge (int): charge of the system
#        basis (list): tuples of atomic symbol, string of basis name
#        gammas (iter): values of range separation parameter (omega)
#        alphas (iter): fractions of Hartree-Fock in the short range
#        route (list): strings or tuples of keyword, value pairs
#        link0 (list): strings or tuples of keyword, value pairs
#        nproc (int): number of processors
#        mem (int): memory (in GB)
#        writedir (str): directory path to write input files
#
#    Returns
#        editors (list): input files as exa.Editors
#    """
#    inuni = set(uni.atom.unique_atoms)
#    try:
#        inbas = set([atom for atom, bas in basis])
#        if inuni != inbas:
#            print("Warning: specific basis sets not the same as atom types")
#    except:
#        print("Warning: did not validate basis sets against atoms in universe")
#    rangedt = """
#IOP(3/107={w}00000)
#IOP(3/108={w}00000)
#IOP(3/130={a})
#IOP(3/131={a})
#IOP(3/119={b}00000)
#IOP(3/120={b}00000)"""
#    globalt = """
#IOP(3/76={b}{a})"""
#    # Make the obtuse strings that Gaussian requires
#    gammas = [str(int(np.round(g * 10000, decimals=4))).zfill(5) for g in gammas]
#    alphas = [str(int(np.round(a * 10000, decimals=4))).zfill(5) for a in alphas]
#    betas = [str(10000 - int(a)).zfill(5) for a in alphas]
#    # A systematic input file naming scheme
#    chgnms = ['cat', 'neut', 'an']
#    # Auxiliary job information
#    chgs = [charge + 1, charge, charge - 1]
#    mults = [2, 1, 2] if mult == 1 else [mult - 1, mult, mult + 1]
#    # Some recommended default keywords for Gaussian DFT jobs
#    route_opts = [('LC-PBEPBE/Genecp', ''),
#                  ('gfinput', ''),
#                  ('Guess', 'read'),
#                  ('IOP(3/75=5)', '')]
#    link_opts = [('NProc', nproc), ('Mem', str(mem) + 'gb')]
#    editors = []
#    for gamma in gammas:
#        for alpha, beta in zip(alphas, betas):
#            for chgnm, chg, mult in zip(chgnms, chgs, mults):
#                ndecgam = max(len(str(int(gamma) / 10000)) - 2, 2)
#                ndecalp = max(len(str(int(alpha) / 10000)) - 2, 2)
#                gam = ('{:.' + str(ndecgam) + 'f}').format(int(gamma) / 10000)
#                alp = ('{:.' + str(ndecalp) + 'f}').format(int(alpha) / 10000)
#                jobname = '-'.join([name, gam, alp, chgnm])
#                this_link = [('chk', jobname + '.chk')]
#                if np.isclose(int(gamma), 0):
#                    this_route = [globalt.format(a=alpha, b=beta)]
#                else:
#                    this_route = [rangedt.format(w=gamma, a=alpha, b=beta)]
#                opts = {'charge': chg, 'mult': mult, 'basis': basis,
#                        'title': jobname, 'writedir': writedir}
#                if field is not None:
#                    opts['postatom'] = field
#                    this_route += ['Charge']
#                if isinstance(route, list):
#                    opts['route'] = route_opts + route + this_route
#                else:
#                    opts['route'] = route_opts + this_route
#                if isinstance(link0, list):
#                    opts['link0'] = link_opts + link0 + this_link
#                else:
#                    opts['link0'] = link_opts + this_link
#                editors.append(Input.from_universe(uni, **opts))
#    return editors
#
#
#def functional_inputs(uni, name, mult, charge, basis,
#                      funcnames={'pbe': 'PBEPBE'}, nproc=4, mem=4,
#                      field=None, writedir=None):
#    """
#    Provided a universe, generate input files to analyze the
#    delocalization error inherent in functionals defined in funcnames.
#    Includes input keywords for orbital visualization within exatomic.
#    Assumes you will copy restart checkpoint files to have the same
#    names as the input files.
#
#    Args
#        uni (exatomic.container.Universe): molecular specification
#        name (str): prefix for job names
#        mult (int): spin multiplicity
#        charge (int): charge of the system
#        basis (list): tuples of atomic symbol, string of basis name
#        gammas (iter): values of range separation parameter (omega)
#        alphas (iter): fractions of Hartree-Fock in the short range
#        route (list): strings or tuples of keyword, value pairs
#        link0 (list): strings or tuples of keyword, value pairs
#        nproc (int): number of processors
#        mem (int): memory (in GB)
#        writedir (str): directory path to write input files
#
#    Returns
#        editors (list): input files as exa.Editors
#    """
#    editors = []
#    link_opts = [('NProc', nproc), ('Mem', mem)]
#    chgnms = ['cat', 'neut', 'an']
#    chgs = [charge + 1, charge, charge - 1]
#    mults = [2, 1, 2] if mult == 1 else [mult - 1, mult, mult + 1]
#    for func in funcnames:
#        route_opts = [funcnames[func] + '/Genecp', 'gfinput', ('Guess', 'read'),
#                      'IOP(3/75=5)', ('Pop', 'full')]
#        for chgnm, chg, mul in zip(chgnms, chgs, mults):
#            jobname = '-'.join([chgnm, chg, mul])
#            this_link = [('chk', jobname + '.chk')]
#            field = field if field is not None else ''
#            this_route = ['Charge'] if field else []
#            opts = {'title': jobname, 'mult': mul, 'charge': chg,
#                    'link0': link_opts + this_link,
#                    'route': route_opts + this_route,
#                    'writedir': writedir, 'postatom': field,
#                    'basis': basis}
#            editors.append(Input.from_universe(uni, **args))
#    return editors
#
#
