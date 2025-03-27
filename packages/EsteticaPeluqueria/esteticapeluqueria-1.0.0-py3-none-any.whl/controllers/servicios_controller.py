from models.servicio import Servicio
from utils.file_manager import load_data, save_data

class ServiciosController:
    def __init__(self):
        self.servicios = load_data("data/servicios.json") or []

    def agregar_servicio(self, servicio_data):
        self.servicios.append(servicio_data)
        save_data("data/servicios.json", self.servicios)
        return True

    def obtener_servicios(self):
        return self.servicios

    def buscar_servicio_por_nombre(self, nombre):
        for servicio in self.servicios:
            if servicio["nombre"] == nombre:
                return servicio
        return None

    def actualizar_servicio(self, servicio_data, nombre_anterior):
        for i, s in enumerate(self.servicios):
            if s["nombre"] == nombre_anterior:
                self.servicios[i] = servicio_data
                save_data("data/servicios.json", self.servicios)
                return True
        return False

    def eliminar_servicio(self, nombre):
        self.servicios = [s for s in self.servicios if s["nombre"] != nombre]
        save_data("data/servicios.json", self.servicios)
        return True