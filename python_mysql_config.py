from configparser import ConfigParser

def leer_configuracion_db(archivo='config.ini', seccion='mysql'):
    # Creamos un ConfigParser y leemos el contenido del archivo config.ini
    parser = ConfigParser()
    parser.read(archivo)

    db = {}
    # Si el archivo tiene la seccion pasada por argumento...
    if parser.has_section(seccion):
        # ...entonces tomamos los items de esa seccion
        items = parser.items(seccion)
        # Recorremos cada par de valores y los guardamos en el diccionario de db
        for item in items:
            db[item[0]] = item[1]
    # Si el archivo no tiene esa seccion
    else:
        # Lanzar una excepcion
        raise Exception('{0} no se encuentra en el archivo {1}'.format(seccion, archivo))
    
    return db