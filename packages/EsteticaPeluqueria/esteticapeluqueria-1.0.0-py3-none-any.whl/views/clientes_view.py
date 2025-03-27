from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QGroupBox, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from models.cliente import Cliente

class ClientesView(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.main_window = parent
        self.controller = controller
        self.editando = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Gestión de Clientes")
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                font-family: Arial, sans-serif;
                font-size: 14px;
                color: #333;
            }
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #4da3af;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                height: 30px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
            }
            QPushButton {
                background-color: #4da3af;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #3b8c92;
            }
            QPushButton:pressed {
                background-color: #2d6e73;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #4da3af;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)

        # Layout principal
        main_layout = QVBoxLayout()

        # Formulario
        form_box = QGroupBox("Datos del Cliente")
        form_layout = QFormLayout()

        # Definición clara y consistente de los campos
        self.inputs = {
            "dni": QLineEdit(),
            "nombre": QLineEdit(),
            "apellido": QLineEdit(),
            "telefono": QLineEdit(),  # Cambiado a "telefono" sin acento
            "email": QLineEdit()
        }

        # Configuración de campos con placeholders
        campos = [
            ("DNI", "dni", "Ej: 12345678A"),
            ("Nombre", "nombre", "Ej: Juan"),
            ("Apellido", "apellido", "Ej: Pérez"),
            ("Teléfono", "telefono", "Ej: 600123456"),  # Label con acento, clave sin acento
            ("Email", "email", "Ej: juan@email.com")
        ]

        for label_text, key, placeholder in campos:
            label = QLabel(f"{label_text}:")
            self.inputs[key].setPlaceholderText(placeholder)
            form_layout.addRow(label, self.inputs[key])

        form_box.setLayout(form_layout)
        main_layout.addWidget(form_box)

        # Botones
        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_volver = QPushButton("Volver")

        for btn in [self.btn_guardar, self.btn_editar, self.btn_eliminar, self.btn_volver]:
            btn.setFixedHeight(40)
            btn_layout.addWidget(btn)

        main_layout.addLayout(btn_layout)

        # Tabla
        self.tabla_clientes = QTableWidget()
        self.tabla_clientes.setColumnCount(5)
        self.tabla_clientes.setHorizontalHeaderLabels(["DNI", "Nombre", "Apellido", "Teléfono", "Email"])
        self.tabla_clientes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.tabla_clientes)

        self.setLayout(main_layout)

        # Conexiones
        self.btn_guardar.clicked.connect(self.guardar_cliente)
        self.btn_editar.clicked.connect(self.editar_cliente)
        self.btn_eliminar.clicked.connect(self.eliminar_cliente)
        self.btn_volver.clicked.connect(self.volver_al_menu)

        self.cargar_clientes()

    def guardar_cliente(self):
        try:
            datos = {
                "dni": self.inputs["dni"].text().strip(),
                "nombre": self.inputs["nombre"].text().strip(),
                "apellido": self.inputs["apellido"].text().strip(),
                "telefono": self.inputs["telefono"].text().strip(),  # Clave sin acento
                "email": self.inputs["email"].text().strip()
            }
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al obtener datos: {str(e)}")
            return

        # Validación de campos obligatorios
        if not all([datos["dni"], datos["nombre"], datos["apellido"]]):
            QMessageBox.warning(self, "Error", "DNI, Nombre y Apellido son obligatorios")
            return

        cliente = Cliente(**datos)
        
        if not self.editando:
            if self.controller.agregar_cliente(cliente):
                QMessageBox.information(self, "Éxito", "Cliente agregado correctamente")
            else:
                QMessageBox.warning(self, "Error", "El cliente ya existe")
        else:
            if self.controller.actualizar_cliente(cliente):
                QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente")
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar el cliente")
            self.editando = False
            self.btn_guardar.setText("Guardar")

        self.limpiar_campos()
        self.cargar_clientes()

    def editar_cliente(self):
        fila = self.tabla_clientes.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccione un cliente de la tabla")
            return

        dni = self.tabla_clientes.item(fila, 0).text()
        cliente = self.controller.buscar_cliente_por_dni(dni)
        
        if cliente:
            self.inputs["dni"].setText(cliente["dni"])
            self.inputs["nombre"].setText(cliente["nombre"])
            self.inputs["apellido"].setText(cliente["apellido"])
            self.inputs["telefono"].setText(cliente["telefono"])  # Clave sin acento
            self.inputs["email"].setText(cliente["email"])

            self.editando = True
            self.btn_guardar.setText("Actualizar")

    def eliminar_cliente(self):
        fila = self.tabla_clientes.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccione un cliente de la tabla")
            return

        dni = self.tabla_clientes.item(fila, 0).text()
        
        respuesta = QMessageBox.question(
            self, 
            "Confirmar",
            f"¿Eliminar al cliente con DNI {dni}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            if self.controller.eliminar_cliente(dni):
                QMessageBox.information(self, "Éxito", "Cliente eliminado")
                self.cargar_clientes()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el cliente")

    def cargar_clientes(self):
        clientes = self.controller.obtener_clientes()
        self.tabla_clientes.setRowCount(len(clientes))
        
        for row, cliente in enumerate(clientes):
            self.tabla_clientes.setItem(row, 0, QTableWidgetItem(cliente["dni"]))
            self.tabla_clientes.setItem(row, 1, QTableWidgetItem(cliente["nombre"]))
            self.tabla_clientes.setItem(row, 2, QTableWidgetItem(cliente["apellido"]))
            self.tabla_clientes.setItem(row, 3, QTableWidgetItem(cliente["telefono"]))  # Clave sin acento
            self.tabla_clientes.setItem(row, 4, QTableWidgetItem(cliente["email"]))

    def limpiar_campos(self):
        for campo in self.inputs.values():
            campo.clear()
        self.editando = False
        self.btn_guardar.setText("Guardar")
        self.tabla_clientes.clearSelection()

    def volver_al_menu(self):
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.container)