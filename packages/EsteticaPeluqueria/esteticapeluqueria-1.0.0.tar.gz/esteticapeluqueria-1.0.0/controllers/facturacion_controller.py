from models.factura import Factura
from utils.file_manager import load_data, save_data

class FacturacionController:
    def __init__(self):
        self.facturas = load_data("data/facturas.json")
        self.clientes = load_data("data/clientes.json")
        self.servicios = load_data("data/servicios.json")
    
    def buscar_cliente_por_dni(self, dni):
        for cliente in self.clientes:
            if cliente["dni"] == dni:
                return cliente
        return None
    
    def obtener_servicios(self):
        return self.servicios
    
    def generar_factura(self, dni, servicios_seleccionados):
        cliente = self.buscar_cliente_por_dni(dni)
        servicios = [servicio for servicio in self.servicios if servicio["nombre"] in servicios_seleccionados]
        total = sum(servicio["precio"] for servicio in servicios)
        
        factura = Factura(len(self.facturas) + 1, cliente, servicios, total)
        self.facturas.append(factura.to_dict())
        save_data("data/facturas.json", self.facturas)