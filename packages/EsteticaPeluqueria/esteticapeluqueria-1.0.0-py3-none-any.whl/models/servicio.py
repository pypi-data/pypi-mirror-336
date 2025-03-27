class Servicio:
    def __init__(self, nombre, precio, duracion):
        self.nombre = nombre
        self.precio = precio
        self.duracion = duracion

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "precio": self.precio,
            "duracion": self.duracion
        }