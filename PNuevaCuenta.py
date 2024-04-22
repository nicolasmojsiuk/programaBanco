import random
import sys


from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QPushButton
from PyQt5.uic import loadUi
from ventana1 import Ui_Form

from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db
import nltk
nltk.download("words")
from nltk.corpus import words
import random

word_list = words.words()


class ClasePnuevaCuenta(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(ClasePnuevaCuenta, self).__init__(parent)
        loadUi("PNuevacuenta.ui", self)
        self.configurar()

    def configurar(self):
        self.btnGuardar.clicked.connect(self.nuevacuenta)
        self.btnSalir.clicked.connect(self.close)

    def nuevacuenta(self):

        nombrecliente = self.leNombreCliente.text()
        tipoDeCuenta = self.cbTipoDeCuenta.currentText()

        if nombrecliente == "":
            QMessageBox.about(self, "ERROR", "No deje campos en blanco")
            return

        if tipoDeCuenta =="caja de ahorro en pesos":
            tipoDeCuentan=2
        if tipoDeCuenta =="corriente en pesos":
            tipoDeCuentan=1
        if tipoDeCuenta =="caja de ahorro en reales":
            tipoDeCuentan=3
        if tipoDeCuenta =="caja de ahorro en dolares":
            tipoDeCuentan=4
        if tipoDeCuenta =="caja de ahorro en euros":
            tipoDeCuentan=5

        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT idclientes FROM clientes WHERE nombre=%s"
            datos=(nombrecliente,)
            cursor.execute(consulta,datos)
            # Obtener los datos de la consulta
            datos = cursor.fetchone()
            if datos==[] or datos==None:
                QMessageBox.warning(self, "Error", "El cliente no existe")
                return
            else:
                idcliente = datos[0]
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()



        try:
            alias = self.obteneralias()
            nombre_archivo= "notalias.txt"
            with open(nombre_archivo, "r") as archivo:
                contenido = archivo.read()
                contenido=contenido.split()
                notalias=contenido
            #seleciona una palabra random para usarla como alias
            while alias in notalias:
                alias=self.obteneralias()

            db_config = leer_configuracion_db()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            consulta = "INSERT INTO cuentas (alias, idcliente, tipo, fechaDeApertura) VALUES(%s, %s, %s, NOW())"
            datos = (alias, idcliente, tipoDeCuentan)
            cursor.execute(consulta, datos)

            if cursor.lastrowid:
                mensaje = f"Exito! Nueva cuenta creada:\nCliente: {nombrecliente}\nCBU: {cursor.lastrowid}\nAlias: {alias}"
                self.msg_box = QMessageBox()
                self.msg_box.setWindowTitle("Éxito!")
                self.msg_box.setText(mensaje)

                boton_ok = QPushButton("OK")
                icono = QIcon("ok.png")
                boton_ok.setIcon(icono)
                boton_ok.clicked.connect(lambda: self.msg_box.done(QMessageBox.Ok))  # Cerrar con código de aceptación
                self.msg_box.addButton(boton_ok, QMessageBox.ActionRole)
                # Mostrar el QMessageBox
                self.msg_box.exec_()


            else:
                print("Error al agregar registro")
            conn.commit()  # Debe ir después de la inserción
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

#--------------------GUARDAR EN EL HISTORIAL-----------------------

            try:
                with open("userlog.txt", "r") as archivo:
                    # Escribe contenido en el archivo
                    contenido = archivo.read()
                contenido = contenido.split()
                # datos para guardar en el historial
                iduparahistorial = int(contenido[0])
                detalle = "Dio de alta una cuenta"
                masdetalle="tipo: "+str(tipoDeCuenta)+" cliente: "+str(nombrecliente)
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "INSERT INTO historialusuarios (idusuario, detalle, fecha, masdetalle) VALUES (%s, %s, NOW(), %s)"
                datos = (iduparahistorial, detalle, masdetalle)
                cursor.execute(consulta, datos)
                conn.commit()
            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()

    def obteneralias(self):
        listaAlias = words.words()
        alias = random.choice(listaAlias)
        with open("notalias.txt", "a") as archivo:
            # Escribe contenido en el archivo
            archivo.write(" "+alias)
        return(alias)


def main():
    app = QApplication(sys.argv)
    ventana = ClasePnuevaCuenta()
    ventana.show()
    app.exec_()


if __name__ == '__main__':
    main()
