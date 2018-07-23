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

BETO = 5.214
FETO = 5.272
SiCenter = 1.681
class SpectrumAnalyser():
    
    def __init__(self,spectrum,params=None,peaks=None,noise=None,toeV=True):
        self.shift_is_held = False
        self.spectrum = spectrum
        self.params = calibrate(plot=False) if params is None else params
        self.peaks = [] if peaks is None else peaks
        self.Boron = [0,0]
        self.Ratio = [0,0]
        self.noise = [0,0] if noise is None else noise
        self.coords = []
        self.cidclick = None
        self.analyse(toeV)
        
        
    @classmethod
    def from_csv(cls,path,params=None,toeV=True):
        return cls(importData(path),params,toeV=toeV)
    
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
    
    def analyse(self,eV=True):
        if max(self.spectrum[:,0]>10) and eV:
            self.spectrum[:,0] = nmFromEV(self.spectrum[:,0])
        try:
            n = self.spectrum[(self.spectrum[:,0]>5.5)&(self.spectrum[:,0]<6.4)][:,1]
            n.sort()
            self.noise = [np.median(n),1.96*n[0:-2].std()]
        except:
            n=np.sort(self.spectrum[:,1])[:100]
            self.noise = [n.mean(),1.96*n.std()]
        logger.debug('NOISE:%.1f +- %.1f'%(self.noise[0],self.noise[1]))
        fs = len(self.spectrum[:,0])/abs(self.spectrum[:,0][-1]-self.spectrum[:,0][0])
        try:
            self.fspec = lowpass_filter(self.spectrum[:,1],200,fs,order=1)
        except:
            self.fspec = self.spectrum[:,1]
        mask = (self.spectrum[:,0]>5.18)&(self.spectrum[:,0]<5.30)
        #initialize default value
        if np.sum(mask)>1:
            if len(self.peaks) < 2:
                r = 100*self.noise[0]/find_max(self.spectrum,[5.18,5.30])[1]
                s=np.copy(self.spectrum)
                if r>10:           
                    s[:,1]=self.fspec
                autoPeaks=self.find_peaks(s[mask])
                logger.debug("PEAKS : ")
                logger.debug(autoPeaks)
                pBETO = autoPeaks[find_nearest(autoPeaks[:,0],BETO)[0]]
                pFETO = autoPeaks[find_nearest(autoPeaks[:,0],FETO)[0]]
                logger.debug(pBETO)
                logger.debug(pFETO)
                self.edit_peaks(pBETO)
                self.edit_peaks(pFETO)
        self.Boron, self.Ratio = Boron(self.peaks,noise=self.noise,params=self.params)
        return self.Boron
    
    def find_peaks(self,data):
        sampleeV = len(data[:,0])/abs(data[:,0][0]-data[:,0][-1]) #sample/ev
        peaks = signal.find_peaks(data[:,1]/max(data[:,1]),height=1e14/self.params[0],prominence=1e-2,distance=0.04*sampleeV,width=0.008*sampleeV)
        peaks = data[peaks[0]]
        if (len(peaks)>1):
            logger.debug('Peak: step1')
            return peaks
        peaks = data[signal.find_peaks(data[:,1]/max(data[:,1]),height=1e14/self.params[0],prominence=1e-2)[0]]
        if (len(peaks)>1):
            logger.debug('Peak: step2')
            return peaks
        pIBETO = find_max(data,[(BETO+0.02),(BETO-0.02)])
        pIFETO = find_max(data,[(FETO+0.02),(FETO-0.02)])
        peaks = np.asarray([pIBETO,pIFETO])
        if (len(peaks)>1):
            logger.debug('Peak: step3')
            return peaks
        logger.warn("""Can't find any peak""")
        peaks=np.array([[BETO,-(1e50)/self.params[0]],[FETO,-1e-49]])
        return peaks
    def edit_peaks(self,peak):
        if peak is None:return
        if len(self.peaks) == 0:
            self.peaks.append(peak)
            return
        else:
            #on regarde si il y est déja
            if not(peak[0] in np.asarray(self.peaks)[:,0]):
                self.peaks.append(peak)
            if len(self.peaks) > 2:
                self.peaks.pop(0)
            self.Boron, self.Ratio = Boron(self.peaks,noise=self.noise,params=self.params)
        return
       
    def plot(self,title="",f=None):
        self.fig = f if not(f is None) else plt.figure()
        self.ax = self.fig.gca() if not(f is None) else self.fig.add_subplot(111)
        self.cidclick = self.fig.canvas.mpl_connect('button_press_event',lambda event: self.onclick(event))
        self.cidpress = self.fig.canvas.mpl_connect('key_press_event',lambda event: self.on_key_press(event))
        self.cidrelease = self.fig.canvas.mpl_connect('key_release_event',lambda event: self.on_key_release(event))
        self.ax.set_yscale('log')
        self.ax.plot(self.spectrum[:,0],self.spectrum[:,1],lw=1,label='CL Spectrum')
        self.ax.plot(self.spectrum[:,0],self.fspec,lw=1,label='Filtered')
        Emax = np.max(self.spectrum[:,0])
        Emin = np.min(self.spectrum[:,0])
        if (BETO > Emin)&(BETO < Emax):self.ax.axvline(BETO,alpha=0.5,c='gray',linestyle='--')
        if (FETO > Emin)&(FETO < Emax):self.ax.axvline(FETO,alpha=0.5,c='gray',linestyle='--')
        if (SiCenter > Emin)&(SiCenter < Emax):self.ax.axvline(SiCenter,alpha=0.5,c='gray',linestyle='--')
        ypos= np.round(np.sqrt(abs(self.spectrum[:,1].max()*self.spectrum[:,1].min())),2)
        try:
            self.peaksplt, = self.ax.plot(np.asarray(self.peaks)[:,0],np.asarray(self.peaks)[:,1],'+',c='red')
        except:
            pass
        self.noiseplt = self.ax.axhline(alpha=0.5,c='gray',linestyle=':')
        self.noiseplt.set_ydata(self.noise[0])
        self.Density = self.ax.text(5.3,ypos,'r=%.4f $\pm$ %.2E\n[B] = %.1E $\pm$ %.1E cm$^{-3}$'%(self.Ratio[0],self.Ratio[1],self.Boron[0],self.Boron[1]),ha='left')
        self.ax.legend(loc='best')
        self.ax.set_title(title)
        self.ax.set_ylabel('CL Intensity (counts)')
        self.ax.set_xlabel('energy (eV)')
        self.ax.autoscale()
        if (f is None):
            self.fig.show()
        self.fig.canvas.draw_idle()
        plt.draw()
        
    def onclick(self,event):
        
        if (event.button == 1) & (self.shift_is_held):
            test = closest_point([event.xdata,event.ydata],self.peaks,onlyx=True)
            self.peaks[test] = [event.xdata,event.ydata]
            self.peaksplt.set_ydata(np.asarray(self.peaks)[:,1])
            self.peaksplt.set_xdata(np.asarray(self.peaks)[:,0])
            
        #reset noise
        if (event.button == 3) & (self.shift_is_held):
            if event.dblclick:
                self.noise=[0,0]
            else:
                self.noise = [event.ydata,0]
            self.noiseplt.set_ydata(self.noise[0])
            logger.debug('NOISE:%.1f +- %.1f'%(self.noise[0],self.noise[1]))
            
        #move label
        if (event.button == 1 & event.dblclick & (not self.shift_is_held)):
            self.Density.set_position((event.xdata,event.ydata))
            
        self.Boron, self.Ratio = Boron(self.peaks,noise=self.noise,params=self.params)
        self.Density.set_text('r=%.4f $\pm$ %.2E\n[B] = %.1E $\pm$ %.1E cm$^{-3}$'%(self.Ratio[0],self.Ratio[1],self.Boron[0],self.Boron[1]))
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