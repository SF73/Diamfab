# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pdfDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_pdfDialog(object):
    def setupUi(self, pdfDialog):
        pdfDialog.setObjectName("pdfDialog")
        pdfDialog.resize(241, 287)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pdfDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(pdfDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(pdfDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.nameTxt = QtWidgets.QLineEdit(pdfDialog)
        self.nameTxt.setObjectName("nameTxt")
        self.gridLayout.addWidget(self.nameTxt, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(pdfDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.substrateTxt = QtWidgets.QPlainTextEdit(pdfDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.substrateTxt.sizePolicy().hasHeightForWidth())
        self.substrateTxt.setSizePolicy(sizePolicy)
        self.substrateTxt.setObjectName("substrateTxt")
        self.gridLayout.addWidget(self.substrateTxt, 2, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(pdfDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.layersTxt = QtWidgets.QPlainTextEdit(pdfDialog)
        self.layersTxt.setObjectName("layersTxt")
        self.gridLayout.addWidget(self.layersTxt, 4, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(pdfDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)

        self.retranslateUi(pdfDialog)
        self.buttonBox.accepted.connect(pdfDialog.accept)
        self.buttonBox.rejected.connect(pdfDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(pdfDialog)

    def retranslateUi(self, pdfDialog):
        _translate = QtCore.QCoreApplication.translate
        pdfDialog.setWindowTitle(_translate("pdfDialog", "Export as PDF"))
        self.label.setText(_translate("pdfDialog", "Name"))
        self.label_2.setText(_translate("pdfDialog", "Substrate"))
        self.substrateTxt.setPlainText(_translate("pdfDialog", "Size, mm\t4.0 x 4.0\n"
"Thickness, mm\t0.5\n"
"Type\tIIa\n"
"Face orientation\t(100)"))
        self.label_3.setText(_translate("pdfDialog", "Layers"))
        self.layersTxt.setPlainText(_translate("pdfDialog", "p--\t4000nm\t5E20\n"
"p++\t460nm\t>4E20\n"
"substrate\t5000nm\t5E20"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pdfDialog = QtWidgets.QDialog()
    ui = Ui_pdfDialog()
    ui.setupUi(pdfDialog)
    pdfDialog.show()
    sys.exit(app.exec_())

