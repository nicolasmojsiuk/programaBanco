import sys
import datetime

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from ventana1 import Ui_Form
from nuevoCliente import ClaseNuevoCliente
from estadisticasclientes import ClasePEstadisticasClientes
from modificarCliente import ClaseModificarCliente
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db

class ClasePCliente(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(ClasePCliente, self).__init__(parent)
        loadUi("PCliente.ui", self)
        self.configurar()
        self.btnActualizar.clicked.connect(self.configurar)

    def configurar(self):
        self.btnCrearCliente.clicked.connect(self.AbrirPNuevo)
        self.btnModificarCliente.clicked.connect(self.AbrirPModificar)
        self.btnEliminarCliente.clicked.connect(self.EliminarCliente)
        self.btnEstadisticas_2.clicked.connect(self.verEstadisticas)
        self.btnBuscar.clicked.connect(self.buscarCliente)
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT * FROM clientes"
            cursor.execute(consulta)

            # Obtener los datos de la consulta
            datos = cursor.fetchall()

            # Obtener el número de filas y columnas
            num_filas = len(datos)
            num_columnas = len(cursor.column_names)

            # Configurar el número de filas y columnas de la tabla
            self.tableClientes.setRowCount(num_filas)
            self.tableClientes.setColumnCount(num_columnas)
            # Rellenar la tabla con los datos
            for fila, fila_datos in enumerate(datos):
                for columna, valor in enumerate(fila_datos):
                    if valor == 0 and columna==6:
                        self.tableClientes.setItem(fila, columna, QTableWidgetItem("inactivo"))
                    elif valor == 1 and columna==6:
                        self.tableClientes.setItem(fila, columna, QTableWidgetItem("activo"))
                    elif isinstance(valor, datetime.date):
                        valor = valor.strftime("%d-%m-%Y")
                        self.tableClientes.setItem(fila, columna, QTableWidgetItem(str(valor)))
                    elif columna == 2:  # Columna de DNI
                        valor_formateado = '{:,.0f}'.format(float(valor)).replace(',', '.')
                        self.tableClientes.setItem(fila, columna, QTableWidgetItem(str(valor_formateado)))
                    elif columna == 1:  # Columna de nombres
                        valor_formateado = valor.title()
                        self.tableClientes.setItem(fila, columna, QTableWidgetItem(str(valor_formateado)))
                    else:
                        self.tableClientes.setItem(fila, columna, QTableWidgetItem(str(valor)))

            # ajusta el tamaño de las celdas al contenido
            self.tableClientes.resizeRowsToContents()
            self.tableClientes.resizeColumnsToContents()
            # Aplicar negrita a los títulos de las columnas
            header_font = QFont()
            header_font.setBold(True)
            self.tableClientes.horizontalHeader().setFont(header_font)
            # aumentar el espaciado entre columnas
            for col in range(self.tableClientes.columnCount()):
                self.tableClientes.setColumnWidth(col, self.tableClientes.columnWidth(col) + 15)

            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def AbrirPNuevo(self):
        self.nuevoCliente = ClaseNuevoCliente()
        self.nuevoCliente.show()

    def AbrirPModificar(self):
        self.modificarCliente = ClaseModificarCliente()
        self.modificarCliente.show()

    def verEstadisticas(self):
        self.verestadistica = ClasePEstadisticasClientes()
        self.verestadistica.show()

    def EliminarCliente(self):
        # Pide al usuario el ID que desea eliminar
        idus, ok = QInputDialog.getInt(self, "Eliminar cliente", "Ingrese el número del cliente a eliminar:")

        if ok:
            try:
                db_config = leer_configuracion_db()
                conn = MySQLConnection(**db_config)
                cursor = conn.cursor()

                # Verifica si el cliente existe
                consulta = "SELECT nombre FROM clientes WHERE idclientes = %s"
                cursor.execute(consulta, (idus,))
                resultado = cursor.fetchone()

                if resultado:
                    # Obtiene el nombre del cliente
                    nombre_cliente = resultado[0]

                    # Crea un cuadro de diálogo de confirmación
                    confirmacion_dialog = QMessageBox()
                    confirmacion_dialog.setWindowTitle("Confirmación de Eliminación")
                    confirmacion_dialog.setIcon(QMessageBox.Question)
                    confirmacion_dialog.setText(f"¿Está seguro de eliminar al cliente: {nombre_cliente}?")
                    confirmacion_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

                    result = confirmacion_dialog.exec_()

                    if result == QMessageBox.Yes:
                        # Elimina al cliente
                        consulta = "DELETE FROM clientes WHERE idclientes = %s"
                        cursor.execute(consulta, (idus,))
                        conn.commit()
                        print("Eliminación completada")

                        # ---------------obtener usuario logueado----------------
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
                            detalle = "Elimino un cliente"
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
                    else:
                        print("Eliminación cancelada por el usuario.")
                else:
                    QMessageBox.about(self, "Cliente no existe", "El cliente con ID " + str(idus) + " no existe.")
            except Error as e:
                print(e)

    def buscarCliente(self):
        nombre_a_buscar = self.leBuscar.text()
        if nombre_a_buscar:
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "SELECT * FROM clientes WHERE nombre = %s or dni=%s"
                cursor.execute(consulta, (nombre_a_buscar, nombre_a_buscar))

                # Obtener los datos de la consulta
                datos = cursor.fetchall()

                # Obtener el número de filas y columnas
                num_filas = len(datos)
                num_columnas = len(cursor.description)

                # Configurar el número de filas y columnas de la tabla
                self.tableClientes.setRowCount(num_filas)
                self.tableClientes.setColumnCount(num_columnas)

                # Rellenar la tabla con los datos
                for fila, fila_datos in enumerate(datos):
                    for columna, valor in enumerate(fila_datos):
                        if valor == 0:
                            self.tableClientes.setItem(fila, columna, QTableWidgetItem("inactivo"))
                        elif valor == 1:
                            self.tableClientes.setItem(fila, columna, QTableWidgetItem("activo"))
                        elif isinstance(valor, datetime.date):
                            valor = valor.strftime("%d-%m-%Y")  # Cambiar formato de fecha
                        elif columna == 2:
                            valor_formateado = '{:,.0f}'.format(float(valor)).replace(',', '.')
                            self.tableClientes.setItem(fila, columna, QTableWidgetItem(str(valor_formateado)))
                        elif columna == 1:  # Columna de nombres
                            valor_formateado = valor.title()
                            self.tableClientes.setItem(fila, columna, QTableWidgetItem(str(valor_formateado)))
                        else:
                            self.tableClientes.setItem(fila, columna, QTableWidgetItem(str(valor)))

                cursor.close()
                conn.close()
            except Error as e:
                print(e)


def main():
    app = QApplication(sys.argv)
    ventana = ClasePCliente()
    ventana.show()
    app.exec_()


if __name__ == '__main__':
    main()