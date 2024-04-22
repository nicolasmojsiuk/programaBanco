import sys
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox
from PyQt5.uic import loadUi
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db

class ClaseModificarCliente(QMainWindow):
    def __init__(self, parent=None):
        super(ClaseModificarCliente, self).__init__(parent)
        loadUi("PmodCliente.ui", self)
        self.configurar()
        self.id = None

    def configurar(self):
        self.leNombre.setDisabled(True)
        self.leDni.setDisabled(True)
        self.cbEstado.setDisabled(True)
        self.leDireccion.setDisabled(True)
        self.leTelefono.setDisabled(True)
        self.deFechaNacimiento.setDisabled(True)
        self.btnModificar.clicked.connect(self.modificar_un_registro)
        self.btnGuardarCliente.clicked.connect(self.guardarRegistroModificado)
        self.btnClose.clicked.connect(self.close)

    def modificar_un_registro(self):
        self.leNombre.setDisabled(False)
        self.leDni.setDisabled(False)
        self.cbEstado.setDisabled(False)
        self.leDireccion.setDisabled(False)
        self.leTelefono.setDisabled(False)
        self.deFechaNacimiento.setDisabled(False)
        try:
            # Pide al usuario el ID que desea modificar
            id, ok = QInputDialog.getInt(self, "Modificar Cliente", "Ingrese el numero del cliente a modificar:")
            if ok:
                # Convierte el texto del ID a un número entero
                id = int(id)
                self.id = id
                # Obtén el nombre del cliente basado en el ID
                try:
                    dbconfig = leer_configuracion_db()
                    conn = MySQLConnection(**dbconfig)
                    cursor = conn.cursor()
                    consulta = "SELECT idclientes, nombre FROM clientes"
                    cursor.execute(consulta,)
                # Obtener los datos de la consulta
                    datos = cursor.fetchall()
                    for fila in datos:
                        if int(fila[0]) == id:
                            nombre_cliente = fila[1]
                            id=fila[0]
                            break
                        else:
                            nombre_cliente = None

                except Error as e:
                    print(e)

                if nombre_cliente is not None:
                    # Continuar con la modificación
                    dbconfig = leer_configuracion_db()
                    conn = MySQLConnection(**dbconfig)
                    cursor = conn.cursor()
                    consulta = "SELECT * FROM clientes WHERE idclientes=%s"
                    datos = (id,)
                    cursor.execute(consulta, datos)
                    # Obtener los datos de la consulta
                    datos = cursor.fetchone()

                    self.leNombre.setText(datos[1])
                    self.leDni.setText(str(datos[2]))
                    fechadenacimiento = datos[3]
                    self.deFechaNacimiento.setDate(fechadenacimiento)
                    self.leTelefono.setText(str(datos[4]))
                    if datos[6] == 1:
                        self.cbEstado.setCurrentText("Activo")
                    elif datos[6] == 0:
                        self.cbEstado.setCurrentText("Inactivo")
                    self.leDireccion.setText(datos[7])
                    cursor.close()
                    conn.close()
                else:
                    QMessageBox.warning(self, "ID inválido", "El numero de cliente no existe.")
        except Error as e:
            print(e)



    def guardarRegistroModificado(self):
        if self.id is None:
            QMessageBox.warning(self, "ID inválido", "No se ha ingresado un numero válido.")
            return

        self.nombre = self.leNombre.text()
        if self.nombre == "":
            QMessageBox.warning(self, "Error", "No hay cliente seleccionado. Presione el botón de modificar.")
        else:
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                nombre = self.leNombre.text()
                dni = int(self.leDni.text())
                estado = self.cbEstado.currentText()
                if estado == "Activo":
                    estado = 1
                elif estado == "Inactivo":
                    estado = 0
                telefono = int(self.leTelefono.text())
                direccion = self.leDireccion.text()
                fechaNacimiento = self.deFechaNacimiento.date().toString("yyyy-MM-dd")
                id = int(self.id)
                consulta = "UPDATE clientes SET nombre=%s, dni=%s, fechaDeNacimiento=%s, numeroDeTelefono=%s, estado=%s, direccion=%s WHERE idclientes = %s"
                datos = (nombre, dni, fechaNacimiento, telefono, estado, direccion, id)
                cursor.execute(consulta, datos)
                conn.commit()
                QMessageBox.about(self, "Éxito", "Se modificaron los datos")
            except Error as e:
                print(e)
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
                try:
                    with open('userlog.txt', 'r') as archivo:
                        primera_linea = archivo.readline()
                        palabras = primera_linea.split()
                        idusuariolog = palabras[0]
                except Error as e:
                    print(e)
                try:
                    nombre_cliente = self.leNombre.text()
                    idparatxt = int(idusuariolog)
                    detalle = "Modificó los datos de un cliente"
                    masdetalle = f"Nombre: {nombre_cliente}"
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
    ventana = ClaseModificarCliente()
    ventana.show()
    app.exec_()

if __name__ == '__main__':
    main()
