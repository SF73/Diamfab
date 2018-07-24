# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'optionsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_optionsDialog(object):
    def setupUi(self, optionsDialog):
        optionsDialog.setObjectName("optionsDialog")
        optionsDialog.resize(162, 96)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../res/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        optionsDialog.setWindowIcon(icon)
        self.widget = QtWidgets.QWidget(optionsDialog)
        self.widget.setGeometry(QtCore.QRect(9, 9, 145, 80))
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.templbl = QtWidgets.QLabel(self.widget)
        self.templbl.setObjectName("templbl")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.templbl)
        self.tempcomboBox = QtWidgets.QComboBox(self.widget)
        self.tempcomboBox.setEditable(False)
        self.tempcomboBox.setCurrentText("")
        self.tempcomboBox.setObjectName("tempcomboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tempcomboBox)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.pushButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.buttonBox)

        self.retranslateUi(optionsDialog)
        self.buttonBox.accepted.connect(optionsDialog.accept)
        self.buttonBox.rejected.connect(optionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(optionsDialog)

    def retranslateUi(self, optionsDialog):
        _translate = QtCore.QCoreApplication.translate
        optionsDialog.setWindowTitle(_translate("optionsDialog", "Options"))
        self.templbl.setText(_translate("optionsDialog", "Temperature"))
        self.pushButton.setText(_translate("optionsDialog", "View Calibration"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    optionsDialog = QtWidgets.QDialog()
    ui = Ui_optionsDialog()
    ui.setupUi(optionsDialog)
    optionsDialog.show()
    sys.exit(app.exec_())

