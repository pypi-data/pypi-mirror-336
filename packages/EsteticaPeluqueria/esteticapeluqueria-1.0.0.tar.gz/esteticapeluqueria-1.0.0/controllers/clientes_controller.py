from datetime import datetime
from models.cliente import Cliente
from utils.file_manager import load_data, save_data

class ClientesController:
    def __init__(self):
        self.clientes = load_data("data/clientes.json")

    def guardar_clientes(self):
        """Guarda los clientes en el archivo JSON"""
        save_data("data/clientes.json", self.clientes)

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente.to_dict())
        self.guardar_clientes()

    def buscar_cliente_por_dni(self, dni):
        for cliente in self.clientes:
            if cliente["dni"] == dni:
                return cliente
        return None

    def actualizar_cliente(self, cliente):
        for i, cl in enumerate(self.clientes):
            if cl["dni"] == cliente.dni:
                self.clientes[i] = cliente.to_dict()
                self.guardar_clientes()
                return True
        return False

    def eliminar_cliente(self, dni):
        for i, cl in enumerate(self.clientes):
            if cl["dni"] == dni:
                del self.clientes[i]
                self.guardar_clientes()
                return True
        return False

    def obtener_clientes(self):
        return self.clientes

    def obtener_bonos_cliente(self, dni):
        """Obtiene los bonos de un cliente"""
        cliente = self.buscar_cliente_por_dni(dni)
        if cliente:
            return cliente.get('bonos', {})
        return {}

    def usar_sesion_bono(self, dni, tipo_bono):
        """Usa una sesión del bono del cliente"""
        try:
            for cliente in self.clientes:
                if cliente['dni'] == dni:
                    if 'bonos' not in cliente:
                        return False
                    
                    if tipo_bono in cliente['bonos'] and cliente['bonos'][tipo_bono]['sesiones'] > 0:
                        cliente['bonos'][tipo_bono]['sesiones'] -= 1
                        cliente['bonos'][tipo_bono]['ultimo_uso'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        self.guardar_clientes()
                        return True
            return False
        except Exception as e:
            print(f"Error al usar sesión de bono: {e}")
            return False

    def agregar_bono(self, dni, tipo_bono, sesiones):
        """Agrega un bono al cliente"""
        try:
            for cliente in self.clientes:
                if cliente['dni'] == dni:
                    if 'bonos' not in cliente:
                        cliente['bonos'] = {}
                    
                    if tipo_bono in cliente['bonos']:
                        cliente['bonos'][tipo_bono]['sesiones'] += sesiones
                    else:
                        cliente['bonos'][tipo_bono] = {
                            'sesiones': sesiones,
                            'ultimo_uso': ''
                        }
                    self.guardar_clientes()
                    return True
            return False
        except Exception as e:
            print(f"Error al agregar bono: {e}")
            return False

    def actualizar_comentarios(self, dni, comentarios):
        """Actualiza los comentarios de un cliente"""
        try:
            for cliente in self.clientes:
                if cliente['dni'] == dni:
                    cliente['comentarios'] = comentarios
                    self.guardar_clientes()
                    return True
            return False
        except Exception as e:
            print(f"Error al actualizar comentarios: {e}")
            return False