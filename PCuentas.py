import datetime
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QInputDialog
from PyQt5.uic import loadUi
from ventana1 import Ui_Form
from PNuevaCuenta import ClasePnuevaCuenta
from PModCuenta import ClasePModCuenta
from PEstadisticasCuentas import ClasePEstadisticasCuentas
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db



class ClasePCuentas(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(ClasePCuentas, self).__init__(parent)
        loadUi("Pcuentas.ui", self)
        self.configurar()
        self.btnActualizar.clicked.connect(self.configurar)

    def configurar(self):
        self.btnCrear.clicked.connect(self.abrirPantallaNuevaCuenta)
        self.btnEstadisticas.clicked.connect(self.abrirPantallaEstadisticas)
        self.btnBuscar.clicked.connect(self.buscar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnModificar.clicked.connect(self.modificar)




        #cargar la base de datos en la tabla
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT cuentas.*, clientes.nombre FROM cuentas JOIN clientes ON cuentas.idcliente = clientes.idclientes;"
            cursor.execute(consulta)

            # Obtener los datos de la consulta
            datos = cursor.fetchall()

            # Convertir los valores numéricos a cadenas de texto
            datos_modificados = []
            for i in range(0, len(datos)):
                fila_modificada = list(datos[i])
                if fila_modificada[3] == 1:
                    fila_modificada[3] = "Cuenta corriente en pesos"
                elif fila_modificada[3] == 2:
                    fila_modificada[3] = "Caja de ahorro en pesos"
                elif fila_modificada[3] == 3:
                    fila_modificada[3] = "Caja de ahorro en reales"
                elif fila_modificada[3] == 4:
                    fila_modificada[3] = "Caja de ahorro en dólares"
                elif fila_modificada[3] == 5:
                    fila_modificada[3] = "caja de ahorro en euros"
                else:
                    fila_modificada[3] = "Tipo de cuenta desconocido"
                datos_modificados.append(tuple(fila_modificada))

            # Obtener el número de filas y columnas de la tabla
            num_filas = len(datos_modificados)
            num_columnas = len(cursor.column_names)

            # Configurar el número de filas y columnas de la tabla
            self.tableCuentas.setRowCount(num_filas)
            self.tableCuentas.setColumnCount(num_columnas)

            # Rellenar la tabla con los datos
            for fila, fila_datos in enumerate(datos_modificados):
                for columna, valor in enumerate(fila_datos):
                    if isinstance(valor, datetime.date):
                        valor = valor.strftime("%d-%m-%Y")
                        self.tableCuentas.setItem(fila, columna, QTableWidgetItem(str(valor)))
                    self.tableCuentas.setItem(fila, columna, QTableWidgetItem(str(valor)))

            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def buscar(self):
        busqueda=self.leBuscar.text()
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT cuentas.*, clientes.nombre FROM cuentas JOIN clientes ON cuentas.idcliente = clientes.idclientes WHERE cuentas.cbu=%s OR cuentas.alias=%s OR clientes.nombre=%s"
            datos=(busqueda,busqueda,busqueda)
            cursor.execute(consulta,datos)

            # Obtener los datos de la consulta
            datos = cursor.fetchall()
            print(datos)
            if datos==[]:
                QMessageBox.about(self, "Búsqueda", "No hay resultados para la busqueda")
                return

            # Convertir los valores numéricos a cadenas de texto
            datos_modificados = []
            for i in range(0, len(datos)):
                fila_modificada = list(datos[i])
                if fila_modificada[3] == 1:
                    fila_modificada[3] = "Cuenta corriente en pesos"
                elif fila_modificada[3] == 2:
                    fila_modificada[3] = "Caja de ahorro en pesos"
                elif fila_modificada[3] == 3:
                    fila_modificada[3] = "Caja de ahorro en reales"
                elif fila_modificada[3] == 4:
                    fila_modificada[3] = "Caja de ahorro en dólares"
                elif fila_modificada[3] == 5:
                    fila_modificada[3] = "caja de ahorro en euros"
                else:
                    fila_modificada[3] = "Tipo de cuenta desconocido"
                datos_modificados.append(tuple(fila_modificada))

            # Obtener el número de filas y columnas de la tabla
            num_filas = len(datos_modificados)
            num_columnas = len(cursor.column_names)

            # Configurar el número de filas y columnas de la tabla
            self.tableCuentas.setRowCount(num_filas)
            self.tableCuentas.setColumnCount(num_columnas)

            # Rellenar la tabla con los datos
            for fila, fila_datos in enumerate(datos_modificados):
                for columna, valor in enumerate(fila_datos):
                    self.tableCuentas.setItem(fila, columna, QTableWidgetItem(str(valor)))

            cursor.close()
            conn.close()
        except Error as e:
            print(e)

    def eliminar(self):
        try:
            # Pide al usuario el ID que desea eliminar
            cbu, ok = QInputDialog.getText(self, "Eliminar cuenta", "Ingrese el cbu de la cuenta a eliminar:")
            if not ok:
                return
            if ok:
                # Convierte el texto del ID a un número entero
                cbu = int(cbu)
                try:
                    dbconfig = leer_configuracion_db()
                    conn = MySQLConnection(**dbconfig)
                    cursor = conn.cursor()
                    consulta = "SELECT cuentas.cbu, clientes.nombre FROM cuentas JOIN clientes ON cuentas.idcliente = clientes.idclientes WHERE cuentas.cbu=%s"
                    datos = (cbu,)
                    cursor.execute(consulta, datos)
                    # Obtener los datos de la consulta
                    datos = cursor.fetchone()
                    print(datos)
                    nombreCliente=datos[1]
                    if datos == [] or datos==None:
                        QMessageBox.about(self, "Error", "No hay cuenta con el cbu indicado")
                        return
                    cursor.close()
                    conn.close()
                except Error as e:
                    print(e)



                # Crea un cuadro de diálogo de confirmación
                confirmation_dialog = QMessageBox()
                confirmation_dialog.setWindowTitle("Confirmación de Eliminación")
                confirmation_dialog.setIcon(QMessageBox.Question)  # Icono de pregunta

                # Configura el mensaje de confirmación con el nombre del usuario
                message = f"¿Está seguro de eliminar la cuenta {cbu} del cliente: {nombreCliente}?"
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
                        consulta = "DELETE FROM cuentas WHERE cbu = %s"
                        datos = (cbu,)
                        cursor.execute(consulta, datos)
                        conn.commit()
                    except Error as e:
                        print(e)
                elif confirmation_dialog.clickedButton() == cancel_button:
                    QMessageBox.about(self, "Cancelado", "Se canceló la eliminación")
        except Error as e:
            print(e)
#------------------------guardar en el historial--------------------------------------
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
            detalle = "Elimino una cuenta"
            masdetalle = f"Cuenta: {cbu} del cliente {nombreCliente}"
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


    def modificar(self):
        self.PModCuenta = ClasePModCuenta()
        self.PModCuenta.show()
    def abrirPantallaNuevaCuenta(self):
        self.PNuevaCuenta = ClasePnuevaCuenta()  # Crea una instancia
        self.PNuevaCuenta.show()

    def abrirPantallaEstadisticas(self):
        self.PEstadisticas = ClasePEstadisticasCuentas()  # Crea una instancia
        self.PEstadisticas.show()
def main():
    app = QApplication(sys.argv)
    ventana = ClasePCuentas()
    ventana.show()
    app.exec_()


if __name__ == '__main__':
    main()
