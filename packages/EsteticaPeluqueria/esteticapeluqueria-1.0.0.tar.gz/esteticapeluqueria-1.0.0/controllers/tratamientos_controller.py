# controllers/tratamientos_controller.py
from models.tratamiento import Tratamiento
from utils.file_manager import load_data, save_data

class TratamientosController:
    def __init__(self):
        self.tratamientos = load_data("data/tratamientos.json")

    def agregar_tratamiento(self, tratamiento):
        self.tratamientos.append(tratamiento.to_dict())
        save_data("data/tratamientos.json", self.tratamientos)

    def obtener_tratamientos_por_cliente(self, dni_cliente):
        return [t for t in self.tratamientos if t["dni_cliente"] == dni_cliente]

    def eliminar_tratamiento(self, dni_cliente, nombre_tratamiento):
        tratamientos_filtrados = [t for t in self.tratamientos if not (t["dni_cliente"] == dni_cliente and t["nombre"] == nombre_tratamiento)]

        if len(tratamientos_filtrados) == len(self.tratamientos):
            return False  # No se eliminó nada porque no se encontró el tratamiento

        self.tratamientos = tratamientos_filtrados
        save_data("data/tratamientos.json", self.tratamientos)
        return True
    
    def obtener_tratamientos(self):
        return self.tratamientos
