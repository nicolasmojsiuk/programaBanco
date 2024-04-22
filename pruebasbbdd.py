from mysql.connector import MySQLConnection, Error
from python_mysql_config import leer_configuracion_db

try:
    # Abre el archivo de texto en modo lectura
    with open('userlog.txt', 'r') as archivo:
        primera_linea = archivo.readline()
        palabras = primera_linea.split()
        idusuariolog = palabras[0]
except Error as e:
    print(e)

try:
    idparatxt=int(idusuariolog)
    detalle="funca"
    masdetalle="funcamas"
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