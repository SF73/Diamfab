# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 13:16:26 2018

@author: Sylvain
"""
from reportlab.platypus import Image
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Drawing,Rect,colors
from reportlab.graphics.charts.textlabels import Label
import numpy as np
import logging
logger = logging.getLogger()
class HyperlinkedImage(Image, object):
    """Image with a hyperlink, adopted from http://stackoverflow.com/a/26294527/304209."""

    def __init__(self, filename, hyperlink=None, width=None, height=None, kind='direct',
                 mask='auto', lazy=1, hAlign='CENTER'):
        """The only variable added to __init__() is hyperlink.

        It defaults to None for the if statement used later.
        """
        super(HyperlinkedImage, self).__init__(filename, width, height, kind, mask, lazy,
                                               hAlign=hAlign)
        self.hyperlink = hyperlink

    def drawOn(self, canvas, x, y, _sW=0):
        if self.hyperlink:  # If a hyperlink is given, create a canvas.linkURL()
            # This is basically adjusting the x coordinate according to the alignment
            # given to the flowable (RIGHT, LEFT, CENTER)
            x1 = self._hAlignAdjust(x, _sW)
            y1 = y
            x2 = x1 + self._width
            y2 = y1 + self._height
            canvas.linkURL(url=self.hyperlink, rect=(x1, y1, x2, y2), thickness=0, relative=1)
        super(HyperlinkedImage, self).drawOn(canvas, x, y, _sW)
        
        
def genLayers(l0=["substrate",30],
                           l1=["p++",20],
                                        l2=["p--",50]):
    c = ['#ffeea0','#ff88ff','#bbd5e8']
    length=4*cm
    d = Drawing(4*cm,100)
    xpos=0#*(width-length-4*cm)/2
#        layer0 = 40
#        l1[1] = 40
#        l2[1]= 100-layer0-l1[1]
    l0[1],l1[1],l2[1] = layersize(l0[1],l1[1],l2[1])
    
    d.add(Rect(xpos,0,length,l0[1] ,fillColor=colors.HexColor(c[0])))
    lab = Label()
    lab.textAnchor = 'middle'
    lab.setText(l0[0])
    lab.setOrigin(xpos+2*cm,l0[1]/2)
    d.add(lab)
    
    d.add(Rect(xpos,l0[1],length,l1[1] ,fillColor=colors.HexColor(c[1])))
    lab = Label()
    lab.textAnchor = 'middle'
    lab.setText(l1[0])
    lab.setOrigin(xpos+2*cm,l0[1]+l1[1]/2)
    d.add(lab)
    
    d.add(Rect(xpos,l0[1]+l1[1],length,l2[1] ,fillColor=colors.HexColor(c[2])))
    lab = Label()
    lab.textAnchor = 'middle'
    lab.setText(l2[0])
    lab.setOrigin(xpos+2*cm,l0[1]+l1[1]+l2[1]/2)
    d.add(lab)
    
    return d
    
    
def genLayers2(ls):
    #ls =(titre, taille)
    c = ['#ffeea0','#ff88ff','#bbd5e8']
    length=4*cm
#    ls = np.asarray(ls)
    l = []
    for i in range(len(ls)):
        l.append((ls[i][0],ls[i][1]))
    ls = np.asarray(l,dtype=np.str)
    d = Drawing(4*cm,100)
    xpos=0
    ls[:,1] = layersize2(ls[:,1])
    tickness = ls[:,1].astype(np.float32)
    for i in range(len(ls)):
        lab = Label()
        lab.textAnchor = 'middle'
        color = c[0]
        labelTxt = str(ls[:,0][i])
        if '+' in labelTxt:
            color = c[1]
        elif '-' in labelTxt:
            color = c[2]
        lab.setText(ls[:,0][i])
        if i>0:
            d.add(Rect(xpos,np.cumsum(tickness)[i-1],length,tickness[i] ,fillColor=colors.HexColor(color)))
            lab.setOrigin(xpos+2*cm,np.cumsum(tickness)[i-1]+tickness[i]/2)
        else:
            d.add(Rect(xpos,0,length,tickness[i] ,fillColor=colors.HexColor(color)))
            lab.setOrigin(xpos+2*cm,tickness[i]/2)
        d.add(lab)
    
    return d
    
def layersize2(ls):
    for i in range(len(ls)):
        ls[i]=ls[i].replace('*','')
        if str(ls[i]).endswith("um"):ls[i] = int(ls[i][:-2])*1000
        if str(ls[i]).endswith("nm"):ls[i] = int(ls[i][:-2])
    ls = np.asarray(ls, dtype=np.float32)
    ls = np.log10(ls)
    s = np.sum(ls)
    ls = ls/s*100
    return ls

def resize(w,h,maxwidth):
    return maxwidth,h*maxwidth/w

def layersize(l0,l1,l2):
    if str(l0).endswith("um"):l0 = int(l0[:-2])*1000
    if str(l1).endswith("um"):l1 = int(l1[:-2])*1000
    if str(l2).endswith("um"):l2 = int(l2[:-2])*1000
    
    if str(l0).endswith("nm"):l0 = int(l0[:-2])
    if str(l1).endswith("nm"):l1 = int(l1[:-2])
    if str(l2).endswith("nm"):l2 = int(l2[:-2])
    l0=np.log(l0)
    l1=np.log(l1)
    l2=np.log(l2)
    s = l0+l1+l2
    l0 = l0/s*100
    l1 = l1/s*100
    l2 = l2/s*100
    return l0,l1,l2
    