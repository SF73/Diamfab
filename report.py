# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 23:44:52 2018

@author: Sylvain
"""

import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image,Table
from reportlab.graphics.shapes import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from graph import HyperlinkedImage,genLayers,genLayers2,resize
from Subfunctions import strToTable
import subprocess

def report(path,name,samp,substrate,layers):
    doc = SimpleDocTemplate(path,pagesize=A4,
                            rightMargin=1.5*cm,leftMargin=1.5*cm,
                            topMargin=1.5*cm,bottomMargin=1.5*cm)
    width,height = A4
    styles=getSampleStyleSheet()
    
    
    
    Story=[]
    logo = "res/logo.png"
    
    #Logo 
    im = HyperlinkedImage(logo,width=3.5*cm,height=3.5*cm,hyperlink="http://diamfab.eu")
    im.hAlign='RIGHT'
    Story.append(im)
    
    #Title
    Story.append(Spacer(1, -2.5*cm))
    Story.append(Paragraph("""%s<font size="12"><br/>%s</font>"""%(name,""), styles["Title"]))
    Story.append(Spacer(1, 2*cm))
    
    
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    
#    data = [['Propiété1','Valeur'],
#            ['Propiété2','Valeur'],
#            ['Propiété3','Valeur'],
#            ['Propiété4','Valeur'],
#            ['Propiété5','Valeur']]

    data = strToTable(substrate).tolist()
    if len(data)>0:
        Story.append(Paragraph("Substrate specification :",styles['Heading2']))
        tstyle =    [
        #                ('GRID', (0, 0), (-1, -1), 1, colors.black),
        #                ('GRID', (4, 0), (4, 2), 1, colors.black),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.lightblue,colors.white])
                    ]
        t = Table(data,style=tstyle,colWidths=(width-3*cm)/2)
        Story.append(t)

    Story.append(Paragraph("Layers : ",styles['Heading2']))
    data = strToTable(layers).tolist()
    
    
    if len(data)>0:
        tstyle =    [
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.lightblue,colors.white])
                    ]
        data.reverse()
        layerspict = Image(genLayers2(data),4*cm,100)
        layerspict.hAlign='LEFT'
        Story.append(layerspict)
        data.reverse()
        data = [['Layer','Thickness*','Boron density (cm^-3)**']]+ data
        t = Table(data,style=tstyle)
        Story.append(Spacer(1,-100))
        Story.append(t)
        w, h = t.wrap(0, 0)
        Story.append(Spacer(1,100-h))
        Story.append(Paragraph("*\t:Mesured by ellipsometry",styles["BodyText"]))
        Story.append(Paragraph("**\t:Mesured by cathodoluminescence",styles["BodyText"]))
    
    Story.append(Spacer(1, 12))
    Story.append(Paragraph("Boron Density",styles['Heading2']))
    bd = ImageReader(samp.as_Image())
    iw,ih = bd.getSize()
    nw,nh = resize(iw,ih,15*cm)
    bd = Image(samp.as_Image(),nw,nh)
    Story.append(bd)
    
    doc.build(Story)
    subprocess.Popen([path],shell=True)