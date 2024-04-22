import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db

class ClasePEstadisticasClientes(QMainWindow):
    def __init__(self, parent=None):
        super(ClasePEstadisticasClientes, self).__init__(parent)
        loadUi("PEstadisticasClientes.ui", self)
        self.configurar()

    def configurar(self):
        self.btnSalir.clicked.connect(self.close)
        # Obtener estadísticas
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()

            # Número de clientes
            cursor.execute("SELECT COUNT(*) FROM clientes")
            nClientes = cursor.fetchone()[0]
            self.lblClientes.setText("Número de clientes: " + str(nClientes))

            # Número de cuentas inactivas
            cursor.execute("SELECT COUNT(*) FROM clientes WHERE estado=0")
            nInactivos = cursor.fetchone()[0]
            self.lblInactivos.setText("Número de clientes inactivos: " + str(nInactivos))

            # Número de clientes con cuentas activas
            nActivos = nClientes - nInactivos
            self.lblActivos.setText("Número de clientes activos: " + str(nActivos))



            # Top 5 transacciones en el mes (solo nombre)
            consulta = """
            SELECT c.nombre, COUNT(*) AS num_transacciones
            FROM transacciones t
            JOIN cuentas cu ON t.idcuentaorigen = cu.cbu
            JOIN clientes c ON cu.idcliente = c.idclientes
            GROUP BY c.nombre
            ORDER BY num_transacciones DESC
            LIMIT 5
            """
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            for row, (Cliente, Transacciones) in enumerate(resultados):
                self.tableTop.setItem(row, 0, QTableWidgetItem(Cliente))
                self.tableTop.setItem(row, 1, QTableWidgetItem(str(Transacciones)))


        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

def main():
    app = QApplication(sys.argv)
    ventana = ClasePEstadisticasClientes()
    ventana.show()
    app.exec_()

if __name__ == '__main__':
    main()
