# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sampleDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_sampleDialog(object):
    def setupUi(self, sampleDialog):
        sampleDialog.setObjectName("sampleDialog")
        sampleDialog.resize(243, 233)
        sampleDialog.setMinimumSize(QtCore.QSize(243, 233))
        sampleDialog.setMaximumSize(QtCore.QSize(243, 233))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        sampleDialog.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(sampleDialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 200, 156, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.nameTxt = QtWidgets.QLineEdit(sampleDialog)
        self.nameTxt.setGeometry(QtCore.QRect(100, 10, 133, 20))
        self.nameTxt.setObjectName("nameTxt")
        self.label = QtWidgets.QLabel(sampleDialog)
        self.label.setGeometry(QtCore.QRect(10, 14, 47, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(sampleDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 51, 20))
        self.label_2.setObjectName("label_2")
        self.tlTxt = QtWidgets.QLineEdit(sampleDialog)
        self.tlTxt.setGeometry(QtCore.QRect(100, 40, 133, 20))
        self.tlTxt.setObjectName("tlTxt")
        self.label_3 = QtWidgets.QLabel(sampleDialog)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 51, 20))
        self.label_3.setObjectName("label_3")
        self.trTxt = QtWidgets.QLineEdit(sampleDialog)
        self.trTxt.setGeometry(QtCore.QRect(100, 70, 133, 20))
        self.trTxt.setObjectName("trTxt")
        self.label_4 = QtWidgets.QLabel(sampleDialog)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 61, 20))
        self.label_4.setObjectName("label_4")
        self.blTxt = QtWidgets.QLineEdit(sampleDialog)
        self.blTxt.setGeometry(QtCore.QRect(100, 100, 133, 20))
        self.blTxt.setObjectName("blTxt")
        self.label_5 = QtWidgets.QLabel(sampleDialog)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 61, 20))
        self.label_5.setObjectName("label_5")
        self.brTxt = QtWidgets.QLineEdit(sampleDialog)
        self.brTxt.setGeometry(QtCore.QRect(100, 130, 133, 20))
        self.brTxt.setObjectName("brTxt")
        self.label_6 = QtWidgets.QLabel(sampleDialog)
        self.label_6.setGeometry(QtCore.QRect(10, 160, 61, 20))
        self.label_6.setObjectName("label_6")
        self.cTxt = QtWidgets.QLineEdit(sampleDialog)
        self.cTxt.setGeometry(QtCore.QRect(100, 160, 133, 20))
        self.cTxt.setObjectName("cTxt")

        self.retranslateUi(sampleDialog)
        self.buttonBox.accepted.connect(sampleDialog.accept)
        self.buttonBox.rejected.connect(sampleDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(sampleDialog)

    def retranslateUi(self, sampleDialog):
        _translate = QtCore.QCoreApplication.translate
        sampleDialog.setWindowTitle(_translate("sampleDialog", "New Sample"))
        self.nameTxt.setText(_translate("sampleDialog", "NDTXX"))
        self.label.setText(_translate("sampleDialog", "Name"))
        self.label_2.setText(_translate("sampleDialog", "Top Left"))
        self.tlTxt.setText(_translate("sampleDialog", "[0,4]"))
        self.label_3.setText(_translate("sampleDialog", "Top right"))
        self.trTxt.setText(_translate("sampleDialog", "[3.7,4]"))
        self.label_4.setText(_translate("sampleDialog", "Bottom left"))
        self.blTxt.setText(_translate("sampleDialog", "[0,0]"))
        self.label_5.setText(_translate("sampleDialog", "Bottom right"))
        self.brTxt.setText(_translate("sampleDialog", "[4,0]"))
        self.label_6.setText(_translate("sampleDialog", "Cut"))
        self.cTxt.setText(_translate("sampleDialog", "[4,3.5]"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    sampleDialog = QtWidgets.QDialog()
    ui = Ui_sampleDialog()
    ui.setupUi(sampleDialog)
    sampleDialog.show()
    sys.exit(app.exec_())

