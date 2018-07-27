# -*- coding: utf-8 -*-
"""
Created on Wed May 30 15:44:04 2018

@author: sylvain.finot
"""
from Calibrate import calibrate
from SpectrumAnalyser import SpectrumAnalyser
from sample import sample
import time
import matplotlib.pyplot as plt
from report import report
import numpy as np

start_time = time.clock()

params = calibrate(plot=False)

#spectrumA = SpectrumAnalyser.from_csv('06-04-2018\\NDT38\\5\\Spot7_10kV_mag2984k_5K_t100s_slit0-1mm',params)
#spectrumA.plot()
#spectrumA = SpectrumAnalyser.from_csv('NDT33\\1\\Spot7_10kV_mag2984k_5K_t100s_slit0-1mm',params)
#spectrumA.plot()
#spectrum = SpectrumAnalyser.from_csv("""..\\14062018\\06-04-2018\\NDT38\\6\\Spot7_10kV_mag2984k_5K_t100s_slit0-1mm""")
#spectrum.plot()
#NDT38 = sample(name="NDT38",
#                bl=[5.15141,-0.93662],
#                br=[9.16087, -1.30639],
#                tl=[4.80728,-4.92088],
#                c=[8.84821, -4.53165],
#                tr=[8.46323, -5.27961])
#NDT38 = sample(name="NDT38",
#                bl=[5.15141,-0.93662],
#                br=[4.80728,-4.92088],
#                tl=[9.16087, -1.30639],
#                c=[8.46323, -5.27961],
#                tr=[8.84821, -4.53165])
##points = [[8.3821, -4.78165], 
##          [8.3521, -4.72165], 
##          [5.1728,-4.52088], 
##          [5.55141,-1.43662], 
##          [8.5087,-1.80639],
##          [6.9087, -3.0639]]
##for i in range(6):
##    try:
##        s = SpectrumAnalyser.from_csv('06-04-2018\\NDT38\\'+str(i+1)+'\\Spot7_10kV_mag2984k_5K_t100s_slit0-1mm',params)
##        NDT38.add_point(pt=points[i],sa=s)
##    except IOError:
##        print("Error")
#NDT38.show()
#NDT38.save("NDT38")
#report('test.pdf','NDT38',NDT38,substrate=sub,layers=lay)


#NDT33 = sample(name="NDT33",
#                bl=[5.15141,-0.93662],
#                br=[9.16087, -1.30639],
#                tl=[4.80728,-4.92088],
#                c=[8.8821, -4.53165],
#                tr=[8.46323, -5.27961])
#
#points = [[8.3821, -4.78165], 
#          [5.1728,-4.52088], 
#          [5.55141,-1.43662], 
#          [8.5087,-1.80639],
#          [6.9087, -3.0639]]
#for i in range(6):
#    try:
#        s = SpectrumAnalyser.from_csv('06-04-2018\\NDT33\\'+str(i+1)+'\\Spot7_10kV_mag2984k_5K_t100s_slit0-1mm',params)
#        if s:
#            NDT33.add_point(pt=points[i],sa=s)
#    except IOError:
#        print("Error")
#NDT33.show()
#NDT33.save("NDT33")

#bl = [0,0]
#br = [4,0]
#tl=[0,4]
#tr=[3.8,4]
#cut=[4,3.6]
##for i in np.linspace(270,360,20):
#theta = -163*np.pi/180
#c, s = np.cos(theta), np.sin(theta)
#R = np.array(((c,-s), (s, c)))
#bl = R.dot(bl)
#br = R.dot(br)
#tl = R.dot(tl)
#tr = R.dot(tr)
#cut = R.dot(cut)
#
#test = sample(name=theta,
#               bl=bl,
#               br=br,
#               tr=tr,
#               tl=tl,
#               c=cut)
#test.show()
#
#khaled2=sample.load('khaled(2).npz')
#khaled2.transParam[1]+=np.pi/2
#khaled2.show()
#NDT29 = sample(name="NDT29|side",
#               bl=[0,0],
#               br=[3.77160,-0.20193],
#               tr=[3.73762,-0.75031],
#               tl=[-0.02520,-0.52808])
#NDT29.show()
#sample2 = sample(name="NDT38 Tranche",
#                bl=[0,0],
#                br=[0.2, 0],
#                tr=[0.2,4],
#                tl=[0, 4])
#sample2.show()

#sampleA = sample.load("autosave.npz")
#sampleA.show()
#sampleB = sample.load("samples\\NDT38.npz")

#sp = SpectrumAnalyser.from_csv("C:/Users/sylvain.finot/Documents/Mesures/07-05-2018/K5/2/Full_14keV_Spot5_2s_0-1mm_200-800nm",toeV=True)
#sp.plot()
spKhaled = np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/07-05-2018/Khaled/1/Full_14keV_Spot5_4s_0-1mm_200-800nm")
##spK5 = np.loadtxt("C:/Users/sylvain.finot/Documents/Mesures/07-05-2018/K5/2/Full_14keV_Spot5_2s_0-1mm_200-800nm")
#
##f ,(ax,bx) = plt.subplots(2,1, gridspec_kw = {'height_ratios':[1, 1]})
##ax.get_shared_x_axes().join(ax, bx)
f= plt.figure()
bx = f.gca()
##ax.semilogy(1239.8419/spK5[:,0],spK5[:,1])
bx.semilogy(spKhaled[:,0],spKhaled[:,1],label="14keV_Spot5_4s_0-1mm_200-800nm")
##ax.set_title("K5")
#bx.set_title("14594-01-02")
#bx.axvline(x=230,c='grey',ls='--')
#bx.axvline(x=251,c='grey',ls='--')
#bx.text((230+251)/2,260,'1',ha='center')
#
##bx.axvline(x=260,c='grey',ls='--')
##bx.axvline(x=344,c='grey',ls='--')
##bx.text((260+344)/2,260,'2',ha='center')
#
#bx.axvline(x=230*2,c='grey',ls='--')
#bx.axvline(x=250*2,c='grey',ls='--')
#bx.text((230+250),260,'1\'',ha='center')
#
#bx.axvline(x=230*3,c='grey',ls='--')
#bx.axvline(x=251*3,c='grey',ls='--')
#bx.text((230+251)*3/2,260,'1\'\'',ha='center')
#bx.legend()
#f.dpi=600
print("--- %s seconds ---" % (time.clock() - start_time))