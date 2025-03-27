# Estilos globales para la aplicación
GLOBAL_STYLES = """
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
    QLineEdit, QComboBox {
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
"""

# Estilos específicos para diálogos
DIALOG_STYLES = """
    QLabel {
        font-size: 14px;
        color: #333;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 5px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QPushButton:pressed {
        background-color: #3e8e41;
    }
"""

# Estilos para QTextEdit
TEXT_EDIT_STYLES = """
    QTextEdit {
        background-color: white;
        color: black;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        font-size: 14px;
    }
"""