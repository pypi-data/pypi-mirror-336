import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.enums import TA_CENTER

class EstadisticasTrimestralesView(QWidget):
    def __init__(self, main_window, tratamientos_controller):
        super().__init__()
        self.main_window = main_window
        self.tratamientos_controller = tratamientos_controller
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Título
        self.label_titulo = QLabel("Estadísticas Trimestrales")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(self.label_titulo)

        # Selector de trimestre
        self.combo_trimestre = QComboBox()
        trimestres = ["Enero-Marzo", "Abril-Junio", "Julio-Septiembre", "Octubre-Diciembre"]
        self.combo_trimestre.addItems(trimestres)
        self.combo_trimestre.currentIndexChanged.connect(self.cargar_estadisticas)
        layout.addWidget(self.combo_trimestre)

        # Dinero generado en el trimestre seleccionado
        self.label_dinero_trimestre = QLabel()
        layout.addWidget(self.label_dinero_trimestre)

        # Tabla de tratamientos más vendidos
        self.table_tratamientos = QTableWidget()
        self.table_tratamientos.setColumnCount(3)
        self.table_tratamientos.setHorizontalHeaderLabels(["Tratamiento", "Cantidad", "Total Generado"])
        self.table_tratamientos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_tratamientos)

        # Botón para exportar a PDF
        self.btn_exportar_pdf = QPushButton("Exportar Informe a PDF")
        self.btn_exportar_pdf.clicked.connect(self.exportar_pdf)
        layout.addWidget(self.btn_exportar_pdf)

        # Botón para volver al menú principal
        self.btn_volver = QPushButton("Volver al Menú Principal")
        self.btn_volver.clicked.connect(self.volver_al_menu)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)
        self.cargar_estadisticas()

    def cargar_estadisticas(self):
        # Obtener el trimestre seleccionado
        trimestre_seleccionado = self.combo_trimestre.currentIndex() + 1

        # Rangos de meses para cada trimestre
        rangos_meses = {
            1: (1, 3),  # Enero-Marzo
            2: (4, 6),  # Abril-Junio
            3: (7, 9),  # Julio-Septiembre
            4: (10, 12)  # Octubre-Diciembre
        }
        mes_inicio, mes_fin = rangos_meses[trimestre_seleccionado]

        # Obtener los tratamientos
        tratamientos = self.tratamientos_controller.obtener_tratamientos()

        # Filtrar tratamientos del trimestre seleccionado
        tratamientos_trimestre = [
            t for t in tratamientos
            if mes_inicio <= datetime.strptime(t["fecha"], "%Y-%m-%d %H:%M:%S").month <= mes_fin
        ]

        # Calcular el dinero generado este trimestre
        dinero_trimestre = sum(t["precio"] for t in tratamientos_trimestre)
        self.label_dinero_trimestre.setText(
            f"Dinero generado en {self.combo_trimestre.currentText()}: €{dinero_trimestre:.2f}"
        )

        # Calcular tratamientos más vendidos
        tratamientos_vendidos = {}
        for t in tratamientos_trimestre:
            nombre = t["nombre"]
            if nombre in tratamientos_vendidos:
                tratamientos_vendidos[nombre]["cantidad"] += 1
                tratamientos_vendidos[nombre]["total"] += t["precio"]
            else:
                tratamientos_vendidos[nombre] = {
                    "cantidad": 1,
                    "total": t["precio"]
                }

        # Ordenar por cantidad vendida
        tratamientos_ordenados = sorted(
            tratamientos_vendidos.items(),
            key=lambda x: x[1]["cantidad"],
            reverse=True
        )

        # Mostrar en la tabla
        self.table_tratamientos.setRowCount(len(tratamientos_ordenados))
        for i, (nombre, datos) in enumerate(tratamientos_ordenados):
            self.table_tratamientos.setItem(i, 0, QTableWidgetItem(nombre))
            self.table_tratamientos.setItem(i, 1, QTableWidgetItem(str(datos["cantidad"])))
            self.table_tratamientos.setItem(i, 2, QTableWidgetItem(f"€{datos['total']:.2f}"))

    def exportar_pdf(self):
        # Obtener el trimestre seleccionado
        trimestre_seleccionado = self.combo_trimestre.currentIndex() + 1
        trimestre_nombre = self.combo_trimestre.currentText()

        # Crear la carpeta "EstadisticasTrimestrales" si no existe
        carpeta = "EstadisticasTrimestrales"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Crear el archivo PDF dentro de la carpeta
        filename = os.path.join(carpeta, f"Informe_Trim_{trimestre_nombre.replace('-', '_')}.pdf")
        pdf = SimpleDocTemplate(filename, pagesize=letter)

        # Contenido del PDF
        elements = []

        # Agregar logo de la empresa sin distorsión
        try:
            logo_path = "utils/D&G.png"  # Asegúrate de que el logo esté en esta ruta
            logo = Image(logo_path)
            logo.drawHeight = 100
            logo.drawWidth = 100
            logo.hAlign = 'CENTER'
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
        titulo = Paragraph(f"Informe Trimestral - {trimestre_nombre}", estilo_titulo)
        elements.append(titulo)

        # Dinero generado en el trimestre
        dinero_texto = Paragraph(
            f"Dinero generado: €{float(self.label_dinero_trimestre.text().split('€')[-1]):.2f}",
            estilo_normal
        )
        elements.append(dinero_texto)

        # Tabla de tratamientos más vendidos
        data = [["Tratamiento", "Cantidad", "Total Generado"]]
        for row in range(self.table_tratamientos.rowCount()):
            tratamiento = self.table_tratamientos.item(row, 0).text()
            cantidad = self.table_tratamientos.item(row, 1).text()
            total = self.table_tratamientos.item(row, 2).text()
            data.append([tratamiento, cantidad, total])

        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4da3af")),  # Turquesa
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
        QMessageBox.information(self, "Éxito", f"Informe generado exitosamente: {filename}")

    def volver_al_menu(self):
        # Restaurar el menú principal usando QStackedWidget
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.container)