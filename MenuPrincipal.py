import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi
from ventana1 import Ui_Form
from Pusuario import ClasePusuarios
from PHistorial import ClasePhistorial
from PCuentas import ClasePCuentas
from Cliente import ClasePCliente
from PTransacciones import ClasePTransacciones
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db



class ClaseMenuPrincipal(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(ClaseMenuPrincipal, self).__init__(parent)
        loadUi("menu_principal.ui", self)
        self.configurar()

    def configurar(self):
        #lee el archivo de texto donde esta el usuario logueado y busca en la base de datos para saber si es o no admin
        #si no es admin desactiva los botones
        nombre_archivo = "userlog.txt"  # Reemplaza con el nombre de tu archivo
        try:
            with open(nombre_archivo, "r") as archivo:
                contenido = archivo.read()
            # 'contenido' ahora contiene el contenido del archivo
        except FileNotFoundError:
            print(f"El archivo {nombre_archivo} no se encontró.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
        contenido=contenido.split()
        contenido=str(contenido[1])
        dbconfig = leer_configuracion_db()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        #print(contenido)
        consulta = "SELECT * FROM usuarios WHERE nombreUsuario=%s"
        datos = (contenido,)
        cursor.execute(consulta, datos)
        resultado = cursor.fetchone()
        #desactivar los botones si no es admin
        #print(resultado)
        if resultado[3]=="Administrador":
            self.btnUsuarios.setEnabled(True)
            self.btnHistorial.setEnabled(True)
        else:
            self.btnUsuarios.setEnabled(False)
            self.btnHistorial.setEnabled(False)

        # conecciones de botones del menu principal
        self.btnUsuarios.clicked.connect(self.abrirPantallaUsuario)
        self.btnClientes.clicked.connect(self.abrirPantallaClientes)
        self.btnCuentas.clicked.connect(self.abrirPantallaCuentas)
        self.btnHistorial.clicked.connect(self.abrirPantallaHistorial)
        self.btnTransacciones.clicked.connect(self.abrirPantallaTransacciones)
        self.btnSalir.clicked.connect(self.close)

    def abrirPantallaUsuario(self):
        self.Pusuario = ClasePusuarios()  # Crea una instancia
        self.Pusuario.show()

    def abrirPantallaHistorial(self):
        self.PHistorial = ClasePhistorial()  # Crea una instancia
        self.PHistorial.show()

    def abrirPantallaCuentas(self):
        self.PCuentas = ClasePCuentas()  # Crea una instancia
        self.PCuentas.show()

    def abrirPantallaClientes(self):
        self.PClientes = ClasePCliente()  # Crea una instancia
        self.PClientes.show()

    def abrirPantallaTransacciones(self):
        self.PTransacciones = ClasePTransacciones()  # Crea una instancia
        self.PTransacciones.show()

def main():
    app = QApplication(sys.argv)
    ventana = ClaseMenuPrincipal()
    ventana.show()
    app.exec_()


if __name__ == '__main__':
    main()
