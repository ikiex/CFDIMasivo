#-*- coding: utf-8 -*-
#-----------------------------------------------------------------------#
# Autor: Luis Enrique Rojas Desales                                     #
#-----------------------------------------------------------------------#
# Este codigo esta liberado bajo licencia GPL.                          #
#-----------------------------------------------------------------------#
'''
Descarga Masiva SAT
Luis E. Rojas Desales

'''
from Interfaz import ListaRFC

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow
from PySide2 import QtCore
import os
import configparser


class ListaC(QMainWindow):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.ui = ListaRFC.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(QIcon('cfdi.ico'))
        self.inicio()

    def inicio(self):
        contenido = os.listdir('C:/CFDIs/')
        for i in range(len(contenido)):
            self.ui.lista.addItem(contenido[i])
        self.ui.lista.itemDoubleClicked.connect(self.onClicked)
        self.ui.aceptar.clicked.connect(self.aceptar)

    def onClicked(self, item):
        #QMessageBox.information(self, "Info", item.text())
        self.close()
        configuracion = configparser.ConfigParser()
        configuracion.read('C:/CFDIs/' + item.text() + '/datos.cfg')
        self.parent.ui.lrfc.setText(configuracion['Contribuyente']['rfc'])
        self.parent.ui.lrazon.setText(configuracion['Contribuyente']['razon'])
        self.parent.cargar(configuracion['Contribuyente']['rfc'])

    def aceptar(self):
        item = self.ui.lista.currentItem()
        self.close()
        configuracion = configparser.ConfigParser()
        configuracion.read('C:/CFDIs/' + item.text() + '/datos.cfg')
        self.parent.ui.lrfc.setText(configuracion['Contribuyente']['rfc'])
        self.parent.ui.lrazon.setText(configuracion['Contribuyente']['razon'])
        self.parent.cargar(configuracion['Contribuyente']['rfc'])
