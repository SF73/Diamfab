# -*- coding: utf-8 -*-
"""
Created on Thu May 31 15:55:52 2018

@author: sylvain.finot
"""
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from Calibrate import calibrate
from Subfunctions import importData, nmFromEV, find_nearest, find_max, Boron,lowpass_filter,closest_point,partial_mean
import logging
from copy2clipboard import copy2clipboard
logger = logging.getLogger(__name__)

IBETO = 5.214
IFETO = 5.272

class SpectrumAnalyser():
    
    def __init__(self,spectrum,params=None,peaks=None,noise=None):
        self.shift_is_held = False
        self.spectrum = spectrum
        self.params = calibrate(plot=False) if params is None else params
        self.peaks = [] if peaks is None else peaks
        self.Boron = 0
        self.noise = 0 if noise is None else noise
        self.coords = []
        self.cidclick = None
        self.analyse()
        
        
    @classmethod
    def from_csv(cls,path,params=None):
        return cls(importData(path),params)
    
    @classmethod
    def from_array(cls,array):
        if len(array)>3:
            return cls(spectrum=array[0],params=array[1],peaks=array[2],noise=array[3])
        elif len(array)>2:
            return cls(spectrum=array[0],params=array[1],peaks=array[2])
        elif len(array)>1:
            return cls(spectrum=array[0],params=array[1])
    def as_array(self):
        return np.asarray([self.spectrum,self.params,self.peaks,self.noise])
    
    def analyse(self):
        if max(self.spectrum[:,0]>10):
