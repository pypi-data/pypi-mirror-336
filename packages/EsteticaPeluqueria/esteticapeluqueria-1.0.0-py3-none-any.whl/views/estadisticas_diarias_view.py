import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
    QHeaderView, QPushButton, QDateEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.enums import TA_CENTER

class EstadisticasDiariasView(QWidget):
    def __init__(self, main_window, tratamientos_controller):
        super().__init__()
        self.main_window = main_window
        self.tratamientos_controller = tratamientos_controller
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Título
        self.label_titulo = QLabel("Estadísticas Diarias")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(self.label_titulo)

        # Selector de fecha
        self.date_selector = QDateEdit()
        self.date_selector.setDisplayFormat("dd/MM/yyyy")
        self.date_selector.setDate(QDate.currentDate())
        self.date_selector.setCalendarPopup(True)
        self.date_selector.dateChanged.connect(self.cargar_estadisticas)
        layout.addWidget(self.date_selector)

        # Dinero generado en el día seleccionado
        self.label_dinero_dia = QLabel()
        self.label_dinero_dia.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.label_dinero_dia)

        # Tabla de tratamientos del día
        self.table_tratamientos = QTableWidget()
        self.table_tratamientos.setColumnCount(4)
        self.table_tratamientos.setHorizontalHeaderLabels(["Hora", "Tratamiento", "Cliente", "Precio"])
        self.table_tratamientos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_tratamientos)

        # Resumen diario
        self.label_resumen = QLabel()
        self.label_resumen.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.label_resumen)

        # Botón para exportar a PDF
        self.btn_exportar_pdf = QPushButton("Exportar Informe Diario a PDF")
        self.btn_exportar_pdf.clicked.connect(self.exportar_pdf)
        layout.addWidget(self.btn_exportar_pdf)

        # Botón para volver al menú principal
        self.btn_volver = QPushButton("Volver al Menú Principal")
        self.btn_volver.clicked.connect(self.volver_al_menu)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)
        self.cargar_estadisticas()

    def cargar_estadisticas(self):
        # Obtener la fecha seleccionada
        fecha_seleccionada = self.date_selector.date()
        dia = fecha_seleccionada.day()
        mes = fecha_seleccionada.month()
        año = fecha_seleccionada.year()

        # Obtener todos los tratamientos
        tratamientos = self.tratamientos_controller.obtener_tratamientos()

        # Filtrar tratamientos del día seleccionado
        tratamientos_dia = [
            t for t in tratamientos
            if datetime.strptime(t["fecha"], "%Y-%m-%d %H:%M:%S").date() == datetime(año, mes, dia).date()
        ]

        # Calcular el dinero generado este día
        dinero_dia = sum(t["precio"] for t in tratamientos_dia)
        self.label_dinero_dia.setText(
            f"Dinero generado el {dia}/{mes}/{año}: €{dinero_dia:.2f}"
        )

        # Mostrar tratamientos del día
        self.table_tratamientos.setRowCount(len(tratamientos_dia))
        for i, tratamiento in enumerate(tratamientos_dia):
            fecha = datetime.strptime(tratamiento["fecha"], "%Y-%m-%d %H:%M:%S")
            self.table_tratamientos.setItem(i, 0, QTableWidgetItem(fecha.strftime("%H:%M")))
            self.table_tratamientos.setItem(i, 1, QTableWidgetItem(tratamiento["nombre"]))
            self.table_tratamientos.setItem(i, 2, QTableWidgetItem(tratamiento["dni_cliente"]))
            self.table_tratamientos.setItem(i, 3, QTableWidgetItem(f"€{tratamiento['precio']:.2f}"))

        # Calcular resumen
        num_tratamientos = len(tratamientos_dia)
        tratamiento_mas_caro = max((t["precio"] for t in tratamientos_dia), default=0)
        tratamiento_mas_barato = min((t["precio"] for t in tratamientos_dia), default=0)
        
        resumen_texto = (
            f"Resumen del día: {num_tratamientos} tratamientos | "
            f"Más caro: €{tratamiento_mas_caro:.2f} | "
            f"Más barato: €{tratamiento_mas_barato:.2f}"
        )
        self.label_resumen.setText(resumen_texto)

    def exportar_pdf(self):
        # Obtener la fecha seleccionada
        fecha_seleccionada = self.date_selector.date()
        dia = fecha_seleccionada.day()
        mes = fecha_seleccionada.month()
        año = fecha_seleccionada.year()
        fecha_str = f"{dia:02d}_{mes:02d}_{año}"

        # Crear la carpeta "EstadisticasDiarias" si no existe
        carpeta = "EstadisticasDiarias"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Crear el archivo PDF dentro de la carpeta
        filename = os.path.join(carpeta, f"Informe_Diario_{fecha_str}.pdf")
        pdf = SimpleDocTemplate(filename, pagesize=letter)

        # Contenido del PDF
        elements = []

        # Agregar logo de la empresa
        try:
            logo_path = "utils/D&G.png"
            logo = Image(logo_path)
            logo.drawHeight = 100
            logo.drawWidth = 100
            logo.hAlign = 'LEFT'
            elements.append(logo)
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")

        # Estilo de texto
        styles = getSampleStyleSheet()
        estilo_titulo = styles["Heading1"]
        estilo_normal = styles["Normal"]
        estilo_titulo.alignment = TA_CENTER
        estilo_normal.alignment = TA_CENTER

        # Título del informe
        titulo = Paragraph(f"Informe Diario - {dia}/{mes}/{año}", estilo_titulo)
        elements.append(titulo)

        # Dinero generado en el día
        dinero_texto = Paragraph(
            f"Dinero generado: €{float(self.label_dinero_dia.text().split('€')[-1]):.2f}",
            estilo_normal
        )
        elements.append(dinero_texto)

        # Resumen del día
        resumen_texto = Paragraph(self.label_resumen.text(), estilo_normal)
        elements.append(resumen_texto)

        # Tabla de tratamientos
        data = [["Hora", "Tratamiento", "Cliente", "Precio"]]
        for row in range(self.table_tratamientos.rowCount()):
            hora = self.table_tratamientos.item(row, 0).text()
            tratamiento = self.table_tratamientos.item(row, 1).text()
            cliente = self.table_tratamientos.item(row, 2).text()
            precio = self.table_tratamientos.item(row, 3).text()
            data.append([hora, tratamiento, cliente, precio])

        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4da3af")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

        # Construir el PDF
        pdf.build(elements)

        # Notificar al usuario
        QMessageBox.information(self, "Éxito", f"Informe diario generado: {filename}")

    def volver_al_menu(self):
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.container)