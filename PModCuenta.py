import sys
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox
from PyQt5.uic import loadUi
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db

class ClasePModCuenta(QMainWindow):
    def __init__(self, parent=None):
        super(ClasePModCuenta, self).__init__(parent)
        loadUi("PModCuenta.ui", self)
        self.configurar()
        self.id = None

    def configurar(self):
        self.leAlias.setDisabled(True)
        self.leBalance.setDisabled(True)
        self.btnModificar.clicked.connect(self.modificar_un_registro)
        self.btnGuardar.clicked.connect(self.guardarRegistroModificado)
        self.btnGuardar.setDisabled(True)
        self.btnSalir.clicked.connect(self.close)

    def modificar_un_registro(self):
        self.leAlias.setDisabled(False)
        self.leBalance.setDisabled(False)
        cbuMod=self.leCbu.text()
        if cbuMod=="":
            QMessageBox.about(self,"Info","Ingrese un cbu o alias")
            return
        aliasMod="n"
        if cbuMod.isdigit():
            cbuMod=int(cbuMod)
        else:
            aliasMod=cbuMod

        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT * FROM cuentas WHERE cbu=%s or alias=%s"
            datos=(cbuMod,aliasMod)
            cursor.execute(consulta,datos)
        # Obtener los datos de la consulta
            resultado = cursor.fetchone()
            if resultado ==[] or resultado==None:
                QMessageBox.about(self, "Error", "No existe ese cbu o alias")
                self.leAlias.setDisabled(True)
                self.leBalance.setDisabled(True)
                self.lblDatos.setText("")
                return
            else:
                try:
                    self.btnGuardar.setDisabled(False)
                    self.cbu=resultado[0]
                    idcliente=int(resultado[2])
                    dbconfig = leer_configuracion_db()
                    conn = MySQLConnection(**dbconfig)
                    cursor = conn.cursor()
                    consulta = "SELECT nombre FROM clientes WHERE idclientes=%s"
                    datos = (idcliente,)
                    cursor.execute(consulta, datos)
                    # Obtener los datos de la consulta
                    resCliente = cursor.fetchone()
                    self.dueño=resCliente[0]
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
        #rellenar los campos con los resultado actuales
        if resultado[3] == 1:
            tipoC= "Cuenta corriente en pesos"
        elif resultado[3] == 2:
            tipoC= "Caja de ahorro en pesos"
        elif resultado[3] == 3:
            tipoC= "Caja de ahorro en reales"
        elif resultado[3] == 4:
            tipoC = "Caja de ahorro en dólares"
        elif resultado[3] == 5:
            tipoC = "caja de ahorro en euros"
        else:
            tipoC= "Tipo de cuenta desconocido"

        self.lblDatos.setText(tipoC+" de "+self.dueño)
        self.leAlias.setText(str(resultado[1]))
        self.leBalance.setText(str(resultado[5]))


    def guardarRegistroModificado(self):
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            alias = self.leAlias.text()
            balance = float(self.leBalance.text())
            consulta_verificar_alias = "SELECT cbu FROM cuentas WHERE alias = %s"
            cursor.execute(consulta_verificar_alias, (alias,))
            resultado_verificacion = cursor.fetchone()

            if resultado_verificacion and resultado_verificacion[0] != self.cbu:
                # Alias ya existe para otra cuenta
                QMessageBox.warning(self, "Error", "El alias ya existe para otra cuenta. Por favor, elija otro.")
                return

            # Continuar con la actualización si el alias es único
            consulta = "UPDATE cuentas SET alias=%s, balance=%s WHERE cbu = %s"
            datos = (alias, balance, self.cbu)
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
            idparatxt = int(idusuariolog)
            detalle = "Modificó los datos de una cuenta"
            masdetalle = f"cbu: {self.cbu} de {self.dueño}"
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
    ventana = ClasePModCuenta()
    ventana.show()
    app.exec_()

if __name__ == '__main__':
    main()
