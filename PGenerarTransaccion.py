import sys

import pygame
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi
from ventana1 import Ui_Form
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db

class ClasePGenerarTransaccion(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(ClasePGenerarTransaccion, self).__init__(parent)
        loadUi("PGenerarTransaccion.ui", self)
        self.configurar()

    def configurar(self):
        self.btnConfirmar.clicked.connect(self.generarTransaccion)
        self.btnSalir.clicked.connect(self.close)

    def obtenerTransaccionesMensuales(self, cbuOrigen, cbuDestino):
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()

            # Consulta para transacciones de origen
            consulta = "SELECT monto FROM transacciones WHERE (idcuentaorigen = %s) AND MONTH(fechayhoraInicio) = MONTH(NOW())"
            cursor.execute(consulta, (cbuOrigen,))
            datos = cursor.fetchall()
            self.transaccionesMesOrigen = sum(monto[0] for monto in datos)

            # Consulta para transacciones de destino
            consulta = "SELECT monto FROM transacciones WHERE (idcuentadestino = %s) AND MONTH(fechayhoraInicio) = MONTH(NOW())"
            cursor.execute(consulta, (cbuDestino,))
            datos = cursor.fetchall()
            self.transaccionesMesDestino = sum(monto[0] for monto in datos)
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def generarTransaccion(self):
        # verifica sii el monto no es cero
        monto = self.SBMonto.value()
        if monto == 0:
            QMessageBox.warning(None, 'ERROR', 'No se puede realizar una transaccion de monto 0 (cero)')
            return
    #obtner los datos de las cajas de texto

        cbuOrigen = self.leCuentaOr.text()
        cbuDestino = self.leCuentaDes.text()

#---------------si ingresa un alias lo convierto a cbu correspondiente-----------------------------------------------
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT cbu,idcliente FROM cuentas where cbu=%s or alias=%s"
            datos=(cbuOrigen,cbuOrigen)
            cursor.execute(consulta,datos)
            # Obtener los datos de la consulta
            cbuOrigen = cursor.fetchone()
            if cbuOrigen==None:
                QMessageBox.warning(None, 'ERROR', 'La cuenta de origen no existe')
                return
            else:
                idCliente=cbuOrigen[1]
                cbuOrigen=cbuOrigen[0]
                # Obtener el estado del cliente
                estadoCliente = self.obtenerEstadoCliente(idCliente)
                # Verificar el estado del cliente antes de permitir la transacción
                if estadoCliente == 0:
                    QMessageBox.warning(None, 'ERROR',
                                        'El cliente no está activo. No puede realizar transacciones.')
                    return
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT cbu FROM cuentas where cbu=%s or alias=%s"
            datos=(cbuDestino,cbuDestino)
            cursor.execute(consulta,datos)
            # Obtener los datos de la consulta
            cbuDestino = cursor.fetchone()
            print(cbuDestino)
            if cbuDestino==None:
                QMessageBox.warning(None, 'ERROR', 'La cuenta de destino no existe')
                return
            else:
                cbuDestino=cbuDestino[0]
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
#----------------------------------------------------------------------------------------------------------------------
    #verificar si son iguales los cbu o alias
        if cbuDestino == cbuOrigen:
            QMessageBox.warning(None, 'ERROR', 'Las cuentas de origen y destino son la misma')
            return

        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT * FROM cuentas"
            cursor.execute(consulta)
            # Obtener los datos de la consulta
            cuentas = cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

        # verficar si las cuentas existen
        if all((cbuOrigen in tupla, cbuDestino in tupla) for tupla in cuentas):
            #------------------------------------------------------------------------------------------
            #OBTENER TRANSACCIONES MENSUALES DE LOS INVOLUCRADOS origen
            self.transaccionesMesorigen=0
            self.transaccionesMesdestino=0
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                # Consulta para transacciones de origen
                consulta = "SELECT monto FROM transacciones WHERE (idcuentaorigen = %s) AND MONTH(fechayhoraInicio) = MONTH(NOW())"
                datos=(cbuOrigen,)
                cursor.execute(consulta, datos)
                transacciones = cursor.fetchall()
                for tupla in transacciones:
                    self.transaccionesMesorigen += tupla[0]
                print("-------------------------")
                print(self.transaccionesMesorigen)
            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
# ------------------------------------------------------------------------------------------
    # OBTENER TRANSACCIONES MENSUALES DE LOS INVOLUCRADOS cuenta destino
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                # Consulta para transacciones de destino
                consulta = "SELECT monto FROM transacciones WHERE (idcuentadestino = %s) AND MONTH(fechayhoraInicio) = MONTH(NOW())"
                datos = (cbuDestino,)
                cursor.execute(consulta, datos)
                transaccionesd = cursor.fetchall()
                for tupla in transaccionesd:
                    self.transaccionesMesdestino += tupla[0]
                print("---------------------------")
                print(self.transaccionesMesdestino)
            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
    # ------------------------------------------------------------------------------------------
            # obtener los limites mensuales para cada tipo de cuenta
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "SELECT * FROM tipodecuenta"
                cursor.execute(consulta,)
                # Obtener los datos de la consulta
                resTipodecuenta = cursor.fetchall()
                print(resTipodecuenta)
                lmCCP = resTipodecuenta[0][3]
                lmCAP = resTipodecuenta[1][3]
                lmCAR = resTipodecuenta[2][3]
                lmCAD = resTipodecuenta[3][3]
                lmCAE = resTipodecuenta[4][3]

            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()

            # -----------------------------------------------------------------------------------------
            # obtengo tipo de cuenta del origen
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "SELECT tipo FROM cuentas WHERE cbu=%s OR alias=%s"
                datos = (cbuOrigen, cbuOrigen)
                cursor.execute(consulta, datos)
                # Obtener los datos de la consulta
                tipoOrigen = cursor.fetchone()
                tipoOrigen=tipoOrigen[0]
                print("tipo de origen ", tipoOrigen)
            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()

            # obtengo el tipo de cuenta del destino
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "SELECT tipo FROM cuentas WHERE cbu=%s OR alias=%s"
                datos = (cbuDestino, cbuDestino)
                cursor.execute(consulta, datos)
                # Obtener los datos de la consulta
                tipoDestino = cursor.fetchone()
                tipoDestino=tipoDestino[0]
            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
            # --------------------------------------------------------------------------------------------
            # verificar el monto limite
            transaccionOKD = False
            if tipoDestino == 1:
                if lmCCP >= monto + self.transaccionesMesdestino:
                    transaccionOKD = True
                else:
                    QMessageBox.warning(None, 'ERROR',
                                        'La cuenta de destino no puede realizar esta transaccion debido a que supera su limite mensual')
            elif tipoDestino == 2:
                if lmCAP >= monto + self.transaccionesMesdestino:
                    transaccionOKD = True
                else:
                    QMessageBox.warning(None, 'ERROR',
                                        'La cuenta de destino no puede realizar esta transaccion debido a que supera su limite mensual')
            elif tipoDestino == 3:
                if lmCAR >= monto + self.transaccionesMesdestino:
                    transaccionOKD = True
                else:
                    QMessageBox.warning(None, 'ERROR',
                                        'La cuenta de destino no puede realizar esta transaccion debido a que supera su limite mensual')
            elif tipoDestino == 4:
                if lmCAD >= monto + self.transaccionesMesdestino:
                    transaccionOKD = True
                else:
                    QMessageBox.warning(None, 'ERROR',
                                        'La cuenta de destino no puede realizar esta transaccion debido a que supera su limite mensual')
            elif tipoDestino == 5:
                if lmCAE >= monto + self.transaccionesMesdestino:
                    transaccionOKD = True
                else:
                    QMessageBox.warning(None, 'ERROR',
                                        'La cuenta de destino no puede realizar esta transaccion debido a que supera su limite mensual')

            # verifico lo mismo pero de la cuenta origen
            transaccionOKO = False

            if tipoOrigen == 1:
                if lmCCP >= monto + self.transaccionesMesorigen:
                     transaccionOKO = True
                     moneda="pesos"
                else:
                    QMessageBox.warning(None, 'ERROR',
                                        'La cuenta de origen no puede realizar esta transaccion debido a que supera su limite mensual')
            elif tipoOrigen == 2:
                if lmCAP >= monto + self.transaccionesMesorigen:
                    transaccionOKO = True
                    moneda="pesos"
                else:
                    QMessageBox.warning(None, 'ERROR',
                                        'La cuenta de origen no puede realizar esta transaccion debido a que supera su limite mensual')
            elif tipoOrigen == 3:
                if lmCAR >= monto + self.transaccionesMesorigen:
                    transaccionOKO = True
                    moneda="reales"
                else:
                    QMessageBox.warning(None, 'ERROR',
                                        'La cuenta de origen no puede realizar esta transaccion debido a que supera su limite mensual')
            elif tipoOrigen == 4:
                if lmCAD >= monto + self.transaccionesMesorigen:
                    transaccionOKO = True
                    moneda="dolares"
                else:
                    QMessageBox.warning(None, 'ERROR',
                                        'La cuenta de origen no puede realizar esta transaccion debido a que supera su limite mensual')
            elif tipoOrigen == 5:
                if lmCAE >= monto + self.transaccionesMesorigen:
                    transaccionOKO = True
                    moneda="euros"
                else:
                    QMessageBox.warning(None, 'ERROR',
                                        'La cuenta de origen no puede realizar esta transaccion debido a que supera su limite mensual')

            if transaccionOKO == False:
                return
            if transaccionOKD == False:
                return
        else:
            QMessageBox.warning(None, 'ERROR', 'Las cuentas de origen o destino no existen')
            return

        # obtengo balance del origen
        saldo = False
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT balance FROM cuentas WHERE cbu=%s OR alias=%s"
            datos = (cbuOrigen, cbuOrigen)
            cursor.execute(consulta, datos)
            # Obtener los datos de la consulta
            balance = cursor.fetchone()
            saldoOrigen = balance[0]
            if saldoOrigen >= monto:
                saldo = True
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    #obtener balance actual del destino
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT balance FROM cuentas WHERE cbu=%s OR alias=%s"
            datos = (cbuDestino, cbuDestino)
            cursor.execute(consulta, datos)
            # Obtener los datos de la consulta
            balance = cursor.fetchone()
            saldoDestino = balance[0]
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
        # verificar si los tipos de cuenta son compatibles
        tipo = False
        if tipoDestino == tipoOrigen:
            tipo = True
        elif (tipoDestino == 1 and tipoOrigen == 2) or (tipoDestino == 2 and tipoOrigen == 1):
            tipo = True
        else:
            QMessageBox.warning(None, 'ERROR',
                                'Las cuentas de origen y destino no son trabajan en el mismo tipo de moneda')
            return
        # si esta ok cada item realizo la transaccion

        # ----------------------------------------------------------------------------------------
        if transaccionOKO == True and transaccionOKD == True and saldo == True and tipo == True:
            try:
                idcuentaorigen=cbuOrigen
                idcuentadestino=cbuDestino
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "INSERT INTO transacciones (fechaYhoraInicio, monto, idcuentaorigen, idcuentadestino, moneda) VALUES (NOW(), %s, %s, %s, %s)"
                datos = (monto, idcuentaorigen, idcuentadestino, moneda)
                cursor.execute(consulta, datos)
                conn.commit()
            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()

#--------------------------------obtener la transacion id---------------------------------------
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()

                # Consulta para obtener el ID del último registro
                consulta = "SELECT MAX(idtransacciones) FROM transacciones"

                cursor.execute(consulta)
                transaccionactual = cursor.fetchone()[0]  # Obtenemos el valor del ID

                conn.commit()
            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()


            #---------------------RESTA EL MONTO DEL BALANCE DEL ORIGEN-------------------------
            try:
                nuevobalance=saldoOrigen-monto
                print(nuevobalance)
                print(cbuOrigen)
                db_config = leer_configuracion_db()
                conn = MySQLConnection(**db_config)
                cursor = conn.cursor()
                consulta = "UPDATE cuentas SET balance = %s WHERE cbu=%s OR alias=%s"
                datos = (nuevobalance, cbuOrigen, cbuOrigen)
                cursor.execute(consulta, datos)
                conn.commit()
                # ----------------sonido de confirmacion-------------------------
                pygame.init()
                # Ruta del archivo MP3 que deseas reproducir
                mp3_file = 'dindon.mp3'
                # Crear un objeto mixer
                pygame.mixer.init()
                # Cargar y reproducir el archivo MP3
                pygame.mixer.music.load(mp3_file)
                pygame.mixer.music.play()
                # Deja que la música se reproduzca durante un tiempo (por ejemplo, 10 segundos)
                pygame.time.wait(2000)
                # Detén la música
                pygame.mixer.music.stop()
                # Cierra pygame
                pygame.quit()
                QMessageBox.information(None, "Éxito", "Se envio la transferencia")
            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
#------------------------------sumar el balance al destino----------------------
            try:
                nuevobalancedes = saldoDestino + monto
                db_config = leer_configuracion_db()
                conn = MySQLConnection(**db_config)
                cursor = conn.cursor()
                consulta = "UPDATE cuentas SET balance = %s WHERE cbu=%s OR alias=%s"
                datos = (nuevobalancedes, cbuDestino, cbuDestino)
                cursor.execute(consulta, datos)
                conn.commit()

            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
    #------------guarda en el historial de usuarios----------------
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
                detalle = "realizo una transaccion"
                masdetalle = f"cbu origen: {cbuOrigen} cbu destino: {cbuDestino} monto: ${monto}"
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
    #------------guarda la fecha y hora del impacto----------------
            try:
                dbconfig = leer_configuracion_db()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                consulta = "UPDATE transacciones SET fechaYhoraImpacto = NOW() WHERE idtransacciones =%s"
                datos=(transaccionactual,)
                cursor.execute(consulta,datos)
                conn.commit()
            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()


        else:
            QMessageBox.warning(None, 'ERROR', 'La cuenta de origen no tiene saldo suficiente')

        print(self.transaccionesMesorigen)
        print(self.transaccionesMesdestino)

    def obtenerEstadoCliente(self, idCliente):
        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "SELECT estado FROM clientes WHERE idclientes = %s"
            cursor.execute(consulta, (idCliente,))
            estadoCliente = cursor.fetchone()[0]
            return estadoCliente
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

def main():
    app = QApplication(sys.argv)
    ventana = ClasePGenerarTransaccion()
    ventana.show()
    app.exec_()

if __name__ == '__main__':
    main()
