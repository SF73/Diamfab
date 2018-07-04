# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pointDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_pointDialog(object):
    def setupUi(self, pointDialog):
        pointDialog.setObjectName("pointDialog")
        pointDialog.resize(400, 102)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pointDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(pointDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pointTxt = QtWidgets.QLineEdit(pointDialog)
        self.pointTxt.setObjectName("pointTxt")
        self.gridLayout.addWidget(self.pointTxt, 0, 0, 1, 1)
        self.transformChk = QtWidgets.QCheckBox(pointDialog)
        self.transformChk.setChecked(True)
        self.transformChk.setObjectName("transformChk")
        self.gridLayout.addWidget(self.transformChk, 0, 1, 1, 1)
        self.pathTxt = QtWidgets.QLineEdit(pointDialog)
        self.pathTxt.setObjectName("pathTxt")
        self.gridLayout.addWidget(self.pathTxt, 1, 0, 1, 1)
        self.openBtn = QtWidgets.QPushButton(pointDialog)
        self.openBtn.setObjectName("openBtn")
        self.gridLayout.addWidget(self.openBtn, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(pointDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(pointDialog)
        self.buttonBox.accepted.connect(pointDialog.accept)
        self.buttonBox.rejected.connect(pointDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(pointDialog)

    def retranslateUi(self, pointDialog):
        _translate = QtCore.QCoreApplication.translate
        pointDialog.setWindowTitle(_translate("pointDialog", "Add point"))
        self.pointTxt.setText(_translate("pointDialog", "[0,0]"))
        self.transformChk.setText(_translate("pointDialog", "Transform"))
        self.pathTxt.setText(_translate("pointDialog", "Spectrum Path"))
        self.openBtn.setText(_translate("pointDialog", "Open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pointDialog = QtWidgets.QDialog()
    ui = Ui_pointDialog()
    ui.setupUi(pointDialog)
    pointDialog.show()
    sys.exit(app.exec_())

