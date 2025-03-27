class Factura:
    def __init__(self, numero, cliente, servicios, total):
        self.numero = numero
        self.cliente = cliente
        self.servicios = servicios
        self.total = total

    def to_dict(self):
        return {
            "numero": self.numero,
            "cliente": self.cliente,
            "servicios": self.servicios,
            "total": self.total
        }