#    on est en nm
            self.spectrum[:,0] = nmFromEV(self.spectrum[:,0])
        self.noise = np.percentile(self.spectrum[:,1],10)#partial_mean(self.spectrum,[5.5,6])
        fs = len(self.spectrum[:,0])/abs(self.spectrum[:,0][-1]-self.spectrum[:,0][0])
        try:
            self.fspec = lowpass_filter(self.spectrum[:,1],200,fs,order=1)
        except:
            self.fspec = self.spectrum[:,1]
        if len(self.peaks) < 2:
            s=np.copy(self.spectrum)
            s[:,1]=self.fspec
            autoPeaks=self.find_peaks(s)
            self.IBETO = autoPeaks[find_nearest(autoPeaks[:,0],IBETO)[0]]
            self.IFETO = autoPeaks[find_nearest(autoPeaks[:,0],IFETO)[0]]
            self.edit_peaks(self.IBETO)
            self.edit_peaks(self.IFETO)
        self.Boron = Boron(self.peaks,noise=self.noise,params=self.params)
        return self.Boron
    
    def plot(self,title="",f=None):
        self.fig = f if not(f is None) else plt.figure()
        self.ax = self.fig.gca() if not(f is None) else self.fig.add_subplot(111)
        self.cidclick = self.fig.canvas.mpl_connect('button_press_event',lambda event: self.onclick(event))
        self.cidpress = self.fig.canvas.mpl_connect('key_press_event',lambda event: self.on_key_press(event))
        self.cidrelease = self.fig.canvas.mpl_connect('key_release_event',lambda event: self.on_key_release(event))
        self.ax.set_yscale('log')
        self.ax.plot(self.spectrum[:,0],self.spectrum[:,1],lw=1,label='CL Spectrum')
        self.ax.plot(self.spectrum[:,0],self.fspec,lw=1,label='Filtered')
        self.ax.axvline(IBETO,alpha=0.5,c='gray',linestyle='--')
        self.ax.axvline(IFETO,alpha=0.5,c='gray',linestyle='--')
        ypos= np.round(np.sqrt(abs(self.spectrum[:,1].max()*self.spectrum[:,1].min())),2)
        self.peaksplt, = self.ax.plot(np.asarray(self.peaks)[:,0],np.asarray(self.peaks)[:,1],'+',c='red')
        self.noiseplt = self.ax.axhline(alpha=0.5,c='gray',linestyle=':')
        self.noiseplt.set_ydata(self.noise)
        self.Density = self.ax.text(5.3,ypos,'[B] = %.1E $\pm$ %.1E cm$^{-3}$'%(self.Boron[0],self.Boron[1]),ha='left')
        self.ax.legend(loc='best')
        self.ax.set_title(title)
        self.ax.set_ylabel('CL Intensity (counts)')
        self.ax.set_xlabel('energy (eV)')

        if (f is None):
            self.fig.show()
        self.fig.canvas.draw_idle()
        plt.draw()
    def find_peaks(self,data):
        cSpectrum = data[(data[:,0]>5.18)&(data[:,0]<5.30)]
        sampleeV = len(data[:,0])/abs(data[:,0][0]-data[:,0][-1]) #sample/ev
        peaks = signal.find_peaks(cSpectrum[:,1]/max(cSpectrum[:,1]),height=1e14/self.params[0],prominence=1e-2,distance=0.04*sampleeV,width=0.008*sampleeV)
        peaks = cSpectrum[peaks[0]]
        if (len(peaks)>1):
            logger.debug('Peak: step1')
            return peaks
        peaks = cSpectrum[signal.find_peaks(cSpectrum[:,1]/max(data[:,1]),height=1e14/self.params[0],prominence=1e-2)[0]]
        if (len(peaks)>1):
            logger.debug('Peak: step2')
            return peaks
        pIBETO = find_max(data,[(IBETO+0.02),(IBETO-0.02)])
        pIFETO = find_max(data,[(IFETO+0.02),(IFETO-0.02)])
        peaks = np.asarray([pIBETO,pIFETO])
        if (len(peaks)>1):
            logger.debug('Peak: step3')
            return peaks
        logger.warn("""Can't find any peak""")
        peaks=np.array([[IBETO,-(1e50)/self.params[0]],[IFETO,-1e-49]])
        return peaks
    def edit_peaks(self,peak):
        if peak is None:return
        if len(self.peaks) == 0:
            self.peaks.append(peak)
            return
        else:# len(peaks)>0:
            #on regarde si il y est déja
            if not(peak[0] in np.asarray(self.peaks)[:,0]):
                self.peaks.append(peak)
            if len(self.peaks) > 2:
                self.peaks.pop(0)
            self.Boron = Boron(self.peaks,noise=self.noise,params=self.params)
        return
    def onclick(self,event):
        if (event.button == 1) & (self.shift_is_held):
            test = closest_point([event.xdata,event.ydata],self.peaks,onlyx=True)
            self.peaks[test] = [event.xdata,event.ydata]
        if (event.button == 3) & (self.shift_is_held):
            if event.dblclick:
                self.noise=0
            else:
                self.noise = event.ydata
            self.noiseplt.set_ydata(self.noise)
            logger.debug('NOISE:%.1f'%self.noise)
        if (event.button == 1 & event.dblclick & (not self.shift_is_held)):
            self.Density.set_position((event.xdata,event.ydata))
            
        self.Boron = Boron(self.peaks,noise=self.noise,params=self.params)
        self.peaksplt.set_ydata(np.asarray(self.peaks)[:,1])
        self.peaksplt.set_xdata(np.asarray(self.peaks)[:,0])
        self.Density.set_text('[B] = %.1e'%self.Boron[0]+'$\pm$ %.1e'%self.Boron[1])
        self.Density.set_text('[B] = %.1E $\pm$ %.1E cm$^{-3}$'%(self.Boron[0],self.Boron[1]))
        self.fig.canvas.draw_idle()
        plt.draw()
    
    def on_key_press(self, event):
        if event.key == 'shift':
           self.shift_is_held = True
        if event.key == 'ctrl+c':
            copy2clipboard(self.fig)
            logger.info('Copied to clipboard')
    def on_key_release(self, event):
#        logger.debug("release")
        if event.key == 'shift':
           self.shift_is_held = False
    def disconnect_plot(self):
        if self.cidclick is None:return
        self.fig.canvas.mpl_disconnect(self.cidclick)
        self.fig.canvas.mpl_disconnect(self.cidrelease)
        self.fig.canvas.mpl_disconnect(self.cidpress)