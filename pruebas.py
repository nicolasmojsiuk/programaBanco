import sys

import PyQt5
from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QMenu, QAction, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Crear la tabla y configurar algunas comidas de ejemplo
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Comidas"])
        self.tableWidget.setContextMenuPolicy(PyQt5.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.mostrar_menu_contextual)

        self.agregar_comida("Pizza")
        self.agregar_comida("Hamburguesa")
        self.agregar_comida("Ensalada")

        # Configurar la ventana principal
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.tableWidget)
        self.setCentralWidget(central_widget)

    def agregar_comida(self, nombre_comida):
        # Agregar una fila con la comida especificada
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row_position, 0, QTableWidgetItem(nombre_comida))

    def mostrar_menu_contextual(self, position):
        # Obtener el ítem seleccionado
        item = self.tableWidget.itemAt(position)

        if item:
            # Crear un menú contextual
            menu = QMenu(self)

            # Agregar la opción "Eliminar" al menú
            eliminar_action = QAction("Eliminar", self)
            eliminar_action.triggered.connect(self.eliminar_comida)
            menu.addAction(eliminar_action)

            # Mostrar el menú en la posición del clic derecho
            menu.exec_(self.tableWidget.viewport().mapToGlobal(position))

    def eliminar_comida(self):
        # Obtener el índice de la fila seleccionada
        selected_row = self.tableWidget.currentRow()

        if selected_row != -1:
            # Eliminar la fila seleccionada
            self.tableWidget.removeRow(selected_row)


def main():
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
