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

from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtWidgets import QMessageBox
from Interfaz import CFDIM
from Controlador import altacontribuyente
from Controlador import lista
from Controlador.calendario import Calendario
from cfdiclient import Autenticacion
from cfdiclient import DescargaMasiva
from cfdiclient import Fiel
from cfdiclient import SolicitaDescarga
from cfdiclient import VerificaSolicitudDescarga
from Controlador.ModuloModels import *

from lxml import etree
from decimal import Decimal
import zipfile
import base64
import sys
import os
import shutil
import errno
from datetime import date
import time
from PySide2.QtGui import QIcon
import ctypes
import configparser
import xlsxwriter
import subprocess


class Cfdiui(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()
        self.ui = CFDIM.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("CFDI")
        self.showMaximized()
        appIcon = QIcon("cfdi.ico")
        self.setWindowIcon(appIcon)
        #necesario para mostrar icono en barra de tarea de windows7
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.fechaI = ''
        self.RFC = ''
        self.FIEL_KEY = ''
        self.FIEL_PAS = ''
        self.PATH = 'C:/CFDIs/'
        self.ui.lrfc.setText(self.RFC)
        self.connect(self.ui.lRfcRazon, SIGNAL("textChanged(QString)"),
                    lambda: cambioTexto(self.ui.lRfcRazon,
                    self.lista, self.model))
        self.ui.bfechaInicial.clicked.connect(self.mostrarI)
        self.ui.bfechaFinal.clicked.connect(self.mostrarF)
        self.ui.bdescarga.clicked.connect(self.descarga)
        self.ui.bexportar.clicked.connect(self.exportar)
        self.inicio()

    def exportar(self):
        workbook = xlsxwriter.Workbook(self.dest + 'Recibidos' + '.xlsx')
        worksheet = workbook.add_worksheet()
        header = ["Folio Fiscal", "Serie", "Folio", "Fecha", "Receptor", "RFC",
            "Subtotal", "IVA", "Total", "Forma de Pago",
            "Metodo de Pago", "Uso de CFDI", "Tot Imp Tras", "Pago"]
        self.lista2.insert(0, header)
        worksheet.set_column('A:A', 40)
        cell_format = workbook.add_format()
        cell_format.set_num_format(3)
        worksheet.set_column('G:G', None, cell_format)
        for row_num, row_data in enumerate(self.lista2):
            for col_num, col_data in enumerate(row_data):
                worksheet.write(row_num, col_num, col_data)
        workbook.close()
        archivo = (self.dest + 'Recibidos' + '.xlsx')
        subprocess.Popen([archivo], shell=True)

    def descarga(self):
        if len(self.ui.lfechaInicial.text()) == 0 or len(
            self.ui.lfechaFinal.text()) == 0:
            QMessageBox.warning(self, "Cuidado!",
            "Debes seleccionar rango de fechas")
        else:
            self.fechaInicial = date(
                int(self.ui.lfechaInicial.text().split('-')[0]),
                int(self.ui.lfechaInicial.text().split('-')[1]),
                int(self.ui.lfechaInicial.text().split('-')[2]))
            self.fechaFinal = date(
                int(self.ui.lfechaFinal.text().split('-')[0]),
                int(self.ui.lfechaFinal.text().split('-')[1]),
                int(self.ui.lfechaFinal.text().split('-')[2]))
            self.descargasat()

    def mostrarI(self):
        self.cal = Calendario(self, 1)
        self.cal.show()

    def mostrarF(self):
        self.cal = Calendario(self, 2)
        self.cal.show()

    def inicio(self):
        directorio = self.PATH
        try:
            os.stat(directorio)
        except:
            os.mkdir(directorio)
        contenido = os.listdir(directorio)
        if len(contenido) > 0:
            self.lista = lista.ListaC(self)
            self.lista.show()
        else:
            self.alta = altacontribuyente.Alta(self)
            self.alta.show()

    def cargar(self, rfc):
        configuracion = configparser.ConfigParser()
        configuracion.read('C:/CFDIs/' + rfc + '/datos.cfg')
        self.RFC = configuracion['Contribuyente']['rfc']
        self.FIEL_KEY = configuracion['Contribuyente']['key']
        self.FIEL_CER = configuracion['Contribuyente']['certificado']
        self.FIEL_PAS = configuracion['Contribuyente']['passwd']

    def descomprimir(self, ruta, dest):
        self.dest = self.PATH + self.RFC + '/'
        with zipfile.ZipFile(ruta, "r") as zip_ref:
            zip_ref.extractall(self.dest)
        directorio = self.dest
        contenido = os.listdir(directorio)
        cfdis = []
        for fichero in contenido:
            if os.path.isfile(os.path.join(
                directorio, fichero)) and fichero.endswith('.xml'):
                cfdis.append(fichero)
        for i in range(len(cfdis)):
            doc = etree.parse(directorio + str(cfdis[i]))
            raiz = doc.getroot()
            for elemnt in raiz.iter("{http://www.sat.gob.mx/cfd/3}Comprobante"):
                fecha = elemnt.attrib['Fecha'].split('T')[0]
                try:
                    os.mkdir('C:/CFDIs/' + str(self.RFC) + '/' +
                    fecha.split('-')[0])
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
            for elemnt in raiz.iter("{http://www.sat.gob.mx/cfd/3}Comprobante"):
                fecha = elemnt.attrib['Fecha'].split('T')[0]
                try:
                    os.mkdir('C:/CFDIs/' + str(self.RFC) + '/' +
                    fecha.split('-')[0] + '/' + fecha.split('-')[1])
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
            for elemnt in raiz.iter("{http://www.sat.gob.mx/cfd/3}Comprobante"):
                origen = 'C:/CFDIs/' + str(self.RFC) + '/' + cfdis[i]
                destino = 'C:/CFDIs/' + str(self.RFC) + '/' + \
                fecha.split('-')[0] + '/' + fecha.split('-')[1]
                shutil.move(origen, destino)
        self.dest = self.PATH + self.RFC + '/'
        self.listar()
        QMessageBox.warning(self, "Terminado", "Se ha completado la descarga")

    def listar(self):
        cfdis = []
        for nombre_dir, dirs, ficheros in os.walk(self.dest):
            for nombre_fichero in ficheros:
                if os.path.isfile(os.path.join(
                    nombre_dir, nombre_fichero)
                    ) and nombre_fichero.endswith('.xml'):
                    cfdis.append(os.path.join(nombre_dir, nombre_fichero))
        self.leerxml(cfdis)

    def leerxml(self, cfdis):
        header = ["Folio Fiscal", "Serie", "Folio", "Fecha", "Receptor", "RFC",
            "Subtotal", "IVA", "Total", "Forma de Pago",
            "Metodo de Pago", "Uso de CFDI", "Tot Imp Tras", "Pago"]
        self.columnaProductos = dict(id='', nombre='')
        self.lista = []
        self.lista2 = []
        for i in range(len(cfdis)):
            doc = etree.parse(cfdis[i])
            raiz = doc.getroot()
            for elemnt in raiz.iter("{http://www.sat.gob.mx/cfd/3}Receptor"):
                usocfdi = elemnt.attrib['UsoCFDI']
                try:
                    nombreC = elemnt.attrib['Nombre']
                except:
                    nombreC = ''
            for elemnt in raiz.iter("{http://www.sat.gob.mx/cfd/3}Emisor"):
                rfc = elemnt.attrib['Rfc']
                nombre = elemnt.attrib['Nombre']
            for elemnt in raiz.iter("{http://www.sat.gob.mx/cfd/3}Comprobante"):
                try:
                    serie = elemnt.attrib['Serie']
                except:
                    serie = ''
                try:
                    folio = elemnt.attrib['Folio']
                except:
                    folio = ''
                fecha = elemnt.attrib['Fecha'].split('T')[0]
                try:
                    formapago = elemnt.attrib['FormaPago']
                except:
                    formapago = ''
                try:
                    metpago = elemnt.attrib['MetodoPago']
                except:
                    metpago = ''
                subtotal = elemnt.attrib['SubTotal']
                total = elemnt.attrib['Total']
            if Decimal(total) > 0:
                imp = "{http://www.sat.gob.mx/cfd/3}Impuestos"
                for elemnt in raiz.iter(imp):
                    try:
                        totimp = elemnt.attrib['TotalImpuestosTrasladados']
                    except:
                        totimp = ''
                pago = 0
            else:
                totimp = 0
                for element in raiz.iter("{http://www.sat.gob.mx/Pagos}Pago"):
                    pago = element.attrib['Monto']
                    formapago = element.attrib['FormaDePagoP']
            u = "{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital"
            for elmnt in raiz.iter(u):
                uuid = elmnt.attrib['UUID'].upper()
            self.lista.append(list((uuid, serie, folio, fecha, nombre, rfc,
                subtotal, totimp, total, formapago, metpago, usocfdi,
                totimp, pago)))
            self.lista2.append(list((uuid, serie, folio, fecha, nombre, rfc,
                subtotal, totimp, total, formapago, metpago, usocfdi,
                totimp, pago)))
        self.model = MyTableModel(self.lista, header, self)
        self.ui.tCfdi.setModel(self.model)
        self.ui.tCfdi.resizeColumnsToContents()
        self.ui.lrazon.setText(nombreC)

    def descargasat(self):
        configuracion = configparser.ConfigParser()
        self.RFC = self.ui.lrfc.text()
        configuracion.read('C:/CFDIs/' + self.RFC + '/datos.cfg')
        self.RFC = configuracion['Contribuyente']['rfc']
        self.FIEL_KEY = configuracion['Contribuyente']['key']
        self.FIEL_CER = configuracion['Contribuyente']['certificado']
        self.FIEL_PAS = configuracion['Contribuyente']['passwd']
        cer_der = open(self.FIEL_CER, 'rb').read()
        key_der = open(self.FIEL_KEY, 'rb').read()

        FECHA_INICIAL = self.fechaInicial
        FECHA_FINAL = self.fechaFinal

        fiel = Fiel(cer_der, key_der, self.FIEL_PAS)
        auth = Autenticacion(fiel)
        token = auth.obtener_token()
        #print('TOKEN: ', token)
        descarga = SolicitaDescarga(fiel)
        # EMITIDOS
        # solicitud = descarga.solicitar_descarga(
        #     token, RFC, FECHA_INICIAL, FECHA_FINAL, rfc_emisor=RFC,
        #tipo_solicitud='CFDI'
        # )

        # RECIBIDOS
        solicitud = descarga.solicitar_descarga(
            token, self.RFC, FECHA_INICIAL, FECHA_FINAL, rfc_receptor=self.RFC,
        tipo_solicitud='CFDI'
        )
        #print('SOLICITUD:', solicitud)
        while True:
            token = auth.obtener_token()
            #print('TOKEN: ', token)
            verificacion = VerificaSolicitudDescarga(fiel)
            verificacion = verificacion.verificar_descarga(
                token, self.RFC, solicitud['id_solicitud'])
            #print('SOLICITUD:', verificacion)
            estado_solicitud = int(verificacion['estado_solicitud'])
            # 1, Aceptada
            # 2, En proceso
            # 3, Terminada
            # 4, Error
            # 5, Rechazada
            # 6, Vencida
            if estado_solicitud <= 2:
                # Si el estado de solicitud esta Aceptado o en proceso el
                # programa espera 60 segundos y vuelve a tratar de verificar
                time.sleep(60)
                continue
            elif estado_solicitud >= 4:
                #print('ERROR:', estado_solicitud)
                QMessageBox.warning(self, "ERROR:", estado_solicitud)
                break
            else:
                # Si el estatus es 3 se trata de descargar los paquetes
                for paquete in verificacion['paquetes']:
                    descarga = DescargaMasiva(fiel)
                    descarga = descarga.descargar_paquete(token, self.RFC,
                        paquete)
                    #print('PAQUETE: ', paquete)
                    with open(self.PATH + self.RFC + '/' +
                        '{}.zip'.format(paquete), 'wb') as fp:
                        fp.write(base64.b64decode(descarga['paquete_b64']))
                ruta = self.PATH + self.RFC + '/' +\
                '{}.zip'.format(paquete)
                dest = self.PATH + self.RFC + '/'
                self.descomprimir(ruta, dest)
                break


if __name__ == "__main__":

    app = QApplication(sys.argv)
    ventana = Cfdiui()
    ventana.show()
    sys.exit(app.exec_())
