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
from Interfaz import AltaC
#import lista
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2 import QtCore
from PySide2.QtCore import QObject
import os
import errno
import configparser


class Alta(QMainWindow):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.ui = AltaC.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(QIcon('cfdi.ico'))
        self.ui.bcertificado.clicked.connect(self.certificado)
        self.ui.bllave.clicked.connect(self.llave)
        self.ui.guardar.clicked.connect(self.guardar)
        self.RFC = ''
        self.cer = ''
        self.key = ''
        self.passwd = ''

    def tr(self, text):
        return QObject.tr(self, text)

    def certificado(self):
        path_to_file, _ = QFileDialog.getOpenFileName(self, self.tr(
            "Archivo cer"), self.tr("C:\\"), self.tr(
                "Certificado (*.cer)"))
        self.ui.certificado.setText(path_to_file)
        self.cer = path_to_file

    def llave(self):
        path_to_file, _ = QFileDialog.getOpenFileName(self, self.tr(
            "Archivo key"), self.tr("C:\\"), self.tr(
                "Certificado (*.key)"))
        self.ui.llave.setText(path_to_file)
        self.key = path_to_file

    def guardar(self):
        configuracion = configparser.ConfigParser()
        self.RFC = self.ui.rfc.text().upper()
        self.razon = self.ui.razon.text().upper()
        self.passwd = self.ui.contrasena.text()
        try:
            os.mkdir('C:/CFDIs/' + str(self.RFC))
            #for i in range(12):
            #    os.mkdir('C:/CFDIs/' + str(self.RFC) + str('/') + str(i + 1))
            configuracion['Contribuyente'] = {'rfc': self.RFC,
                'razon': self.razon, 'Certificado': self.cer, 'Key': self.key,
                'passwd': self.passwd}
            with open('C:/CFDIs/' + str(self.RFC) + str('/') +
                    'datos.cfg', 'w') as archivoconfig:
                configuracion.write(archivoconfig)
            self.close()
            self.parent.ui.lrfc.setText(configuracion['Contribuyente']['rfc'])
            self.parent.ui.lrazon.setText(configuracion[
                'Contribuyente']['razon'])
            self.parent.cargar(configuracion['Contribuyente']['rfc'])
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

