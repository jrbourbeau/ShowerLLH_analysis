#!/usr/bin/env python

#=========================================================================
# File Name     : comp.py
# Description   : Comparison of LLH composition values
# Creation Date : 05-13-2016
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
    E_min, E_max = 6.5, 6.75
    log_energy = np.log10(llhreco['MC_energy'])
    energycuts = (log_energy > E_min) * (log_energy < E_max)
    protoncuts = llhcuts * energycuts * (llhreco['comp'] == 'P')
    ironcuts = llhcuts * energycuts * (llhreco['comp'] == 'Fe')
    heliumcuts = llhcuts * energycuts * (llhreco['comp'] == 'He')
    oxygencuts = llhcuts * energycuts * (llhreco['comp'] == 'O')

    # Calcuate LLH ratio with cuts implemented
    protonLLHdiff = (llhreco['fLLH'] - llhreco['pLLH'])[protoncuts]
    ironLLHdiff = (llhreco['fLLH'] - llhreco['pLLH'])[ironcuts]
    heliumLLHdiff = (llhreco['fLLH'] - llhreco['pLLH'])[heliumcuts]
    oxygenLLHdiff = (llhreco['fLLH'] - llhreco['pLLH'])[oxygencuts]

    # Plotting
    colordict = {'P': '#007acc', 'Fe': '#fc4f30', 'He':'#e5ae38', 'O':'#6d904f'}
    LLHdiffdict = {'P': protonLLHdiff, 'Fe': ironLLHdiff, 'He':heliumLLHdiff, 'O':oxygenLLHdiff}
    llhbins = np.linspace(-5, 5, 100)
    for comp in ['P', 'He', 'O', 'Fe']:
        n, bins, patches = plt.hist(
            LLHdiffdict[comp], bins=llhbins, histtype='step', alpha=0.75, color=colordict[comp], label=comp)
    # n, bins, patches = plt.hist(
    # ironLLHdiff, bins=llhbins, histtype='step', alpha=0.75,
    # color=colorDict['Fe'])
    plt.legend()
    plt.xlim([-6, 6])
    plt.xlabel(
        'Log-Likelihood Difference ($f_{\mathrm{LLH}}-p_{\mathrm{LLH}}$)')
    plt.ylabel('Counts')
    plt.title(r'ShowerLLH - IT73 - standard LLH bins')
    outfile = '/home/jbourbeau/public_html/figures/showerLLHstudy/comp/comp.png'
    checkdir(outfile)
    plt.savefig(outfile)
    plt.close()
