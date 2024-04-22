import datetime
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from ventana1 import Ui_Form
from PGenerarTransaccion import ClasePGenerarTransaccion
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db



class ClasePTransacciones(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(ClasePTransacciones, self).__init__(parent)
        loadUi("PTransacciones.ui", self)
        self.configurar()
        self.btnActualizar.clicked.connect(self.configurar)
        self.btnFiltrar.clicked.connect(self.filtrar)
        self.sbCbu.setRange(0,2147483647)
        self.btnNoFiltros.clicked.connect(self.configurar)

    def configurar(self):
        self.btnSalir.clicked.connect(self.close)
        self.btnGenerarTransaccion.clicked.connect(self.generarTransaccion)
        self.sbCbu.setEnabled(False)
        self.dteDesde.setEnabled(False)
        self.dteHasta.setEnabled(False)
        self.checkFc.stateChanged.connect(self.actualizar_estilo)
        self.checkFf.stateChanged.connect(self.actualizar_estilo)
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta="SELECT * FROM transacciones ORDER BY fechaYhoraInicio DESC"
            cursor.execute(consulta)

            # Obtener los datos de la consulta
            datos = cursor.fetchall()

            # Obtener el número de filas y columnas
            num_filas = len(datos)
            num_columnas = len(cursor.column_names)

            # Configurar el número de filas y columnas de la tabla
            self.tableTransacciones.setRowCount(num_filas)
            self.tableTransacciones.setColumnCount(num_columnas)


            # Rellenar la tabla con los datos
            for fila, fila_datos in enumerate(datos):
                for columna, valor in enumerate(fila_datos):
                    self.tableTransacciones.setItem(fila, columna, QTableWidgetItem(str(valor)))
                    if isinstance(valor, datetime.date):
                            valor = valor.strftime("%d-%m-%Y %H:%M:%S")
                            self.tableTransacciones.setItem(fila, columna, QTableWidgetItem(str(valor)))
            # ajusta el tamaño de las celdas al contenido
            self.tableTransacciones.resizeRowsToContents()
            self.tableTransacciones.resizeColumnsToContents()
            # Aplicar hoja de estilo para hacer negrita los títulos de las columnas
            header_font = QFont()
            header_font.setBold(True)
            self.tableTransacciones.horizontalHeader().setFont(header_font)
            #aumentar el espaciado entre columnas
            for col in range(self.tableTransacciones.columnCount()):
                self.tableTransacciones.setColumnWidth(col, self.tableTransacciones.columnWidth(col) + 15)




        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    def generarTransaccion(self):
        self.PGenerarTransaccion = ClasePGenerarTransaccion()  # Crea una instancia
        self.PGenerarTransaccion.show()

    def filtrar(self):
        if self.checkFc.isChecked() and not self.checkFf.isChecked():
            cbuFiltrar = self.sbCbu.text()

            if cbuFiltrar == "":
                QMessageBox.about(self, "ERROR", "Ingrese un usuario para filtrar")
                return  # Sale de la función si no se ingresó un usuario

            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "SELECT * FROM transacciones WHERE idcuentaorigen = %s ORDER BY fechaYhoraInicio DESC"
                datos = (cbuFiltrar,)
                cursor.execute(consulta, datos)
                resultado = cursor.fetchall()

                if not resultado:
                    QMessageBox.information(self, "ERROR", "no hay transacciones para ese cbu")
                    return
                else:
                    num_filas = len(resultado)
                    num_columnas = len(cursor.column_names)

                    # Configurar el número de filas y columnas de la tabla
                    self.tableTransacciones.setRowCount(num_filas)
                    self.tableTransacciones.setColumnCount(num_columnas)


                    # Rellenar la tabla con los resultados
                    for fila, fila_datos in enumerate(resultado):
                        for columna, valor in enumerate(fila_datos):
                            self.tableTransacciones.setItem(fila, columna, QTableWidgetItem(str(valor)))
                            if isinstance(valor, datetime.date):
                                valor = valor.strftime("%d-%m-%Y %H:%M:%S")
                                self.tableTransacciones.setItem(fila, columna, QTableWidgetItem(str(valor)))
            except Exception as e:
                print(f"Error: {e}")
                QMessageBox.about(self, "Error", "Hubo un error al conectarse a la base de datos")
            finally:
                cursor.close()
                conn.close()

        # FILTRA SOLO POR FECHA
        if not self.checkFc.isChecked() and self.checkFf.isChecked():
            fechaDesde = self.dteDesde.dateTime()
            fechaHasta = self.dteHasta.dateTime()
            # Convierte las variables QDateTime en cadenas en el formato SQL
            fechaDesde = fechaDesde.toString("yyyy-MM-dd HH:mm:ss")
            fechaHasta = fechaHasta.toString("yyyy-MM-dd HH:mm:ss")
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "SELECT * FROM transacciones WHERE fechaYhoraInicio>=%s and fechaYhoraInicio<=%s ORDER BY fechaYhoraInicio DESC"
                datos = (fechaDesde,fechaHasta)
                cursor.execute(consulta, datos)
                resultado = cursor.fetchall()
                num_filas = len(resultado)
                num_columnas = len(cursor.column_names)

                if not resultado:
                    QMessageBox.information(self, "ERROR", "No hay transacciones en ese rango de fechas")
                    return

                # Configurar el número de filas y columnas de la tabla
                self.tableTransacciones.setRowCount(num_filas)
                self.tableTransacciones.setColumnCount(num_columnas)


                # Rellenar la tabla con los resultados
                for fila, fila_datos in enumerate(resultado):
                    for columna, valor in enumerate(fila_datos):
                        self.tableTransacciones.setItem(fila, columna, QTableWidgetItem(str(valor)))
                        if isinstance(valor, datetime.date):
                            valor = valor.strftime("%d-%m-%Y %H:%M:%S")
                            self.tableTransacciones.setItem(fila, columna, QTableWidgetItem(str(valor)))
            except Exception as e:
                print(f"Error: {e}")
                QMessageBox.about(self, "Error", "Hubo un error al conectarse a la base de datos")
            finally:
                cursor.close()
                conn.close()

            # FILTRA por usuario y POR FECHA
        if self.checkFc.isChecked() and self.checkFf.isChecked():
            fechaDesde = self.dteDesde.dateTime()
            fechaHasta = self.dteHasta.dateTime()
            cbuFiltrar = self.sbCbu.text()
            # Convierte las variables QDateTime en cadenas en el formato SQL
            fechaDesde = fechaDesde.toString("yyyy-MM-dd HH:mm:ss")
            fechaHasta = fechaHasta.toString("yyyy-MM-dd HH:mm:ss")
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "SELECT * FROM transacciones WHERE idcuentaorigen=%s and fechaYhoraInicio>=%s and fechaYhoraInicio<=%s ORDER BY fechaYhoraInicio DESC"
                datos = (cbuFiltrar, fechaDesde, fechaHasta)
                cursor.execute(consulta, datos)
                resultado = cursor.fetchall()
                num_filas = len(resultado)
                num_columnas = len(cursor.column_names)

                if not resultado:
                    QMessageBox.information(self, "ERROR", "No hay transacciones en ese rango de fechas o para ese cbu")
                    return
                # Configurar el número de filas y columnas de la tabla
                self.tableTransacciones.setRowCount(num_filas)
                self.tableTransacciones.setColumnCount(num_columnas)


                # Rellenar la tabla con los resultados
                for fila, fila_datos in enumerate(resultado):
                    for columna, valor in enumerate(fila_datos):
                        self.tableTransacciones.setItem(fila, columna, QTableWidgetItem(str(valor)))
                        if isinstance(valor, datetime.date):
                            valor = valor.strftime("%d-%m-%Y %H:%M:%S")
                            self.tableTransacciones.setItem(fila, columna, QTableWidgetItem(str(valor)))
            except Exception as e:
                print(f"Error: {e}")
                QMessageBox.about(self, "Error", "Hubo un error al conectarse a la base de datos")
            finally:
                cursor.close()
                conn.close()

    def actualizar_estilo(self):
        if self.checkFc.isChecked():
            self.actualizar_estilo_widget(self.sbCbu, True)
            self.sbCbu.setEnabled(True)
        else:
            self.actualizar_estilo_widget(self.sbCbu, False)
            self.sbCbu.setEnabled(False)

        if self.checkFf.isChecked():
            self.actualizar_estilo_widget(self.dteDesde, True)
            self.actualizar_estilo_widget(self.dteHasta, True)
            self.dteDesde.setEnabled(True)
            self.dteHasta.setEnabled(True)

        else:
            self.actualizar_estilo_widget(self.dteDesde, False)
            self.actualizar_estilo_widget(self.dteHasta, False)
            self.dteDesde.setEnabled(False)
            self.dteHasta.setEnabled(False)

    def actualizar_estilo_widget(self, widget, seleccionado):
        if seleccionado:
            widget.setStyleSheet("background-color: rgb(255, 252, 185);")  # Cambia el color de fondo a verde
        else:
            widget.setStyleSheet("")

def main():
    app = QApplication(sys.argv)
    ventana = ClasePTransacciones()
    ventana.show()
    app.exec_()


if __name__ == '__main__':
    main()
