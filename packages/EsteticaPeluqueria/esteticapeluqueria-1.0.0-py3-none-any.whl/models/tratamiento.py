# models/tratamiento.py
class Tratamiento:
    def __init__(self, dni_cliente, nombre, fecha, observaciones, precio, duracion):
        self.dni_cliente = dni_cliente
        self.nombre = nombre
        self.fecha = fecha
        self.observaciones = observaciones
        self.precio = precio
        self.duracion = duracion

    def to_dict(self):
        return {
            "dni_cliente": self.dni_cliente,
            "nombre": self.nombre,
            "fecha": self.fecha,
            "observaciones": self.observaciones,
            "precio": self.precio,
            "duracion": self.duracion
        }
