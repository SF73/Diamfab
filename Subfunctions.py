# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 09:40:09 2018

@author: sylvain.finot
"""

import scipy.constants as cst
import numpy as np
from scipy.signal import butter, lfilter, freqz,filtfilt
import ast
import logging
logger = logging.getLogger(__name__)
eV_To_nm = cst.c*cst.h/cst.e*1E9

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b,a,data)#lfilter(b, a, data)
    return y

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def nmFromEV(E):
        return eV_To_nm/E
    
def importData(path):
#    content =  np.loadtxt(path, delimiter='\t' ,dtype=np.str)
#    content = np.char.replace(content, ',', '.').astype(np.float64)[:,:2]
    content = np.genfromtxt(path,delimiter='\t')
    content = content[~np.isnan(content).any(axis=1)]
    return content

def strToTable(txt):
    from io import StringIO
    c = StringIO(txt)
    return np.loadtxt(c,delimiter='\t',dtype=np.str)
def Boron(peaks,noise=[0,0],params=np.array([3.5E16,0])):
    """
    peaks tableau de peak [x (eV),y (coup)]
    noise : [mean,std]
    param : [best, std]
    """
    try:
        p = np.asarray(peaks)
        p=p[np.argsort(p[:,0])]
        a,da = params[0],params[1]
        n,dn = noise[0],noise[1]
        IBETO = p[0][1]
        IFETO = p[1][1]
        r = ((IBETO-n)/(IFETO-n))
        dr = dn*r/(IFETO-n)
        incertitude = np.sqrt((a*dr)**2+(da*r)**2)
        logger.debug("Ratio : %.4f +- %.4f"%(r,dr))
#        logger.info("Boron : %.2e"%(r*params))
        return [r*a,incertitude], [r,dr]
    except:
        logger.exception("Can't calculate BORON")
        return [-1,-1],[-1,-1]

def find_max(data, interval):
    """
        Retourne le maximum compris entre interval[0] interval[1]
        data = [x,y]
    """
    interval.sort()
    nData = data[(data[:,0] > interval[0])&(data[:,0] < interval[1])]
    if len(nData[:,1])<1:return
    index = np.argmax(nData[:,1])
    return nData[index]

def partial_mean(data, interval):
    """
        Retourne le maximum compris entre interval[0] interval[1]
        data = [x,y]
    """
    interval.sort()
    nData = data[(data[:,0] > interval[0])&(data[:,0] < interval[1])]
    if len(nData[:,1])<1:return
    return nData[:,1].mean()

def find_nearest(array,value):
    """
        Retourne l element le plus proche de value ainsi que son index
    """
    index = (np.abs(array-value)).argmin()
    return index, array[index]



def closest_point(point, points,onlyx=False):
    points = np.asarray(points)
    if onlyx:
        dist_2 = abs(points[:,0]-point[0])
    else:
        dist_2 = np.sum((points - point)**2, axis=1)
    return np.argmin(dist_2)

def strToPoint(pt):
    if pt:
        s = str(pt)
        if (not s.endswith(']')):s=s+']'
        if (not s.startswith('[')):s='['+s
        pt = ast.literal_eval(s)
        return list(pt)
    else:
        return None