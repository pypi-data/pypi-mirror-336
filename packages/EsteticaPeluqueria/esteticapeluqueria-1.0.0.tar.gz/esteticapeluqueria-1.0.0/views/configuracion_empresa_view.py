from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
import json
import os

class ConfiguracionEmpresaView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Campos para los datos de la empresa
        self.label_nombre = QLabel("Nombre de la Empresa:")
        self.input_nombre = QLineEdit()
        
        self.label_cif = QLabel("CIF:")
        self.input_cif = QLineEdit()
        
        self.label_email = QLabel("Email de la Empresa:")
        self.input_email = QLineEdit()
        
        self.label_password = QLabel("Contraseña del Correo:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Layout de grid para la dirección
        direccion_layout = QGridLayout()
        
        self.label_calle = QLabel("Calle y Número:")
        self.input_calle = QLineEdit()
        
        self.label_poblacion = QLabel("Población:")
        self.input_poblacion = QLineEdit()
        
        self.label_codigo_postal = QLabel("Código Postal:")
        self.input_codigo_postal = QLineEdit()
        
        direccion_layout.addWidget(self.label_calle, 0, 0)
        direccion_layout.addWidget(self.input_calle, 0, 1)
        direccion_layout.addWidget(self.label_poblacion, 1, 0)
        direccion_layout.addWidget(self.input_poblacion, 1, 1)
        direccion_layout.addWidget(self.label_codigo_postal, 2, 0)
        direccion_layout.addWidget(self.input_codigo_postal, 2, 1)
        
        # Botones
        self.btn_guardar = QPushButton("Guardar Datos")
        self.btn_guardar.clicked.connect(self.guardar_datos)
        
        self.btn_volver = QPushButton("Volver al Menú Principal")
        self.btn_volver.clicked.connect(self.volver_al_menu)
        
        # Cargar los datos existentes
        self.cargar_datos()
        
        # Agregar widgets al layout
        layout.addWidget(self.label_nombre)
        layout.addWidget(self.input_nombre)
        layout.addWidget(self.label_cif)
        layout.addWidget(self.input_cif)
        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        
        # Añadir el layout de dirección
        layout.addLayout(direccion_layout)
        
        layout.addWidget(self.btn_guardar)
        layout.addWidget(self.btn_volver)
        
        self.setLayout(layout)
    
    def cargar_datos(self):
        if os.path.exists("data/config_empresa.json"):
            with open("data/config_empresa.json", "r", encoding='utf-8') as file:
                datos = json.load(file)
                self.input_nombre.setText(datos.get("nombre", ""))
                self.input_cif.setText(datos.get("cif", ""))
                self.input_email.setText(datos.get("email", ""))
                self.input_password.setText(datos.get("password", ""))
                
                # Cargar dirección dividida o la antigua dirección completa
                if "direccion" in datos:
                    # Si ya está dividida
                    if isinstance(datos["direccion"], dict):
                        self.input_calle.setText(datos["direccion"].get("calle", ""))
                        self.input_poblacion.setText(datos["direccion"].get("poblacion", ""))
                        self.input_codigo_postal.setText(datos["direccion"].get("codigo_postal", ""))
                    else:
                        # Migrar de dirección antigua a nueva estructura
                        direccion_completa = datos["direccion"]
                        # Aquí puedes implementar lógica para dividir la dirección si es necesario
                        self.input_calle.setText(direccion_completa)
    
    def guardar_datos(self):
        datos = {
            "nombre": self.input_nombre.text(),
            "cif": self.input_cif.text(),
            "email": self.input_email.text(),
            "password": self.input_password.text(),
            "direccion": {
                "calle": self.input_calle.text(),
                "poblacion": self.input_poblacion.text(),
                "codigo_postal": self.input_codigo_postal.text()
            }
        }
        
        os.makedirs("data", exist_ok=True)
        
        with open("data/config_empresa.json", "w", encoding='utf-8') as file:
            json.dump(datos, file, indent=4, ensure_ascii=False)
        
        QMessageBox.information(self, "Éxito", "Datos de la empresa guardados correctamente")
    
    def volver_al_menu(self):
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.container)