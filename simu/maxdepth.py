# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 14:53:54 2018

@author: sylvain.finot
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib
matplotlib.rcParams.update({'font.size': 14})
from scipy.optimize import curve_fit
import logging
#import csv
#shift_is_held = False
logger = logging.getLogger(__name__)
def find(data, percent=99):
    idx = np.argmax(np.cumsum(data[:,1])>percent)
    return data[idx]

def func(x,a,b):
        return a * x**b
def fit(X,Y):
    popt, pcov = curve_fit(func, X, Y)
    return popt, pcov

def plot(percent=99):
    data = []
    maxdepth = []
    energies = []
    for i in range(11):
        data.append(np.loadtxt(str(10+2*i)+"kev.dat",skiprows=2,delimiter='\t'))
        energies.append(10+2*i)
        maxdepth.append(find(data[i],percent))
    
#    f = plt.figure()
#    ax = f.add_subplot(211)
#    bx = f.add_subplot(212,sharex=ax)
    f ,(ax,bx) = plt.subplots(2,1, gridspec_kw = {'height_ratios':[2, 1]})
    ax.get_shared_x_axes().join(ax, bx)
    for i in range(len(data)):
        ax.plot(data[i][:,0],np.cumsum(data[i][:,1]),label=str(energies[i])+'keV')
        
    majorLocator = MultipleLocator(1000)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(100)
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.set_minor_locator(minorLocator)
    bx.xaxis.set_major_locator(majorLocator)
    bx.xaxis.set_major_formatter(majorFormatter)
    bx.xaxis.set_minor_locator(minorLocator)
    ax.legend()
    ax.set_xlabel('Depth (nm)')
    ax.set_ylabel('Cummulated intensity (%)')
    ax.hlines(y=percent,xmin=-100,xmax=6000)
    para, cov = fit(np.array(maxdepth)[:,0],energies)
    para = np.round(para,3)
    residuals = energies - func(np.array(np.array(maxdepth)[:,0]),para[0],para[1])
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((energies-np.mean(energies))**2)
    r_squared = 1 - (ss_res / ss_tot)
    bx.plot(np.array(maxdepth)[:,0],energies,'.', c='black', markeredgecolor='none')
    bx.plot(np.array(maxdepth)[:,0],func(np.array(np.array(maxdepth)[:,0]),para[0],para[1]),label='$E_{max}[keV]=%.3f\ (L[nm])^{%.3f}$\n$R^2=%.5f$'%(para[0],para[1],r_squared))
    bx.set_xlabel('Depth (nm)')
    bx.set_ylabel('Energy (keV) for %s'%(str(percent)+'%'))
    bx.set_xlim(-100,max(np.array(maxdepth)[:,0])+1000)
    bx.legend()
    f.set_size_inches(19.20,10.80)
    f.tight_layout()
#    f.savefig('maxdepth.png',dpi=300)

plot(99)
#with open('maxdepth'+str(percent)+'.csv', 'w') as csvfile:
#    writer = csv.writer(csvfile, delimiter='\t')
#    for i in range(len(energies)):
#        writer.writerow([energies[i],np.array(maxdepth)[:,0][i]])
