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
from Interfaz import CalendarioM
from PySide2.QtCore import QDate
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow
from PySide2 import QtCore
from datetime import datetime


class Calendario(QMainWindow):
    #fechaInicial = 0

    def __init__(self, parent, boton):
        self.parent = parent
        self.boton = boton
        super().__init__()
        self.ui = CalendarioM.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowIcon(QIcon('cfdi.ico'))
        self.currentMonth = datetime.now().month
        self.currentYear = datetime.now().year
        self.currentDay = datetime.now().day
        self.ui.calendarWidget.setMaximumDate(QDate(self.currentYear,
            self.currentMonth, self.currentDay))
        self.ui.calendarWidget.setSelectedDate(QDate(self.currentYear,
            self.currentMonth, 1))
        self.ui.aceptar.clicked.connect(self.cerrar)
        self.fecha = ('{0}/{1}/{2}'.format(
            self.currentDay, self.currentMonth, self.currentYear))

    def cerrar(self):
        self.fecha = self.ui.calendarWidget.selectedDate()
        if self.boton == 1:
            self.parent.ui.lfechaInicial.setText(str(self.fecha.toPython()))
        if self.boton == 2:
            self.parent.ui.lfechaFinal.setText(str(self.fecha.toPython()))
        self.close()


