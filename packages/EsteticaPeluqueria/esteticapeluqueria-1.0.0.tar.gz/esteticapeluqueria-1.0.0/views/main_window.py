from PyQt6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QWidget, 
                            QStackedWidget, QHBoxLayout, QLineEdit, QLabel, 
                            QTabWidget, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QPixmap
from views.ficha_cliente.buscar_ficha_cliente_view import BuscarFichaClienteView
from views.clientes_view import ClientesView
from views.estadisticas_diarias_view import EstadisticasDiariasView
from views.servicios_view import ServiciosView
from views.facturacion.facturacion_view import FacturacionView
from views.configuracion_empresa_view import ConfiguracionEmpresaView
from views.estadisticas_view import EstadisticasMensualesView
from controllers.tratamientos_controller import TratamientosController
from views.trimestral_view import EstadisticasTrimestralesView
from controllers.clientes_controller import ClientesController
from controllers.servicios_controller import ServiciosController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Punto de Venta D&G Style")
        self.setGeometry(100, 100, 1920, 1800)  # Tamaño por defecto
        self.showMaximized() 
        
        # Inicializar controladores
        self.tratamientos_controller = TratamientosController()
        self.clientes_controller = ClientesController()
        self.servicios_controller = ServiciosController()
        
        self.init_ui()
        self.setup_connections()
        self.apply_styles()
    
    def init_ui(self):
        """Inicializa los componentes de la interfaz"""
        # Configuración principal
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Layout principal
        main_layout = QHBoxLayout()
        
        # Sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Contenido principal
        self.content = self.create_main_content()
        main_layout.addWidget(self.content)
        
        # Widget contenedor
        self.container = QWidget()
        self.container.setLayout(main_layout)
        self.stacked_widget.addWidget(self.container)
    
    def create_sidebar(self):
        """Crea el sidebar con los botones de navegación"""
        sidebar = QWidget()
        sidebar.setFixedWidth(220)  # Un poco más ancho
        sidebar.setObjectName("sidebar")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 20)  # Márgenes internos
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Logo pequeño en el sidebar
        logo_label = QLabel()
        logo_pixmap = QPixmap("utils/D&G.png")
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(
                150, 75, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            ))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #4da3af;")
        layout.addWidget(separator)
        
        # Botones del sidebar
        buttons = [
            ("Clientes", "user.png", self.gestion_clientes),
            ("Servicios", "services.png", self.gestion_servicios),
            ("Facturación", "invoice.png", self.gestion_facturacion),
            ("Ficha Cliente", "search.png", self.buscar_ficha_cliente),
            ("Estadísticas", "stats.png", self.gestion_estadisticas),
            ("Mi Empresa", "settings.png", self.gestion_config_empresa)
        ]
        
        for text, icon, callback in buttons:
            btn = self.create_button(text, icon)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        # Espaciador para empujar todo hacia arriba
        layout.addStretch()
        
        # Versión de la app
        version_label = QLabel("v1.0.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(version_label)
        
        sidebar.setLayout(layout)
        return sidebar
    
    def create_main_content(self):
        """Crea el área de contenido principal"""
        content = QWidget()
        content.setObjectName("mainContent")
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Tarjeta de bienvenida
        welcome_card = QWidget()
        welcome_card.setObjectName("welcomeCard")
        card_layout = QVBoxLayout()
        
        title = QLabel("Bienvenido al Sistema de Gestión")
        title.setObjectName("welcomeTitle")
        
        subtitle = QLabel("Seleccione una opción del menú lateral para comenzar")
        subtitle.setObjectName("welcomeSubtitle")
        
        # Logo central más elegante
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap("utils/D&G.png")
        if not self.logo_pixmap.isNull():
            self.logo_label.setPixmap(self.logo_pixmap.scaled(
                400, 200, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            ))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(20)
        card_layout.addWidget(self.logo_label)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_card.setLayout(card_layout)
        
        layout.addWidget(welcome_card)
        content.setLayout(layout)
        return content
    
    def setup_connections(self):
        """Configura las conexiones de señales y slots"""
        pass  # Ya se configuraron en create_sidebar
    
    def apply_styles(self):
        """Aplica los estilos CSS a la aplicación"""
        self.setStyleSheet("""
            /* Estilos generales */
            QMainWindow {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            /* Sidebar */
            #sidebar {
                background-color: #ffffff;
                border-right: 1px solid #e0e0e0;
            }
            
            /* Botones del sidebar */
            QPushButton {
                background-color: #ffffff;
                color: #4da3af;
                border: 2px solid #4da3af;
                padding: 12px 15px;
                text-align: left;
                font-size: 14px;
                border-radius: 8px;
                margin: 5px 0;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #e6f4f7;
                border-color: #3b8c92;
            }
            
            QPushButton:pressed {
                background-color: #4da3af;
                color: white;
            }
            
            /* Área de contenido principal */
            #mainContent {
                background-color: #f8f9fa;
            }
            
            #welcomeCard {
                background-color: white;
                border-radius: 12px;
                padding: 30px;
                border: 1px solid #e0e0e0;
            }
            
            #welcomeTitle {
                font-size: 24px;
                font-weight: bold;
                color: #4da3af;
                text-align: center;
            }
            
            #welcomeSubtitle {
                font-size: 16px;
                color: #666;
                text-align: center;
            }
            
            /* Componentes generales */
            QLineEdit, QComboBox, QTextEdit {
                background-color: white;
                color: #333;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 6px;
                font-size: 14px;
            }
            
            QLabel {
                color: #333;
                font-size: 14px;
            }
            
            QTableWidget {
                background-color: white;
                alternate-background-color: #f9f9f9;
                gridline-color: #e0e0e0;
                selection-background-color: #4da3af;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
            }
            
            QHeaderView::section {
                background-color: #4da3af;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            
            QTableWidget::item {
                color: #333;
                padding: 8px;
            }
            
            QTableWidget::item:selected {
                background-color: #4da3af;
                color: white;
            }
            
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 5px;
                background: white;
            }
            
            QTabBar::tab {
                background: #f1f1f1;
                border: 1px solid #e0e0e0;
                padding: 8px 15px;
                margin-right: 5px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            
            QTabBar::tab:selected {
                background: #4da3af;
                color: white;
                border-bottom-color: #4da3af;
            }
            
            QTabBar::tab:hover {
                background: #e6f4f7;
            }
        """)
    
    def create_button(self, text, icon_path):
        """Crea un botón con icono"""
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(button.fontMetrics().boundingRect(text).size())
        return button
    
    def gestion_clientes(self):
        """Muestra la vista de gestión de clientes"""
        if not hasattr(self, 'clientes_view'):
            self.clientes_view = ClientesView(self, self.clientes_controller)
        self.stacked_widget.addWidget(self.clientes_view)
        self.stacked_widget.setCurrentWidget(self.clientes_view)
    
    def gestion_servicios(self):
        """Muestra la vista de gestión de servicios"""
        if not hasattr(self, 'servicios_view'):
            self.servicios_view = ServiciosView(self, self.servicios_controller)  # ✅ Pasa ambos argumentos
        self.stacked_widget.addWidget(self.servicios_view)
        self.stacked_widget.setCurrentWidget(self.servicios_view)
    
    def gestion_facturacion(self):
        """Muestra la vista de facturación"""
        if not hasattr(self, 'facturacion_view'):
            self.facturacion_view = FacturacionView(
                self, 
                self.tratamientos_controller,
                self.clientes_controller,
                self.servicios_controller
            )
        self.stacked_widget.addWidget(self.facturacion_view)
        self.stacked_widget.setCurrentWidget(self.facturacion_view)
    
    def gestion_config_empresa(self):
        """Muestra la vista de configuración de empresa"""
        if not hasattr(self, 'config_empresa_view'):
            self.config_empresa_view = ConfiguracionEmpresaView(self)
        self.stacked_widget.addWidget(self.config_empresa_view)
        self.stacked_widget.setCurrentWidget(self.config_empresa_view)
    
    def buscar_ficha_cliente(self):
        """Muestra la vista de búsqueda de fichas de cliente"""
        if not hasattr(self, 'buscar_ficha_view'):
            self.buscar_ficha_view = BuscarFichaClienteView(
                self, 
                self.clientes_controller,
                self.tratamientos_controller
            )
        self.stacked_widget.addWidget(self.buscar_ficha_view)
        self.stacked_widget.setCurrentWidget(self.buscar_ficha_view)
    
    def gestion_estadisticas(self):
        """Muestra la vista de estadísticas con pestañas"""
        tab_widget = QTabWidget()

        if not hasattr(self, 'estadisticas_diarias_view'):
            self.estadisticas_diarias_view = EstadisticasDiariasView(
                self, 
                self.tratamientos_controller
            )
        if not hasattr(self, 'estadisticas_mensuales_view'):
            self.estadisticas_mensuales_view = EstadisticasMensualesView(
                self, 
                self.tratamientos_controller
            )
        if not hasattr(self, 'estadisticas_trimestrales_view'):
            self.estadisticas_trimestrales_view = EstadisticasTrimestralesView(
                self, 
                self.tratamientos_controller
            )

        tab_widget.addTab(self.estadisticas_diarias_view, "Diarias")
        tab_widget.addTab(self.estadisticas_mensuales_view, "Mensuales")
        tab_widget.addTab(self.estadisticas_trimestrales_view, "Trimestrales")

        self.stacked_widget.addWidget(tab_widget)
        self.stacked_widget.setCurrentWidget(tab_widget)