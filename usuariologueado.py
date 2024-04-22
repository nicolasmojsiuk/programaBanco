from Login import ClaseImportarForm

class UserLog():
    def __init__(self, parent=None):
        super(UserLog, self).__init__(parent)
        self.usuario_logueado=""
        self.usuario_logeado=ClaseImportarForm.nombreusuario
        print(self.usuario_logeado)
