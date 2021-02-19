# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ListaContribuyentes.ui',
# licensing of 'ListaContribuyentes.ui' applies.
#
# Created: Thu Feb 18 23:54:55 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(353, 348)
        MainWindow.setMaximumSize(QtCore.QSize(353, 348))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(96, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(96, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 5, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(71, 148, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        self.lista = QtWidgets.QListWidget(self.centralwidget)
        self.lista.setObjectName("lista")
        self.gridLayout.addWidget(self.lista, 1, 1, 1, 5)
        spacerItem3 = QtWidgets.QSpacerItem(72, 148, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 6, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(121, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 2, 0, 1, 3)
        self.aceptar = QtWidgets.QPushButton(self.centralwidget)
        self.aceptar.setObjectName("aceptar")
        self.gridLayout.addWidget(self.aceptar, 2, 3, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(121, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 2, 4, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 353, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Lista", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Lista de Contribuyentes", None, -1))
        self.aceptar.setText(QtWidgets.QApplication.translate("MainWindow", "Aceptar", None, -1))

