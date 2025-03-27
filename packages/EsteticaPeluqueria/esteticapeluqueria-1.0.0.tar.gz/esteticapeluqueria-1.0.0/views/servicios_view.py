from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QHeaderView, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from models.servicio import Servicio

class ServiciosView(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.main_window = parent
        self.controller = controller
        self.editando = False
        self.nombre_original = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Gestión de Servicios")
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                font-family: Arial, sans-serif;
                font-size: 14px;
                color: #333;
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

        main_layout = QVBoxLayout()

        # Título
        titulo = QLabel("Gestión de Servicios")
        titulo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("color: #4da3af;")
        main_layout.addWidget(titulo)

        # Formulario
        form_box = QGroupBox("Datos del Servicio")
        form_layout = QGridLayout()

        self.inputs = {
            "nombre": QLineEdit(),
            "precio": QLineEdit(),
            "duracion": QLineEdit()
        }

        # Configuración de campos
        campos = [
            ("Nombre del Servicio", "nombre", "Ej: Corte de pelo"),
            ("Precio (€)", "precio", "Ej: 25.50"),
            ("Duración (minutos)", "duracion", "Ej: 30")
        ]

        for i, (label_text, key, placeholder) in enumerate(campos):
            label = QLabel(f"{label_text}:")
            self.inputs[key].setPlaceholderText(placeholder)
            form_layout.addWidget(label, i, 0)
            form_layout.addWidget(self.inputs[key], i, 1)

        form_box.setLayout(form_layout)
        main_layout.addWidget(form_box)

        # Botones
        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar Servicio")
        self.btn_editar = QPushButton("Editar Servicio")
        self.btn_eliminar = QPushButton("Eliminar Servicio")
        self.btn_volver = QPushButton("Volver al Menú")

        for btn in [self.btn_guardar, self.btn_editar, self.btn_eliminar, self.btn_volver]:
            btn.setFixedHeight(40)
            btn.setStyleSheet("background-color: #4da3af; color: white; font-weight: bold;")
            btn_layout.addWidget(btn)

        main_layout.addLayout(btn_layout)

        # Tabla
        self.tabla_servicios = QTableWidget()
        self.tabla_servicios.setColumnCount(3)
        self.tabla_servicios.setHorizontalHeaderLabels(["Nombre", "Precio (€)", "Duración (min)"])
        self.tabla_servicios.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.tabla_servicios)

        self.setLayout(main_layout)

        # Conexiones
        self.btn_guardar.clicked.connect(self.guardar_servicio)
        self.btn_editar.clicked.connect(self.editar_servicio)
        self.btn_eliminar.clicked.connect(self.eliminar_servicio)
        self.btn_volver.clicked.connect(self.volver_al_menu)

        self.cargar_servicios()

    def guardar_servicio(self):
        try:
            nombre = self.inputs["nombre"].text().strip()
            precio = float(self.inputs["precio"].text().strip())
            duracion = int(self.inputs["duracion"].text().strip())
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese valores válidos")
            return

        servicio = Servicio(nombre, precio, duracion)
        
        if not self.editando:
            self.controller.agregar_servicio(servicio.to_dict())
            QMessageBox.information(self, "Éxito", "Servicio agregado correctamente")
        else:
            self.controller.actualizar_servicio(servicio.to_dict(), self.nombre_original)
            QMessageBox.information(self, "Éxito", "Servicio actualizado correctamente")
            self.editando = False
            self.btn_guardar.setText("Guardar Servicio")

        self.limpiar_campos()
        self.cargar_servicios()

    def editar_servicio(self):
        fila_seleccionada = self.tabla_servicios.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Error", "Seleccione un servicio para editar")
            return

        nombre = self.tabla_servicios.item(fila_seleccionada, 0).text()
        servicio = self.controller.buscar_servicio_por_nombre(nombre)
        
        if servicio:
            self.inputs["nombre"].setText(servicio["nombre"])
            self.inputs["precio"].setText(str(servicio["precio"]))
            self.inputs["duracion"].setText(str(servicio["duracion"]))
            
            self.editando = True
            self.nombre_original = servicio["nombre"]
            self.btn_guardar.setText("Actualizar Servicio")

    def eliminar_servicio(self):
        fila_seleccionada = self.tabla_servicios.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Error", "Seleccione un servicio para eliminar")
            return

        nombre = self.tabla_servicios.item(fila_seleccionada, 0).text()
        
        respuesta = QMessageBox.question(
            self, 
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar el servicio '{nombre}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            if self.controller.eliminar_servicio(nombre):
                QMessageBox.information(self, "Éxito", "Servicio eliminado correctamente")
                self.cargar_servicios()

    def cargar_servicios(self):
        servicios = self.controller.obtener_servicios()
        self.tabla_servicios.setRowCount(len(servicios))
        
        for row, servicio in enumerate(servicios):
            self.tabla_servicios.setItem(row, 0, QTableWidgetItem(servicio["nombre"]))
            self.tabla_servicios.setItem(row, 1, QTableWidgetItem(f"€{servicio['precio']:.2f}"))
            self.tabla_servicios.setItem(row, 2, QTableWidgetItem(f"{servicio['duracion']} min"))

    def limpiar_campos(self):
        for input_field in self.inputs.values():
            input_field.clear()
        self.editando = False
        self.nombre_original = ""
        self.btn_guardar.setText("Guardar Servicio")

    def volver_al_menu(self):
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.container)
        
        
        