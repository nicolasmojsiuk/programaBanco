import sys
from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QMainWindow
from ventana1 import Ui_Form
from PyQt5.uic import loadUi

class ClaseImportarForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(ClaseImportarForm, self).__init__(parent)
        loadUi("vtnNuevoAlumno.ui", self)
        self.configurar()
        self.btnSalir.clicked.connect(self.close)


    def configurar(self):
        self.sbMatricula.setRange(1,9999999)
        self.sbParcial1.setRange(1, 10)
        self.sbParcial2.setRange(1, 10)
        self.sbAsistencia.setRange(0, 100)
        self.btnAceptar.clicked.connect(self.guardarDatos)

    def guardarDatos(self):
        nombre=self.leNombre.text()
        apellido=self.leApellido.text()
        matricula=self.sbMatricula.text()
        parcial1=self.sbParcial1.text()
        parcial2=self.sbParcial2.text()
        asistencia=sel|
        f.sbAsistencia.text()
        aprobado=0

        if nombre=="" or apellido=="" or matricula=="0" or parcial1=="0" or parcial2=="0":
            QMessageBox.warning(None, 'ERROR', 'No deje campos en blanco')
            return




        if int(parcial1)>=6 and int(parcial2)>=6 and int(asistencia)>=75:
            aprobado=1

        try:
            dbconfig = leer_configuracion_db()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            consulta = "INSERT INTO alumnos (nombre, apellido, matricula, parcial1, parcial2, asistencia, aprobado) values (%s, %s, %s, %s, %s, %s, %s)"
            datos = (nombre, apellido, int(matricula), int(parcial1), int(parcial2), int(asistencia), int(aprobado))
            cursor.execute(consulta, datos)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()



def main():
    app = QApplication(sys.argv)
    ventana = ClaseImportarForm()
    ventana.show()
    app.exec_()


if __name__ == '__main__':
    main()
