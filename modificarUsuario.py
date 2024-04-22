import datetime
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox
from PyQt5.uic import loadUi
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db


class ClaseModificarUsuario(QMainWindow):
    def __init__(self, parent=None):
        super(ClaseModificarUsuario, self).__init__(parent)
        loadUi("PmodificarUsuario.ui", self)
        self.configurar()
        self.id=id
        print(self.id)
    def configurar(self):
        self.cbEstado.setDisabled(True)
        self.cbGrupo.setDisabled(True)
        self.leNombreUsuario.setDisabled(True)
        self.leContra.setDisabled(True)
        self.leEmail.setDisabled(True)
        self.btnModificar.clicked.connect(self.modificar_un_registro)
        self.btnGuardar.clicked.connect(self.guardarRegistroModificado)
        self.btnSalir.clicked.connect(self.close)

    def modificar_un_registro(self):
        self.cbEstado.setDisabled(False)
        self.cbGrupo.setDisabled(False)
        self.leNombreUsuario.setDisabled(False)
        self.leContra.setDisabled(False)
        self.leEmail.setDisabled(False)
        try:
            # Pide al usuario el ID que desea modificar
            id, ok = QInputDialog.getInt(self, "Modificar Cliente", "Ingrese el numero del usuario a modificar:")
            if ok:
                try:
                    dbconfig = leer_configuracion_db()
                    conn = MySQLConnection(**dbconfig)
                    cursor = conn.cursor()
                    consulta = "SELECT idusuarios, nombreUsuario FROM usuarios"
                    cursor.execute(consulta,)
                # Obtener los datos de la consulta
                    datos = cursor.fetchall()
                    for fila in datos:
                        if int(fila[0]) == id:
                            nombre_usuario = fila[1]
                            id=fila[0]
                            break
                        else:
                            nombre_usuario = None

                except Error as e:
                    print(e)

                if nombre_usuario is not None:
                    self.id=id
                    # Continuar con la modificación
                    dbconfig = leer_configuracion_db()
                    conn = MySQLConnection(**dbconfig)
                    cursor = conn.cursor()
                    consulta = "SELECT * FROM usuarios WHERE idusuarios=%s"
                    datos = (id,)
                    cursor.execute(consulta, datos)
                    # Obtener los datos de la consulta
                    datos = cursor.fetchone()
                    print(datos)
                    self.leNombreUsuario.setText(str(datos[1]))
                    self.leContra.setText(str(datos[2]))
                    self.cbGrupo.setCurrentText(str(datos[3]))
                    if datos[5] == 1:
                        self.cbEstado.setCurrentText("Activo")
                    elif datos[5] == 0:
                        self.cbEstado.setCurrentText("Inactivo")
                    self.leEmail.setText(datos[4])
                    cursor.close()
                    conn.close()
                else:
                    QMessageBox.warning(self, "ID inválido", "El numero de usuario no existe.")
        except Error as e:
            print(e)

    def guardarRegistroModificado(self):
        self.nombre = self.leNombreUsuario.text()
        if self.nombre=="":
            QMessageBox.about(self, "Error", "No hay usuario seleccionado. Presione el boton de modificar")
            return
        else:
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                self.nombre = self.leNombreUsuario.text()
                self.contraseña = self.leContra.text()
                self.email = self.leEmail.text()
                self.grupo = self.cbGrupo.currentText()
                self.estado = self.cbEstado.currentText()
                if self.estado == "Activo":
                    self.estado=1
                else:
                    self.estado=0
                self.id = int(self.id)
                consulta = "UPDATE usuarios SET nombreUsuario = %s, contraseña = %s, grupo = %s, email = %s, estado = %s, fechaModificacion=NOW() WHERE idusuarios = %s"
                datos = (self.nombre, self.contraseña, self.grupo, self.email, self.estado, self.id)

                cursor.execute(consulta, datos)
                conn.commit()  # Añadido para confirmar los cambios en la base de datos

                QMessageBox.about(self, "Éxito", "Se modificaron los datos")
            except Error as e:
                print(e)
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

            #guardar en el historial
            try:
                with open('userlog.txt', 'r') as archivo:
                    primera_linea = archivo.readline()
                    palabras = primera_linea.split()
                    idusuariolog = palabras[0]
            except Error as e:
                print(e)

            try:
                nombre_usuario = self.leNombreUsuario.text()
                idparatxt = int(idusuariolog)
                detalle = "Modificó los datos de un usuario"
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
    ventana = ClaseModificarUsuario()
    ventana.show()
    app.exec_()

if __name__ == '__main__':
    main()