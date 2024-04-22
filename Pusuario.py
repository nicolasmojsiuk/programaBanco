import datetime
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QInputDialog, QMessageBox
from PyQt5.uic import loadUi
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db
from nuevoUsuario import ClaseNuevoUsuario
from modificarUsuario import ClaseModificarUsuario



class ClasePusuarios(QMainWindow):
    def __init__(self, parent=None):
        super(ClasePusuarios, self).__init__(parent)
        loadUi("Pusuarios.ui", self)
        self.configurar()
        self.btnActualizar.clicked.connect(self.configurar)
        self.btnEliminar.clicked.connect(self.eliminarUsuario)
        self.btnModificar.clicked.connect(self.modificarUsuario)
        self.btnBuscar.clicked.connect(self.buscar)

    def configurar(self):
        self.btncrearu.clicked.connect(self.abrirPantallaNuevoUsuario)
        dbconfig = leer_configuracion_db()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        consulta = "SELECT idusuarios, nombreUsuario, grupo, email, estado, fechaCreacion, fechaModificacion, ultimoAccesso FROM usuarios"
        cursor.execute(consulta)

        # Obtener los datos de la consulta
        datos = cursor.fetchall()

        # Obtener el número de filas y columnas
        num_filas = len(datos)
        num_columnas = len(cursor.column_names)

        # Configurar el número de filas y columnas de la tabla
        self.tableUsuarios.setRowCount(num_filas)
        self.tableUsuarios.setColumnCount(num_columnas)

        # Rellenar la tabla con los datos
        for fila, fila_datos in enumerate(datos):
            for columna, valor in enumerate(fila_datos):
                if valor is None:
                    valor = "-"
                elif isinstance(valor, datetime.date):
                    valor = valor.strftime("%d-%m-%Y")  # Cambiar formato de fecha
                elif valor == 0 and columna==4:
                    valor = "Inactivo"
                elif valor == 1 and columna==4:
                    valor = "Activo"
                self.tableUsuarios.setItem(fila, columna, QTableWidgetItem(str(valor)))

        cursor.close()
        conn.close()

        # ajusta el tamaño de las celdas al contenido
        self.tableUsuarios.resizeRowsToContents()
        self.tableUsuarios.resizeColumnsToContents()
        # Aplicar negrita a los títulos de las columnas
        header_font = QFont()
        header_font.setBold(True)
        self.tableUsuarios.horizontalHeader().setFont(header_font)
        # aumentar el espaciado entre columnas
        for col in range(self.tableUsuarios.columnCount()):
            self.tableUsuarios.setColumnWidth(col, self.tableUsuarios.columnWidth(col) + 15)

    def buscar(self):
        nombreBuscar=self.leBuscar.text()
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT idusuarios, nombreUsuario, grupo, email, estado, fechaCreacion, fechaModificacion, ultimoAccesso FROM usuarios where nombreUsuario=%s"
            datos=(nombreBuscar,)
            cursor.execute(consulta,datos)

            # Obtener los datos de la consulta
            datos = cursor.fetchall()
            if datos==[] or datos==None:
                return
            # Obtener el número de filas y columnas
            num_filas = len(datos)
            num_columnas = len(cursor.column_names)

            # Configurar el número de filas y columnas de la tabla
            self.tableUsuarios.setRowCount(num_filas)
            self.tableUsuarios.setColumnCount(num_columnas)

            # Rellenar la tabla con los datos
            for fila, fila_datos in enumerate(datos):
                for columna, valor in enumerate(fila_datos):
                    if valor is None:
                        valor = "-"
                    elif isinstance(valor, datetime.date):
                        valor = valor.strftime("%d-%m-%Y")  # Cambiar formato de fecha
                    elif valor == 0 and columna == 4:
                        valor = "Inactivo"
                    elif valor == 1 and columna == 4:
                        valor = "Activo"
                    self.tableUsuarios.setItem(fila, columna, QTableWidgetItem(str(valor)))
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    def abrirPantallaNuevoUsuario(self):
        try:
            self.nuevoUsuario = ClaseNuevoUsuario()  # Crea una instancia
            self.nuevoUsuario.show()  # Muestra la ventana de ClaseNuevoUsuario
        except Exception as e:
            print("Error al abrir la segunda ventana:", str(e))


    def eliminarUsuario(self):
        try:
            # Pide al usuario el ID que desea eliminar
            id, ok = QInputDialog.getText(self, "Eliminar usuario", "Ingrese el ID del usuario a eliminar:")
            if ok:
                # Convierte el texto del ID a un número entero
                id = int(id)
                print(id)
                # Obtén el nombre del usuario basado en el ID
                try:
                    db_config = leer_configuracion_db()
                    conn = MySQLConnection(**db_config)
                    cursor = conn.cursor()
                    consulta = "SELECT nombreUsuario FROM usuarios WHERE idusuarios = %s"
                    datos = (id,)
                    cursor.execute(consulta, datos)
                    nombreEliminar=cursor.fetchone()
                    if nombreEliminar==None or nombreEliminar==[]:
                        QMessageBox.about(self, "Error", "El numero de usuario no existe")
                        return
                    else:
                        nombreEliminar=nombreEliminar[0]
                except Error as e:
                    print(e)
                finally:
                    cursor.close()
                    conn.close()

                # Crea un cuadro de diálogo de confirmación
                confirmation_dialog = QMessageBox()
                confirmation_dialog.setWindowTitle("Confirmación de Eliminación")
                confirmation_dialog.setIcon(QMessageBox.Question)  # Icono de pregunta

                # Configura el mensaje de confirmación con el nombre del usuario
                message = f"¿Está seguro de eliminar al usuario {nombreEliminar}?"
                confirmation_dialog.setText(message)

                # Agrega botones personalizados ("Sí" y "No")
                confirm_button = confirmation_dialog.addButton("Sí", QMessageBox.AcceptRole)
                cancel_button = confirmation_dialog.addButton("No", QMessageBox.RejectRole)

                # Muestra el cuadro de diálogo
                confirmation_dialog.exec_()

                # Verifica el botón presionado
                if confirmation_dialog.clickedButton() == confirm_button:
                    # Elimina al usuario
                    try:
                        db_config = leer_configuracion_db()
                        conn = MySQLConnection(**db_config)
                        cursor = conn.cursor()
                        consulta = "DELETE FROM usuarios WHERE idusuarios = %s"
                        datos = (id,)
                        cursor.execute(consulta, datos)
                        conn.commit()
                        print("Eliminación completada")
                        # GUARDAR EN EL HISTORIAL
                        try:
                            with open("userlog.txt", "r") as archivo:
                                # Escribe contenido en el archivo
                                contenido = archivo.read()
                            contenido = contenido.split()
                            # datos para guardar en el historial
                            iduparahistorial = int(contenido[0])
                            detalle = "ELimino a el usuario: "
                            masdetalle = "nombre: "+nombreEliminar
                            dbconfig = leer_configuracion_db()
                            conn = MySQLConnection(**dbconfig)
                            cursor = conn.cursor()
                            consulta = "INSERT INTO historialusuarios (idusuario, detalle, fecha, masdetalle) VALUES (%s, %s, NOW(), %s)"
                            datos = (iduparahistorial, detalle, masdetalle)
                            cursor.execute(consulta, datos)
                            print("se guardo en el historial")
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
                elif confirmation_dialog.clickedButton() == cancel_button:
                    QMessageBox.about(self, "Cancelado", "Se canceló la eliminación")
        except Error as e:
            print(e)


    def modificarUsuario(self):
        try:
            self.modificarUsuario = ClaseModificarUsuario()  # Crea una instancia
            self.modificarUsuario.show()  # Muestra la ventana de ClaseNuevoUsuario
        except Exception as e:
            print("Error al abrir la segunda ventana:", str(e))





def main():
    app = QApplication(sys.argv)
    ventana = ClasePusuarios()
    ventana.show()
    app.exec_()

if __name__ == '__main__':
    main()
