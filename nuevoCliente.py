import sys
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db

class ClaseNuevoCliente(QMainWindow):
    def __init__(self, parent=None):
        super(ClaseNuevoCliente, self).__init__(parent)
        loadUi("PNuevoCliente.ui", self)
        self.configurar()

    def configurar(self):
        self.btnGuardarCliente.clicked.connect(self.insertar_un_registro)
        self.btnClose.clicked.connect(self.close)

    def insertar_un_registro(self):
        db_config = leer_configuracion_db()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

        try:
            nombre = self.leNombre.text()
            dni = self.leDni.text()
            estado = self.cbEstado.currentText()
            telefono = self.leTelefono.text()
            direccion = self.leDireccion.text()
            fechaNacimiento = self.deFechaNacimiento.date().toString("yyyy-MM-dd")

            if estado=='Activo':
                estado=1
            elif estado=='Inactivo':
                estado=0
            # Verifica que los campos requeridos no estén vacíos
            if not nombre or not dni or not telefono or not direccion:
                QMessageBox.warning(self, "Campos vacíos", "Por favor, complete todos los campos obligatorios.")
            else:
                dni = int(dni)
                telefono = int(telefono)

                consulta = "INSERT INTO clientes (nombre, dni, fechaDeNacimiento, numeroDeTelefono, fechaDeRegistro, estado, direccion) VALUES(%s, %s, %s, %s, NOW(), %s, %s)"
                datos = (nombre, dni, fechaNacimiento, telefono, estado, direccion)
                cursor.execute(consulta, datos)

                if cursor.lastrowid:
                    idcliente=cursor.lastrowid
                    QMessageBox.about(self, "Éxito!", "Se añadió el cliente")
                    self.close()  # Cierra la ventana después de agregar el cliente
                else:
                    print("Error al agregar registro")

                conn.commit()

                try:
                    # Abre el archivo de texto en modo lectura
                    with open('userlog.txt', 'r') as archivo:
                        primera_linea = archivo.readline()
                        palabras = primera_linea.split()
                        idusuariolog = palabras[0]
                except Error as e:
                    print(e)

                try:
                    idparatxt = int(idusuariolog)
                    detalle = "Agrego un cliente"
                    masdetalle = f"Nombre: {nombre}"
                    dbconfig = leer_configuracion_db()
                    conn = MySQLConnection(**dbconfig)
                    cursor = conn.cursor()
                    consulta = "INSERT INTO historialusuarios (idusuario, detalle, fecha, masdetalle) VALUES (%s, %s, NOW(), %s)"
                    datos = (idparatxt, detalle, masdetalle)
                    cursor.execute(consulta, datos)
                    conn.commit()
                except Error as e:
                    print(e)
                finally:
                    cursor.close()
                    conn.close()

        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


def main():
    app = QApplication(sys.argv)
    ventana = ClaseNuevoCliente()
    ventana.show()
    app.exec_()

if __name__ == '__main__':
    main()