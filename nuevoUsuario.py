import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db

class ClaseNuevoUsuario(QMainWindow):
    def __init__(self, parent=None):
        super(ClaseNuevoUsuario, self).__init__(parent)
        loadUi("PNuevoUsuario.ui", self)
        self.configurar()

    def configurar(self):
        self.btnGuardar.clicked.connect(self.insertar_un_registro)
        self.btnSalir.clicked.connect(self.close)

    def insertar_un_registro(self):
        self.nombreusuario = self.leNombreUsuario.text()
        self.contraseña = self.leContra.text()
        self.email = self.leEmail.text()
        self.grupo = self.cbGrupo.currentText()
        self.estado = self.cbEstado.currentText()
        if self.estado =="Inactivo":
            self.estado=0
        else:
            self.estado=1

        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT nombreUsuario FROM usuarios WHERE nombreUsuario = %s"
            cursor.execute(consulta, (self.nombreusuario,))
            nombre_existente = cursor.fetchone()
            conn.commit()
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

        if nombre_existente:
            QMessageBox.about(self, "ERROR", "El nombre de usuario " + self.nombreusuario + " no está disponible")
            return


        if self.nombreusuario =="" or self.contraseña=="" or self.email=="":
            QMessageBox.about(self, "ERROR", "No deje campos en blanco")
            return
        else:
            try:
                db_config = leer_configuracion_db()
                conn = MySQLConnection(**db_config)
                cursor = conn.cursor()
                consulta = "INSERT INTO usuarios (nombreUsuario, contraseña, grupo, email, estado, fechaCreacion) VALUES(%s, %s, %s, %s, %s, NOW())"
                datos = (self.nombreusuario, self.contraseña, self.grupo, self.email, self.estado)
                cursor.execute(consulta, datos)

                if cursor.lastrowid:
                    QMessageBox.about(self, "Exito!", "Se añadio el usuario")
                else:
                    print("Error al agregar registro")

                conn.commit()  # Debe ir después de la inserción
            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()

            #GUARDAR EN EL HISTORIAL
            try:
                with open('userlog.txt', 'r') as archivo:
                    primera_linea = archivo.readline()
                    palabras = primera_linea.split()
                    idusuariolog = palabras[0]
            except Error as e:
                print(e)

            try:
                nombre_usuario = self.nombreusuario
                idparatxt = int(idusuariolog)
                detalle = "Dio de alta un usuario"
                masdetalle = f"Nombre: {nombre_usuario}"
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
            self.close()

def main():
    app = QApplication(sys.argv)
    ventana = ClaseNuevoUsuario()
    ventana.show()
    app.exec_()

if __name__ == '__main__':
    main()