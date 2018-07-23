from __future__ import print_function

import sys

import numpy as np
#from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication,
                            QFileDialog, QWidget, QMenu, QMessageBox, QDialog,QVBoxLayout)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
#from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
from Calibrate import calibrate
from SpectrumAnalyser import SpectrumAnalyser
from Subfunctions import strToPoint
from UI.pdfDialog import Ui_pdfDialog
from UI.pointDialog import Ui_pointDialog
from UI.sampleDialog import Ui_sampleDialog
from UI.aboutDialog import Ui_aboutDialog
from report import report
import os
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',datefmt='%H:%M:%S')

#from matplotlib.backends import qt4_compat

#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from sample import sample

class AppForm(QMainWindow):
    def autosave(self):
        if self.sample is not None:
            try:
                self.sample.save("temp\\autosave.npz")
                logger.info("Autosave")
            except Exception as e:
                logger.exception("Can't autosave")
    
    def restore(self):
        if (self.sample is None) & os.path.isfile("temp\\autosave.npz"):
            restore_msg = "Do you want to load autosave"
            reply = QMessageBox.question(self, 'Autosave found', 
                     restore_msg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.sample = sample.load("temp\\autosave.npz")
                self.sample.show(self.fig)
            else:
                os.remove("temp\\autosave.npz")
                return
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.create_main_frame()
        self.params = calibrate(plot=False)
        os.makedirs("temp", exist_ok=True)
        self.restore()

    def create_main_frame(self):
        self.sample = None
        self.setWindowTitle('Boron Mapping')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.main_frame = QWidget()
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
#        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        #Open on menubar
        openAct = QAction('&Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open file')
        openAct.triggered.connect(self.load)
        
        saveAct = QAction('&Save', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('Open Directory')
        saveAct.triggered.connect(self.save)

        addptAct = QAction('&Add point', self)
#        addptAct.setShortcut('Ctrl+')
        addptAct.setStatusTip('Add point')
        addptAct.triggered.connect(self.addpoint)
        
        newSampleAct = QAction('&New sample', self)
        newSampleAct.setShortcut('Ctrl+N')
        newSampleAct.setStatusTip('New Sample')
        newSampleAct.triggered.connect(self.newsample)
        
        exportAct = QAction('&Export PDF', self)
        exportAct.setShortcut('Ctrl+P')
        exportAct.setStatusTip('Export PDF')
        exportAct.triggered.connect(self.export)
        
        #menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Sample')
        fileMenu.addAction(newSampleAct)
        fileMenu.addAction(openAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(addptAct)
        fileMenu.addAction(exportAct)
        
#        menubar.addSeparator()
        spec_menu = QMenu('&Spectrum', self)
        menubar.addSeparator()
        menubar.addMenu(spec_menu)
        spec_menu.addAction('&Open', self.openSpectrum)
        
        help_menu = QMenu('&Help', self)
        menubar.addSeparator()
        menubar.addMenu(help_menu)
        help_menu.addAction('&About', self.about)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        vbox.addWidget(self.mpl_toolbar)
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.autosave)
        self.timer.start(60000)

    def fileQuit(self):
        self.close()
    def about(self):
        dlg = aboutDialog()
        dlg.exec_()
#        QMessageBox.about(self, "About",
#                          """Shift+LClick : Delete measure point\nIn Spectrum View :\nShift+LClick : Move nearest peak\nShift+RClick : Move noise baseline\nDouble Click : Move boron density label\n© 2018 Sylvain Finot""")
    def getPoint(self):
        dlg = pointDialog()
        if (dlg.exec_()==QDialog.Accepted):
            values = dlg.getValues()
            return values
        return None,None,None
    def addpoint(self):
        if self.sample is None:
            QMessageBox.warning(self,"Error","No open sample")
            return
        else:
            try:
                pt,transform,path = self.getPoint()
                if (pt is None or transform is None or path is None):
                    logger.warn("""Point & Path can't be None""")
                    return
                pt = strToPoint(pt)
                self.sample.add_point(pt=pt,transform=transform,path=path)
            except Exception as e:
                logging.exception("Point format invalid")
    def load(self):
        path = QFileDialog.getOpenFileName(self, "Open Sample","","(*.npz)")[0]
        if path:
            try:
                logger.info(path)
                if self.sample:
                    self.sample.disconnect_plot()
                self.fig.clear()
                self.sample = sample.load(path)
                self.sample.show(self.fig)
            except Exception as e:
                logger.exception("Can't load sample")
    def keyPressEvent(self, event):
        if ((event.key() == QtCore.Qt.Key_Shift) & (self.sample is not None)):
            self.sample.shift_is_held = True
        if((event.modifiers()==QtCore.Qt.ControlModifier) & (self.sample is not None) & (event.key()==QtCore.Qt.Key_C)):
            self.sample.copy2clipboard()

        event.accept()
    def keyReleaseEvent(self, event):
        if ((event.key() == QtCore.Qt.Key_Shift) & (self.sample is not None)):
            self.sample.shift_is_held = False
        event.accept()
    def save(self):
        path = QFileDialog.getSaveFileName(self, "Save file", "",'(*.npz)')[0]
        if path:
            self.sample.save(path)
    
    def openSpectrum(self):
        path = QFileDialog.getOpenFileName(self, "Open Spectrum","","")[0]
        if path:
            try:
                spectrum = SpectrumAnalyser.from_csv(path,self.params)
                spectrum.plot()
            except Exception as e:
                logger.exception("Can't open spectrum")
    def newsample(self):
        try:
            dlg = sampleDialog()
            if (dlg.exec_()==QDialog.Accepted):
                name,pt = dlg.getValues()          
                if (pt is None or np.equal(pt[:-1],None).any()):
                    raise TypeError
                self.fig.clear()
                if self.sample:
                    self.sample.disconnect_plot()
                self.sample=sample(name=name,
                    bl=pt[0],
                    br=pt[1],
                    tl=pt[2],
                    tr=pt[3],
                    c=pt[4])
                self.sample.show(self.fig)
        except TypeError:
            logger.exception("Can't create sample : At least one point is invalid")
        except Exception as e:
            logger.exception("Can't create sample")
        
    def export(self):
        if self.sample is None:
            QMessageBox.warning(self,"Error","No open sample")
            return
        try:
            dlg = pdfDialog()
            if (dlg.exec_()==QDialog.Accepted):
                name,subs,layers = dlg.getValues()
                path = QFileDialog.getSaveFileName(self, "Save file", "",'(*.pdf)')[0]
                if path:
                    report(path=path,name=name,samp=self.sample,substrate=subs,layers=layers)
        except PermissionError as e:
            logger.error("Can't export PDF : File is probably open")
        except Exception as e:
            logger.exception("Can't export PDF")
            
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', 
                     quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            try:
                os.remove("temp\\autosave.npz")
            except OSError:
                pass
        else:
            event.ignore()


#--------------------Dialog inhenerit--------------------
            
class pointDialog(QDialog, Ui_pointDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.path=None
        self.openBtn.pressed.connect(self.openfile)
    def getValues(self):
        return self.pointTxt.text(),self.transformChk.isChecked(),self.path
    def openfile(self):
        path = QFileDialog.getOpenFileName(self, "Open Spectrum","","")[0]
        if path:
            self.path=path
            self.pathTxt.setText(path)
                     
#--------------------------------------------------------
            
class sampleDialog(QDialog, Ui_sampleDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        
    def getValues(self):
        name = self.nameTxt.text()
        tl = self.tlTxt.text()
        bl = self.blTxt.text()
        tr = self.trTxt.text()
        br = self.brTxt.text()
        cut = self.cTxt.text()
        cut = None if not cut else cut
        pt = [bl,br,tl,tr,cut]
        pt = [strToPoint(x) for x in pt]
        return name,pt
    
#--------------------------------------------------------    
        
class pdfDialog(QDialog, Ui_pdfDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        
    def getValues(self):
        return self.nameTxt.text(),self.substrateTxt.toPlainText(),self.layersTxt.toPlainText()
    
#--------------------------------------------------------  
        
class aboutDialog(QDialog, Ui_aboutDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        filename = 'README.md'
        with open(filename) as f:
            data = f.read()
        self.aboutTxt.setPlainText(data)

#--------------------------------------------------------  
        
def main():
    logger.info('Start')
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()