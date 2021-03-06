# -*- coding: utf-8 -*-
"""
Created on Thu May 31 15:44:04 2018

@author: sylvain.finot
"""

from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import scipy.odr.odrpack as odrpack
from collections import Counter
import itertools

def fit(data,interval):
    interval.sort()
    nData = data[(data[:,0] > interval[0])&(data[:,0] < interval[1])]
    X = nData[:,0]
    Y = nData[:,1]
    def func(x, a):
        return (1/a) * x
    popt, pcov = curve_fit(func, X, Y)#,absolute_sigma=True,sigma=0.1*Y)
    return np.array([popt[0], np.sqrt(pcov[0])])

def fit2(data,interval,init):
    interval.sort()
    nData = data[(data[:,0] > interval[0])&(data[:,0] < interval[1])]
    x=nData[:,0]
    y=nData[:,1]
    sx=None
    sy=None
    try:
        sx = nData[:,2]
        sy = nData[:,3]
    except:
        pass
    def func(B,x):
        return (1/B[0]) * x
    linear = odrpack.Model(func)
    mydata = odrpack.RealData(x, y, sx=sx, sy=sy)
    myodr = odrpack.ODR(mydata, linear, beta0=[init])
    myoutput = myodr.run()
    myoutput.pprint()
    return [myoutput.beta[0],myoutput.sd_beta[0]]

def calibrate(plot=False,temp=5,omnes=3.5E16,lim=[0,5E17]):
    markers = itertools.cycle(["o","s",'h','H',"D",'8'])
    data = np.loadtxt('res/Calibration%sK'%(temp),skiprows=1,dtype=np.str)
    method=np.array(list(map(str.upper,data[:,0])))
    methods = list(Counter(map(str.upper, data[:,0])))
    data = data[:,1:].astype(np.float64)
    params = fit(data,lim)
    print('Initial guess\t%.2e\nStd\t%.2e'%(params[0],params[1]))
    params = fit2(data,lim,init=params[0])
    params[1] *= 1.96
    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_yscale('log')
        ax.set_xscale('log')
#        ax.text(1, 1, 'matplotlib', horizontalalignment='right', verticalalignment='center', transform=ax.transAxes)
#        plt.annotate('Something', xy=(0.05, 0.95), xycoords='figure fraction')
        ax.set_title('T=%dK'%(temp))
        x = np.logspace(np.log10(min(data[:,0]))-1,np.log10(max(data[:,0])),20)
        ax.plot(x,x/params[0],c='r',label='Regression [B] = (%.1e ' %params[0]+'$\pm$ %.1e)'%params[1] +'r')
#        ax.plot(x,x/(omnes),label='Omnes [B]=%.1e' %omnes+'r')
        ax.axvline(x=lim[0],c='k',alpha=0.7)
        ax.axvline(x=lim[1],c='k',alpha=0.7)
        ax.plot(x,x/(params[0]+params[1]),c='gray',linestyle='--')
        ax.plot(x,x/(params[0]-params[1]),c='gray',linestyle='--')
        ax.fill_between(x, x/(params[0]+params[1]), x/(params[0]-params[1]), alpha=.25, label='1.96-sigma interval')
        for m in methods:
            cdata = data[method==m].astype(np.float64)
            x=cdata[:,0]
            y=cdata[:,1]
            sx=0
            sy=0
            try:
                sx = cdata[:,2]
                sy = cdata[:,3]
            except:
                pass
            ax.errorbar(x, y, xerr=sx, yerr=sy, linestyle='None',marker=next(markers),markersize=5,label=m)
        ax.legend()
        ax.set_ylabel('r=$\dfrac{I_{BETO}}{I_{FETO}}$')
        ax.set_xlabel('Boron concentration (cm$^{-3}$)')
        fig.show()
    return params