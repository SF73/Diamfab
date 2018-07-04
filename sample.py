# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 09:15:51 2018

@author: sylvain.finot
"""
from copy import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as patches
from SpectrumAnalyser import SpectrumAnalyser
import os
import io
import logging
logger = logging.getLogger(__name__)
from copy2clipboard import copy2clipboard
class sample():
    
    
    def __eq__(self, other):
        if self.__class__ != other.__class__: return False
        return np.allclose(self.as_array(),other.as_array())
#        return self.__dict__ == other.__dict__
    
    
    def __init__(self,name="",bl=[0,0],br=[4,0],tl=[4,4],tr=[4,4],c=None,points=[],spectra=[]):
        self.shift_is_held = False
        self.bottom_left=bl
        self.bottom_right= br
        self.top_left = tl
        self.top_right = tr
        self.cut= c
        self.transParam = self.get_transform()
        self.points = points
        self.spectra = spectra
        self.name = name
    def get_transform(self):
        size = np.sqrt((self.bottom_left[0]-self.bottom_right[0])**2+(self.bottom_left[1]-self.bottom_right[1])**2)
        offset=np.asarray(self.bottom_left)
        bl = self.bottom_left - offset
        br = self.bottom_right - offset
        ctheta = (bl[0]-br[0])/size
        theta = np.arccos(ctheta)
        if ((br[0]<0) & (br[1]<0)):
            theta = np.pi-np.arccos(ctheta)
        elif ((br[0]>0) & (br[1]>0)):
            theta = np.arccos(ctheta)+np.pi
        elif ((br[0]>0) & (br[1]<0)):
            theta = np.pi-theta
        elif ((br[0]<0) & (br[1]>0)):
            theta = -np.pi+np.arccos(ctheta)
        elif (theta==np.pi):
            theta = 0
        return np.asarray([offset,theta])

    def transform(self,x,params=None,digit=3):
        tparam = self.transParam if params is None else params
        theta = tparam[1]
        offset = tparam[0]
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c,-s), (s, c)))
        nx = R.dot((np.asarray(x)-offset))
        return nx
    def reversetransform(self,x,params=None,digit=1):
        tparam = self.transParam if params is None else params
        theta = -tparam[1]
        offset = tparam[0]
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c,-s), (s, c)))
        nx = np.round(R.dot(np.asarray(x))+offset,digit)
        return nx
    def onclick(self,event):
        self.update_sample()
        self.fig.canvas.draw()
        plt.draw()
        logger.info("Updated")

    def on_pick(self,event):
        if self.shift_is_held:
            self.spectra.pop(event.ind[0])
            self.points.pop(event.ind[0])
        else:
            self.spectra[event.ind[0]].plot()

    def update_annot(self,ind):
        pos = self.scat.get_offsets()[ind["ind"][0]]
        idx=ind["ind"][0]
        self.annot.xy = pos
        text = '[B] = %.1E $\pm$ %.1E cm$^{-3}$'%(self.spectra[idx].Boron[0],self.spectra[idx].Boron[1])
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_facecolor('w')
        self.annot.get_bbox_patch().set_alpha(1)
    def update_sample(self):
        self.name = self.ax.get_title()
        if(len(self.spectra)>0):
            boron=np.array(list(map(lambda x: x.Boron, self.spectra)))[:,0]
            points = np.asarray([self.transform(x) for x in self.points])
        else:
            boron=np.array([0])
            points = np.array([[],[]]).T
        maxB = boron.max()
        minB = boron.min()
        self.scat.set_offsets(points)
        self.scat.set_array(boron)
        self.stats.set_text("Min : %.1E\nMax : %.1E \nMean : %.1E \nStd : %.1E"%(minB,maxB,boron.mean(),boron.std()))
        maxB=max(boron[boron<2E17])
        ticks=[]
        if(minB > 0):
            if (maxB/minB>10):
                self.norm = mpl.colors.LogNorm(vmin=minB,vmax=maxB)
                ticks = np.logspace(np.log10(minB),np.log10(maxB),7)
            else:
                self.norm = mpl.colors.Normalize(vmin=minB,vmax=maxB)
                ticks = np.linspace(minB,maxB,7)
            self.scat.set_norm(self.norm)
            lab = ["{:4.1E}".format(i) for i in ticks]
            lab[-1] = '>2E17\n'+lab[-1]
            self.cb.set_ticks(ticks)
            self.cb.ax.set_yticklabels(lab,fontsize=9)

    def hover(self,event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            cont, ind = self.scat.contains(event)
            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                if (vis):
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()

    def on_key_press(self, event):
        if event.key == 'shift':
           self.shift_is_held = True
        if event.key == 'ctrl+c':
            self.copy2clipboard()
    def copy2clipboard(self):
        copy2clipboard(self.fig)
        logger.info('Copied to clipboard')
    def on_key_release(self, event):
        if event.key == 'shift':
           self.shift_is_held = False

    def connect(self):
        self.cidpress = self.fig.canvas.mpl_connect('key_press_event', lambda event: self.on_key_press(event))
        self.cidrelease = self.fig.canvas.mpl_connect('key_release_event',lambda event: self.on_key_release(event))
        self.cidhover = self.fig.canvas.mpl_connect("motion_notify_event",lambda event: self.hover(event))
        self.cidclick = self.fig.canvas.mpl_connect('button_press_event',lambda event: self.onclick(event))
        self.cidenter = self.fig.canvas.mpl_connect("figure_enter_event",lambda event: self.onclick(event))
        self.cidpick = self.fig.canvas.mpl_connect('pick_event',lambda event: self.on_pick(event))
    def disconnect_plot(self):
        if self.cidclick is None:return
        self.fig.canvas.mpl_disconnect(self.cidclick)
        self.fig.canvas.mpl_disconnect(self.cidrelease)
        self.fig.canvas.mpl_disconnect(self.cidpress)
        self.fig.canvas.mpl_disconnect(self.cidenter)
        self.fig.canvas.mpl_disconnect(self.cidpick)
        self.fig.canvas.mpl_disconnect(self.cidhover)
        
    def show(self,f=None):
        self.fig = f if not(f is None) else plt.figure()
        if ((not (self.cut is None)) & (not (self.top_right is None))):
            points = [self.bottom_left,self.bottom_right,self.cut,self.top_right,self.top_left]
        else:
            points = [self.bottom_left,self.bottom_right,self.top_right,self.top_left]
        npoints = [self.transform(x) for x in points]
        self.ax = self.fig.gca() if not(f is None) else self.fig.add_subplot(111, aspect='equal')
        self.ax.set_aspect('equal')
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        plt.subplots_adjust(right=0.8)
        self.ax.figure.texts.append(self.ax.texts.pop())
        self.annot.set_visible(False)
        self.ax.add_patch(patches.Polygon(npoints, fill=True,alpha=0.3))
        self.ax.set_title(self.name)
        plt.ylabel('distance (mm)')
        plt.xlabel('distance (mm)')
        self.ax.autoscale()
        self.fig.subplots_adjust(top=0.9,bottom=0.1,left=0.09,right=0.75)
        self.stats = self.fig.text(0.8,0.5,"Min : %.1E\nMax : %.1E \nMean : %.1E \nStd : %.1E"%(0,0,0,0), bbox=dict(boxstyle="square", fc="w"))
        plasma=copy(plt.get_cmap('plasma'))
        plasma.set_over(color='r', alpha=None)
        self.scat = self.ax.scatter([],[],c=[],picker = 2,edgecolors='black',cmap=plasma,zorder=10)
        self.cb=self.fig.colorbar(self.scat,ax=self.ax,spacing='proportional',extend='max',ticks=[])
        self.update_sample()
        self.fig.canvas.draw()
        plt.draw()
        self.connect()
    def as_Image(self):
        noImage = (self.fig is None)
        if noImage:
            self.show()
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png',dpi=300,bbox_inches='tight')
        if noImage:
            plt.close()
        buf.seek(0)
        return buf
    def as_array(self):
        SamplePosition = np.asarray([self.bottom_left,self.bottom_right,self.cut,self.top_right,self.top_left])
        pt = np.asarray(self.points)
        sp = np.array(list(map(lambda x: x.as_array(), self.spectra)))
        return np.array([SamplePosition,pt,sp,self.name])
    def add_point(self,pt=None,sa=None,transform=True,path=None):
        if ((sa is None)&(path is None)):
            logger.error("Not a valid spectrum")
            return
        sa = SpectrumAnalyser.from_csv(path) if sa is None else sa
        if transform == False:
            pt = self.reversetransform(pt,params=self.transParam).tolist()
        if pt is not None:
            self.points.append(pt)
            self.spectra.append(sa)
            return

    def save(self,path):
        SamplePosition = np.asarray([self.bottom_left,self.bottom_right,self.cut,self.top_right,self.top_left])
        pt = np.asarray(self.points)
        sp = np.array(list(map(lambda x: x.as_array(), self.spectra)))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        np.savez_compressed(path,name=self.name,pos=SamplePosition,points=pt,spectra=sp)

    @classmethod
    def load(cls, path):
        files = np.load(path)
        pos = files['pos']
        _points = files['points'].tolist()
        sp = files['spectra']
        _spectra = list(map(lambda x: SpectrumAnalyser.from_array(x),sp))
        try:
            fname=files['name']
        except:
            fname=os.path.splitext(os.path.basename(path))[0]
        return cls(name = fname,bl=pos[0],br=pos[1],tl=pos[4],tr=pos[3],c=pos[2],points = _points, spectra = _spectra)