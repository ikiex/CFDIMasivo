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
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2 import QtGui, QtCore
"""
----------------------------------------------------
- Modelo que se utiliza para buscar una palabra(s) -
- sobre una listview.                              -
----------------------------------------------------
"""


class MyListModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.listdata = datain

    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()])
        else:
            return QVariant()

    def setAllData(self, newdata):
        self.listdata = newdata
        self.reset()

    def string_intersect(str1, str2):
        newlist = []
        for i, j in zip(str1, str2):
            if i == j:
                newlist.append(i)
            else:
                break
        return ''.join(newlist)

"""
----------------------------------------------------
- Modelo que se utiliza para buscar una palabra(s) -
- sobre una tableview.                             -
----------------------------------------------------
"""


class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.headerdata)

    def data(self, index, role):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                #return self.items[index.row()].value[0]
                return self.arraydata[index.row()][index.column()]
            elif role == QtCore.Qt.ItemDataRole:
                #return self.items[index.row()].value[0]
                return self.arraydata[index.row()][index.column()]
            else:
                pass
        #return self.arraydata[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerdata[col]
        else:
            pass

    def setAllData(self, newdata):
            self.beginResetModel()
            self.arraydata = newdata
            self.endResetModel()


"""
--------------------------------------------------------
- Busca las palabras con la inicial de las letra intro -
- ducida                                         .     -
--------------------------------------------------------
"""


def cambioTexto(edit, lista, lm):
    patron = (edit.text().lower())
    nuevaLista = [item for item in lista if item[4].lower().find(patron) >= 0]
    lm.setAllData(nuevaLista)

