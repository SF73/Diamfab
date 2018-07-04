# -*- coding: utf-8 -*-
"""
Created on Thu May 31 15:44:04 2018

@author: sylvain.finot
"""

#import statsmodels.api as sm
from scipy.optimize import curve_fit
import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
from Subfunctions import importData


#def fit(data,interval):
#    nData = data[(data[:,0] > interval[0])&(data[:,0] < interval[1])]
#    #sm.OLS(Y,X)
#    X = nData[:,0]
#    Y = nData[:,1]
##    X = sm.add_constant(X)
#    res_ols = sm.OLS(X, Y).fit()
##    print(res_ols.summary())  
#    return np.array([res_ols.params[0], res_ols.bse[0]])
##    return np.polyfit(nData[:,0],nData[:,1],1,cov=True)

def fit2(data,interval):
    nData = data[(data[:,0] > interval[0])&(data[:,0] < interval[1])]
    X = nData[:,0]
    Y = nData[:,1]
    def func(x, a):
        return (1/a) * x
    popt, pcov = curve_fit(func, X, Y)
    return np.array([popt[0], np.sqrt(pcov[0])])

def calibrate(plot=False,omnes=3.5E16):
    data = importData('res/Calibration.csv')
    params = fit2(data,[0,2E17])
#    fit2(data,[0,3E17])
    if plot:
#        fig = plt.Figure()
        ax = plt.subplot(111)
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.plot(data[:,0] ,data[:,1], '.', c='black', markeredgecolor='none')
        x = np.logspace(np.log10(min(data[:,0]))-1,np.log10(max(data[:,0])),20)
        ax.plot(x,x/params[0],label='Regression [B] =%.1e ' %params[0]+'$\pm$ %.1e'%params[1] +'r')
        ax.plot(x,x/(omnes),label='Omnes [B]=%.1e' %omnes+'r')
        ax.plot(x,x/(params[0]+1.96*params[1]),c='gray',linestyle='--')
        ax.plot(x,x/(params[0]-1.96*params[1]),c='gray',linestyle='--')
        ax.legend()
        plt.ylabel('r=$\dfrac{I_{BETO}}{I_{FETO}}$')
        plt.xlabel('Boron concentration (cm$^{-3}$)')
    return params