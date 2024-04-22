import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from ventana1 import Ui_Form
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db



class ClasePEstadisticasCuentas(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(ClasePEstadisticasCuentas, self).__init__(parent)
        loadUi("PEstadisticasCuentas.ui", self)
        self.configurar()
    def configurar(self):
        self.btnSalir.clicked.connect(self.close)
        # --------obtener estadisticas-------------
        # -------numero de cuentas----------------
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT * FROM cuentas"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            nCuentas = len(resultado)
            cursor.close()
            conn.close()
            print(nCuentas)
        except Error as e:
            print(e)
        self.lblEstadisticas.setText("N° de cuentas: "+str(nCuentas))
       
       
    # ----------------------------------------
    #--------------con saldo positivo---------------
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT * FROM cuentas WHERE balance>0"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            nCuentasP = len(resultado)
            cursor.close()
            conn.close()
        except Error as e:
            print(e)
        self.lblEstadisticas_2.setText("N° de cuentas con saldo positivo: " + str(nCuentasP))


    # ----------------------------------------
#-----------------------top 10 cuentas transacciones---------------
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()

            # Consulta para contar las transacciones por cuenta y seleccionar las 10 primeras
            consulta = """
            SELECT cu.cbu, c.nombre, COUNT(t.idtransacciones) AS num_transacciones
            FROM transacciones t
            JOIN cuentas cu ON t.idcuentaorigen = cu.cbu
            JOIN clientes c ON cu.idcliente = c.idclientes
            GROUP BY cu.cbu, c.nombre
            ORDER BY num_transacciones DESC
            LIMIT 10
            """
            cursor.execute(consulta)
            resultados = cursor.fetchall()

            print(resultados)
            for row, (cbu, Cliente, Transacciones) in enumerate(resultados):
                self.tableTop.setItem(row, 0, QTableWidgetItem(str(cbu)))
                self.tableTop.setItem(row, 1, QTableWidgetItem(str(Cliente)))
                self.tableTop.setItem(row, 2, QTableWidgetItem(str(Transacciones)))

        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


def main():
    app = QApplication(sys.argv)
    ventana = ClasePEstadisticasCuentas()
    ventana.show()
    app.exec_()


if __name__ == '__main__':
    main()
