#!/usr/bin/env python

#=========================================================================
# File Name     : spectrum.py
# Description   :
# Creation Date : 05-25-2016
# Created By    : James Bourbeau
#=========================================================================

import numpy as np
import matplotlib.pyplot as plt
import argparse

from ShowerLLH_scripts.analysis.load_sim import load_sim
from ShowerLLH_scripts.support_functions.checkdir import checkdir

if __name__ == "__main__":

    llhreco = load_sim(config='IT73', bintype='standard')

    # Caluclate cuts to be made
    llhcuts = llhreco['cuts']['llh']
    # E_min, E_max = 6.5, 6.75
    log_energy = llhreco['ML_energy'][llhcuts]*1e9
    print(log_energy)
    # energycuts = (log_energy > E_min) * (log_energy < E_max)
    # protoncuts = llhcuts * energycuts * (llhreco['comp'] == 'P')
    # ironcuts = llhcuts * energycuts * (llhreco['comp'] == 'Fe')
    # heliumcuts = llhcuts * energycuts * (llhreco['comp'] == 'He')
    # oxygencuts = llhcuts * energycuts * (llhreco['comp'] == 'O')

    # Plotting
    llhbins = np.logspace(9, 21, 100)
    n, bins, patches = plt.hist(
        log_energy, bins=llhbins, histtype='step', alpha=0.75)
    # plt.xlim([-6, 6])
    plt.xlabel('Energy (eV)')
    plt.ylabel('Counts')
    plt.xscale('log')
    plt.title('ShowerLLH - IT73 - standard LLH bins')
    outfile = '/home/jbourbeau/public_html/figures/showerLLHstudy/comp/spectrum.png'
    checkdir(outfile)
    plt.savefig(outfile)
    plt.close()
