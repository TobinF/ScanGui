# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\OneDrive - sjtu.edu.cn\Experiment\GUI\ScanGui\test000.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(625, 490)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(50, 90, 441, 201))
        self.groupBox.setObjectName("groupBox")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(20, 40, 401, 141))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.st1 = QtWidgets.QPushButton(self.widget)
        self.st1.setObjectName("st1")
        self.gridLayout.addWidget(self.st1, 0, 0, 1, 1)
        self.sp1 = QtWidgets.QPushButton(self.widget)
        self.sp1.setObjectName("sp1")
        self.gridLayout.addWidget(self.sp1, 0, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.widget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 0, 2, 1, 1)
        self.st1_2 = QtWidgets.QPushButton(self.widget)
        self.st1_2.setObjectName("st1_2")
        self.gridLayout.addWidget(self.st1_2, 1, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 1, 1, 1)
        self.progressBar_2 = QtWidgets.QProgressBar(self.widget)
        self.progressBar_2.setProperty("value", 24)
        self.progressBar_2.setObjectName("progressBar_2")
        self.gridLayout.addWidget(self.progressBar_2, 1, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        # Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "GroupBox"))
        self.st1.setText(_translate("Dialog", "PushButton"))
        self.sp1.setText(_translate("Dialog", "PushButton"))
        self.st1_2.setText(_translate("Dialog", "PushButton"))
        self.pushButton_4.setText(_translate("Dialog", "PushButton"))
