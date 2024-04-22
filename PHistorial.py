import sys
import datetime

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from ventana1 import Ui_Form
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db

class ClasePhistorial(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(ClasePhistorial, self).__init__(parent)
        loadUi("PHistorial.ui", self)
        self.configurar()
    def configurar(self):
        self.leUsuario.setEnabled(False)
        self.dteDesde.setEnabled(False)
        self.dteHasta.setEnabled(False)
        self.btnSalir.clicked.connect(self.close)

        #boton para sacar filtros
        self.btnNoFiltros.clicked.connect(self.borrarfiltros)

        #verifica la seleccion de check box de filtros
        self.checkFu.stateChanged.connect(self.actualizar_estilo)
        self.checkFf.stateChanged.connect(self.actualizar_estilo)

        try:
            # Cargar la tabla de historial
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT historialusuarios.*, usuarios.nombreUsuario FROM historialusuarios INNER JOIN usuarios ON historialusuarios.idusuario = usuarios.idusuarios ORDER BY historialusuarios.fecha DESC"

            cursor.execute(consulta)

            # Obtener los datos de la consulta
            datos = cursor.fetchall()

            # Obtener el número de filas y columnas
            num_filas = len(datos)
            num_columnas = len(cursor.column_names)

            # Configurar el número de filas y columnas de la tabla
            self.tableHistorial.setRowCount(num_filas)
            self.tableHistorial.setColumnCount(num_columnas)

            # Rellenar la tabla con los datos, reemplazando los valores None con guiones
            for fila, fila_datos in enumerate(datos):
                for columna, valor in enumerate(fila_datos):
                    if valor is None:
                        self.tableHistorial.setItem(fila, columna, QTableWidgetItem("-"))
                    elif isinstance(valor, datetime.datetime):
                        # Cambiar el formato de la fecha
                        valor_formateado = valor.strftime('%d-%m-%Y %H:%M:%S')
                        self.tableHistorial.setItem(fila, columna, QTableWidgetItem(valor_formateado))
                    else:
                        self.tableHistorial.setItem(fila, columna, QTableWidgetItem(str(valor)))
            self.tableHistorial.resizeRowsToContents()
            self.tableHistorial.resizeColumnsToContents()
            # Aplicar hoja de estilo para hacer negrita los títulos de las columnas
            header_font = QFont()
            header_font.setBold(True)
            self.tableHistorial.horizontalHeader().setFont(header_font)

        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    #activa los campos de fuiltros y cambia el color de los filtros para saber que estan activados
    def actualizar_estilo(self):
        if self.checkFu.isChecked():
            self.actualizar_estilo_widget(self.leUsuario, True)
            self.leUsuario.setEnabled(True)
            self.btnFiltrar.clicked.connect(self.filtrar)
        else:
            self.actualizar_estilo_widget(self.leUsuario, False)
            self.leUsuario.setEnabled(False)
            self.btnFiltrar.clicked.connect(self.filtrar)

        if self.checkFf.isChecked():
            self.actualizar_estilo_widget(self.dteDesde, True)
            self.actualizar_estilo_widget(self.dteHasta, True)
            self.dteDesde.setEnabled(True)
            self.dteHasta.setEnabled(True)
            self.btnFiltrar.clicked.connect(self.filtrar)

        else:
            self.actualizar_estilo_widget(self.dteDesde, False)
            self.actualizar_estilo_widget(self.dteHasta, False)
            self.dteDesde.setEnabled(False)
            self.dteHasta.setEnabled(False)
            self.btnFiltrar.clicked.connect(self.filtrar)
    def actualizar_estilo_widget(self, widget, seleccionado):
        if seleccionado:
            widget.setStyleSheet("background-color: rgb(255, 252, 185);")  # Cambia el color de fondo a verde
        else:
            widget.setStyleSheet("")  # Restablece el estilo al predeterminado


    def filtrar(self):
        #FILTRA SOLO POR USUARIO
        if self.checkFu.isChecked() and not self.checkFf.isChecked():
            usuarioAfiltrar = self.leUsuario.text()

            if usuarioAfiltrar == "":
                QMessageBox.about(self, "ERROR", "Ingrese un usuario para filtrar")
                return  # Sale de la función si no se ingresó un usuario

            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "SELECT historialusuarios.*, usuarios.nombreUsuario FROM historialusuarios INNER JOIN usuarios ON historialusuarios.idusuario = usuarios.idusuarios WHERE usuarios.nombreUsuario = %s ORDER BY historialusuarios.fecha DESC"
                datos = (usuarioAfiltrar,)
                cursor.execute(consulta, datos)
                resultado = cursor.fetchall()

                if not resultado:
                    QMessageBox.about(self, "ERROR", "Este usuario no existe en la base de datos")
                else:
                    num_filas = len(resultado)
                    num_columnas = len(cursor.column_names)

                    # Configurar el número de filas y columnas de la tabla
                    self.tableHistorial.setRowCount(num_filas)
                    self.tableHistorial.setColumnCount(num_columnas)


                    # Rellenar la tabla con los resultados
                    for fila, fila_datos in enumerate(resultado):
                        for columna, valor in enumerate(fila_datos):
                            self.tableHistorial.setItem(fila, columna, QTableWidgetItem(str(valor)))
            except Exception as e:
                print(f"Error: {e}")
                QMessageBox.about(self, "Error", "Hubo un error al conectarse a la base de datos")
            finally:
                cursor.close()
                conn.close()
        # FILTRA SOLO POR FECHA
        if not self.checkFu.isChecked() and self.checkFf.isChecked():
            fechaDesde = self.dteDesde.dateTime()
            fechaHasta = self.dteHasta.dateTime()
            # Convierte las variables QDateTime en cadenas en el formato SQL
            fechaDesde = fechaDesde.toString("yyyy-MM-dd HH:mm:ss")
            fechaHasta = fechaHasta.toString("yyyy-MM-dd HH:mm:ss")
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "SELECT historialusuarios.*, usuarios.nombreUsuario FROM historialusuarios INNER JOIN usuarios ON historialusuarios.idusuario = usuarios.idusuarios WHERE historialusuarios.fecha>%s AND historialusuarios.fecha<%s ORDER BY historialusuarios.fecha DESC"
                datos = (fechaDesde,fechaHasta)
                cursor.execute(consulta, datos)
                resultado = cursor.fetchall()
                num_filas = len(resultado)
                num_columnas = len(cursor.column_names)

                # Configurar el número de filas y columnas de la tabla
                self.tableHistorial.setRowCount(num_filas)
                self.tableHistorial.setColumnCount(num_columnas)


                # Rellenar la tabla con los resultados
                for fila, fila_datos in enumerate(resultado):
                    for columna, valor in enumerate(fila_datos):
                        self.tableHistorial.setItem(fila, columna, QTableWidgetItem(str(valor)))
            except Exception as e:
                print(f"Error: {e}")
                QMessageBox.about(self, "Error", "Hubo un error al conectarse a la base de datos")
            finally:
                cursor.close()
                conn.close()

            # FILTRA por usuario y POR FECHA
        if self.checkFu.isChecked() and self.checkFf.isChecked():
            fechaDesde = self.dteDesde.dateTime()
            fechaHasta = self.dteHasta.dateTime()
            usuarioAfiltrar = self.leUsuario.text()
            # Convierte las variables QDateTime en cadenas en el formato SQL
            fechaDesde = fechaDesde.toString("yyyy-MM-dd HH:mm:ss")
            fechaHasta = fechaHasta.toString("yyyy-MM-dd HH:mm:ss")
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "SELECT historialusuarios.*, usuarios.nombreUsuario FROM historialusuarios INNER JOIN usuarios ON historialusuarios.idusuario = usuarios.idusuarios WHERE usuarios.nombreUsuario = %s AND historialusuarios.fecha>%s AND historialusuarios.fecha<%s ORDER BY historialusuarios.fecha DESC"
                datos = (usuarioAfiltrar, fechaDesde, fechaHasta)
                cursor.execute(consulta, datos)
                resultado = cursor.fetchall()
                num_filas = len(resultado)
                num_columnas = len(cursor.column_names)

                # Configurar el número de filas y columnas de la tabla
                self.tableHistorial.setRowCount(num_filas)
                self.tableHistorial.setColumnCount(num_columnas)


                # Rellenar la tabla con los resultados
                for fila, fila_datos in enumerate(resultado):
                    for columna, valor in enumerate(fila_datos):
                        self.tableHistorial.setItem(fila, columna, QTableWidgetItem(str(valor)))
            except Exception as e:
                print(f"Error: {e}")
                QMessageBox.about(self, "Error", "Hubo un error al conectarse a la base de datos")
            finally:
                cursor.close()
                conn.close()


    def borrarfiltros(self):
        try:
            #cargar la tabla de historial
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT historialusuarios.*, usuarios.nombreUsuario FROM historialusuarios INNER JOIN usuarios ON historialusuarios.idusuario = usuarios.idusuarios ORDER BY historialusuarios.fecha DESC"
            cursor.execute(consulta)

            # Obtener los datos de la consulta
            datos = cursor.fetchall()

            # Obtener el número de filas y columnas
            num_filas = len(datos)
            num_columnas = len(cursor.column_names)

            # Configurar el número de filas y columnas de la tabla
            self.tableHistorial.setRowCount(num_filas)
            self.tableHistorial.setColumnCount(num_columnas)


            # Rellenar la tabla con los datos
            for fila, fila_datos in enumerate(datos):
                for columna, valor in enumerate(fila_datos):
                    self.tableHistorial.setItem(fila, columna, QTableWidgetItem(str(valor)))
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


def main():
    app = QApplication(sys.argv)
    ventana = ClasePhistorial()
    ventana.show()
    app.exec_()


if __name__ == '__main__':
    main()
