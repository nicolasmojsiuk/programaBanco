import sys
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QMainWindow
from ventana1 import Ui_Form
from PyQt5.uic import loadUi
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db
from MenuPrincipal import ClaseMenuPrincipal

class ClaseImportarForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(ClaseImportarForm, self).__init__(parent)
        loadUi("login.ui", self)
        self.btnIngresar.clicked.connect(self.ingresar)


    def ingresar(self):
        self.nombreusuario = self.leNombreUsuario.text()
        self.email = self.nombreusuario
        self.contraseña = self.leContra.text()

        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT * FROM usuarios WHERE nombreUsuario = %s OR email = %s"
            datos = (self.nombreusuario, self.email)
            cursor.execute(consulta, datos)
            resultado = cursor.fetchall()
            if len(resultado) == 0:
                QMessageBox.about(self, "ERROR", "Ingrese un usuario y una contraseña válidos")
            else:
                if self.contraseña == resultado[0][2] and resultado[0][5]==1:
                    idparatxt = str(resultado[0][0])
                    try:
                        with open("userlog.txt", "w") as archivo:
                            archivo.write(idparatxt+" "+resultado[0][1])
                        detalle = "Inicio de sesión"
                        try:
                            self.idUltimoAcceso=idparatxt
                            dbconfig = leer_configuracion_db()
                            conn = MySQLConnection(**dbconfig)
                            cursor = conn.cursor()
                            consulta = "INSERT INTO historialusuarios (idusuario, detalle, fecha) VALUES (%s, %s, NOW())"
                            datos = (idparatxt, detalle)
                            cursor.execute(consulta, datos)
                            conn.commit()
                        except Error as e:
                            print(e)
                        finally:
                            cursor.close()
                            conn.close()
                    except Exception as e:
                        print(f"Error: {e}")
                    self.abrirMenuP()
                else:
                    QMessageBox.about(self, "ERROR", "Usuario o contraseña incorrectos")
        except Error:
            QMessageBox.Information(self, "Error", "Hubo un error al conectarse a la base de datos", QMessageBox.Ok)
        finally:
            cursor.close()
            conn.close()



    def abrirMenuP(self):
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "UPDATE usuarios SET ultimoAccesso=NOW() WHERE idusuarios=%s"
            datos=(self.idUltimoAcceso,)
            cursor.execute(consulta, datos)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
        self.MenuPrincipal = ClaseMenuPrincipal()  # Crea una instancia de la ventana del menú principal
        self.MenuPrincipal.show()
        self.close()

def main():
    app = QApplication(sys.argv)
    ventana = ClaseImportarForm()
    ventana.show()
    app.exec_()


if __name__ == '__main__':
    main()
