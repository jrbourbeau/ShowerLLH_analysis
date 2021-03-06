#!/usr/bin/env python

##############################################################################
# Load essential information for simulation analysis
##############################################################################


import numpy as np
import time
import glob
import re

from llhtools import inPoly
import myGlobals as my


def load_sim(config='IT73', bintype='logdist'):

    # Load simulation information
    my.setupShowerLLH(verbose=False)
    infile = '{}/{}_sim/SimPlot_{}.npy'.format(my.llh_data, config, bintype)

    s = {}

    t0 = time.time()
    print('Working on {}...'.format(infile))
    s = np.load(infile)
    s = s.item()
    print('Time taken to load: {}'.format(time.time() - t0))

    # Set array types
    bools = []
    bools += ['LoudestOnEdge']
    for cut in bools:
        s[cut] = s[cut].astype('bool')

    ## Quality Cuts ##
    c = {}

    # Adapted versions of Bakhtiyar's cuts
    c['llh1'] = np.logical_not(np.isnan(s['ML_energy']))
    c['llh2'] = (np.cos(np.pi - s['zenith']) >= 0.8)
    c['llh3'] = inPoly(s['ML_x'], s['ML_y'], 0)
    c['llh4'] = np.logical_not(s['LoudestOnEdge'])
    c['llh5'] = (np.nan_to_num(s['Q1']) >= 6)
    # Final versions of cuts for testing
    c['llh'] = c['llh1'] * c['llh2'] * c['llh3'] * c['llh4'] * c['llh5']
    s['cuts'] = c

    ## Load MC information ##
    print('Loading MC information...')
    s['MC'] = np.load('{}/{}_sim/SimPlot_MC.npy'.format(my.llh_data, config))
    s['MC'] = s['MC'].item()

    compList = s['MC'].keys()
    s['MC']['joint'] = {}
    shape = s['MC']['P']['low'].shape
    for key in ['low', 'mid', 'high']:
        s['MC']['joint'][key] = np.zeros(shape, dtype=int)
        s['MC']['joint'][key] = np.sum([s['MC'][comp][key]
                                        for comp in compList], axis=0)

    return s


def print_cut_eff(config='IT73', bintype='standard'):
    s = load_sim(config, bintype)
    n_total = float(len(s['eventID']))
    cut_eff = {}
    for i in range(1,6):
        cut = 'llh{}'.format(i)
        cut_eff[cut] = len(s['eventID'][s['cuts'][cut]])/n_total
    for key in cut_eff:
        print('{} = {}'.format(key, cut_eff[key]))



if __name__ == "__main__":

    s = load_sim()
