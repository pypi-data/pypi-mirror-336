from datetime import datetime
import json
import os

def load_data(filename):
    """Carga datos desde un archivo JSON."""
    try:
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}
    except json.JSONDecodeError:
        return {}

def save_data(filename, data):
    """Guarda datos en un archivo JSON."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def get_invoice_number(file_path="data/invoice_number.json"):
    """Obtiene el número de factura actual."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        return data.get("invoice_number", 1)
    return 1

def update_invoice_number(new_number, file_path="data/invoice_number.json"):
    """Actualiza el número de factura."""
    save_data(file_path, {"invoice_number": new_number})

def get_invoice_folder():
    """Genera la carpeta donde se almacenarán las facturas."""
    today = datetime.today()
    folder_path = os.path.join("facturas", str(today.year), today.strftime("%m"))
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def calculate_iva(amount, rate=0.21):
    """Calcula el IVA y el total."""
    iva = amount * rate
    total = amount + iva
    return iva, total