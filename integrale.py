# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 13:38:26 2018

@author: sylvain.finot
"""

from scipy.optimize import curve_fit
import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
from Subfunctions import find_max,importData
from scipy.integrate import simps
import scipy.interpolate as inter

#gaussian = lambda x: 3*np.exp(-(30-x)**2/20.)
def gauss_function(x, b, a, x0, sigma):
    return b + a*np.exp(-(x-x0)**2/(2*sigma**2))

def lorenz(x,b, a, x0,sigma):
    return b+a/np.pi * (sigma/((x-x0)**2+sigma**2))

def gauss_fit(data,interval,noise=None,amp=None,sig=None,mean=None):
    base=np.percentile(data[:,1],20) if noise is None else noise
    interval.sort()
    data = data[(data[:,0] > interval[0])&(data[:,0] < interval[1])]
    X = data[:,0]
    x = np.sum(X*data[:,1])/np.sum(data[:,1]) if mean is None else mean
    width = np.sqrt(np.abs(np.sum((X-x)**2*data[:,1])/np.sum(data[:,1]))) if sig is None else sig
    a = data[:,1].max()-base if amp is None else amp
    popt, pcov = curve_fit(lambda x,a,x0,sigma : gauss_function(x,base,a,x0,sigma), X , data[:,1], p0 = [a, x, width])
    return np.array([base,*popt])

def gauss_area(amp,sig):
    return amp*np.sqrt(np.pi)*sig
    
sp = []
#sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/07-05-2018/R9/4/24keV_Spot4_2s_0-1mm_5K"))
#sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/07-05-2018/R9/4/24keV_Spot4-5_1s_0-1mm_5K"))
#sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/07-05-2018/R9/4/24keV_Spot5_0-5s_0-1mm_5K"))
#sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/07-05-2018/R9/4/24keV_Spot5_0-5s_0-1mm_5K_02"))

sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-29-2018/1/10x10 12kV Spot 3/1"))
sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-29-2018/1/10x10 12kV Spot 3/2"))
sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-29-2018/1/10x10 12kV Spot 3/3"))
sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-29-2018/1/10x10 12kV Spot 3/4"))
sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-29-2018/1/10x10 12kV Spot 3/5"))
sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-29-2018/1/10x10 12kV Spot 3/6"))
sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-29-2018/1/10x10 12kV Spot 3/7"))
sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-29-2018/1/10x10 12kV Spot 3/8"))
sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-29-2018/1/10x10 12kV Spot 3/9"))
sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-29-2018/1/10x10 12kV Spot 3/10"))


#sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-04-2018/NDT33/6/Spot7_10kV_mag2984k_5K_t10s_slit0-1mm"))
#sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-04-2018/NDT33/6/Spot7_10kV_mag2984k_5K_t50s_slit0-1mm"))

#sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-04-2018/NDT33/1/Spot7_10kV_mag2984k_5K_t100s_slit0-1mm"))
#sp.append(np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/06-04-2018/NDT38/3/Spot7_10kV_mag2984k_5K_t100s_slit0-1mm"))


#sp.append(importData("C:/Users/sylvain.finot/Desktop/GD171B_faceB_point1_merged.txt"))
#sp.append(importData("C:/Users/sylvain.finot/Desktop/GD171B_faceA_point2_merged.txt"))
#sp.append(importData("C:/Users/sylvain.finot/Desktop/GD171B_face_A_point1_merged.txt"))
#sp.append(importData("C:/Users/sylvain.finot/Desktop/GD171B_faceB_point2_merged.txt"))

maxRatio = []
gaussRatio = []
ampRatio = []
intRatio = []
splineRatio = []
f = plt.figure()
for data in sp:
    #BETO = data[(data[:,0]<236)&(data[:,0]>234)]
    ##print(INT.simps(BETO[:,1],BETO[:,0]))
    #FETO = data[(data[:,0]<233.5)&(data[:,0]>231.5)]
    ##print(INT.simps(FETO[:,1],FETO[:,0]))
    ###data = data[(data[:,0]<233.5)&(data[:,0]>231.5)]
    
    ax = f.gca()
    ax.semilogy(data[:,0],data[:,1], '-',alpha=0.8)
    ##
    #base=np.percentile(data[:,1],10)
    #data = BETO
    #data = FETO
    #X = data[:,0]#np.arange(data.size)
    ##data = data[:,1]
    #x = np.sum(X*data[:,1])/np.sum(data[:,1])
    #width = np.sqrt(np.abs(np.sum((X-x)**2*data[:,1])/np.sum(data[:,1])))
    #amp = data[:,1].max()-base
    #fit = lambda t : base+amp*np.exp(-(t-x)**2/(2*width**2))
    #
    #popt, pcov = curve_fit(lambda x,a,x0,sigma : gauss_function(x,base,a,x0,sigma), X , data[:,1], p0 = [amp, x, width])
    
    #Gaussian
    paraBETO = gauss_fit(data,[233,236])
#    ax.plot(data[:,0],gauss_function(data[:,0],*paraBETO),label='fit BETO')
    paraFETO = gauss_fit(data,[236.5,238])
#    ax.plot(data[:,0],gauss_function(data[:,0],*paraFETO),label='fit FETO')
    
    
    #SPLINE
#    cdata = data[(data[:,0] > 233)&(data[:,0] < 236)]
#    s1 = inter.UnivariateSpline(cdata[:,0],cdata[:,1]-paraBETO[0],s=0.1)
#    spIntBE = s1.integral(paraBETO[2]-2.355/2*paraBETO[3],paraBETO[2]+2.355/2*paraBETO[3])
#    cdata = data[(data[:,0] > 236.5)&(data[:,0] < 238)]
#    s2 = inter.UnivariateSpline(cdata[:,0],cdata[:,1]-paraFETO[0],s=0.1)
#    spIntFE = s2.integral(paraFETO[2]-2.355/2*paraFETO[3],paraFETO[2]+2.355/2*paraFETO[3])
#    splineRatio.append(spIntBE/spIntFE)
    
    
    gaussRatio.append(gauss_area(paraBETO[1],paraBETO[3])/gauss_area(paraFETO[1],paraFETO[3]))
    maskFETO = (data[:,0]>=(paraFETO[2]-2.355/2*paraFETO[3]))&(data[:,0]<=(paraFETO[2]+2.355/2*paraFETO[3]))
    maskBETO = (data[:,0]>=(paraBETO[2]-2.355/2*paraBETO[3]))&(data[:,0]<=(paraBETO[2]+2.355/2*paraBETO[3]))
#    ax.hlines(y=paraFETO[1]/2-paraFETO[0],xmin=data[maskFETO][:,0].min(),xmax=data[maskFETO][:,0].max())
#    ax.hlines(y=paraBETO[1]/2-paraBETO[0],xmin=data[maskBETO][:,0].min(),xmax=data[maskBETO][:,0].max())
    intFETO=simps(y=(data[maskFETO][:,1]-paraFETO[0]),x=data[maskFETO][:,0])
    intBETO=simps(y=(data[maskBETO][:,1]-paraBETO[0]),x=data[maskBETO][:,0])
    intRatio.append(intBETO/intFETO)
    base=np.percentile(data[:,1],20)
    ampRatio.append(paraBETO[3]/paraFETO[3])
    maxRatio.append((find_max(data,[234,236])[0]-base)/(find_max(data,[231,234])[0]-base))
#    ax.legend()
    ax.set_xlim(232,240)
maxRatio = np.array(maxRatio)
gaussRatio = np.array(gaussRatio)
ampRatio = np.array(ampRatio)
intRatio = np.array(intRatio)
splineRatio = np.array(splineRatio)
#fig, axes = plt.subplots(nrows=2, ncols=2,sharey='all')
#
#axes[0,0].plot((maxRatio-maxRatio.mean())/maxRatio.mean(),'.')
#axes[1,0].plot((gaussRatio-gaussRatio.mean())/gaussRatio.mean(),'.')
#axes[0,1].plot((ampRatio-ampRatio.mean())/ampRatio.mean(),'.')
#axes[1,1].plot((intRatio-intRatio.mean())/intRatio.mean(),'.')

fig, axes = plt.subplots(nrows=2, ncols=2,sharey='all')

axes[0,0].plot((maxRatio/maxRatio.mean()-1),'.',label='Std/mean : %.4f'%(maxRatio.std()/maxRatio.mean()))
axes[0,0].set_title("Maxima Ratio")
axes[0,0].legend()

axes[1,0].plot((gaussRatio/gaussRatio.mean()-1),'.',label='Std/mean : %.4f'%(gaussRatio.std()/gaussRatio.mean()))
axes[1,0].set_title("Gaussian Area Ratio")
axes[1,0].legend()

axes[0,1].plot((ampRatio/ampRatio.mean()-1),'.',label='Std/mean : %.4f'%(ampRatio.std()/ampRatio.mean()))
axes[0,1].set_title("Gaussian Amplitude Ratio")
axes[0,1].legend()

axes[1,1].plot((intRatio/intRatio.mean()-1),'.',label='Std/mean : %.4f'%(intRatio.std()/intRatio.mean()))
axes[1,1].set_title("Integrated intensity Ratio")
axes[1,1].legend()

#best, cov = curve_fit(lambda x,a,x0,sigma : gauss_function(x,base,a,x0,sigma), X , data[:,1], p0 = [amp, x,width])
#
#plt.plot(X,lorenz(X,base,*best))