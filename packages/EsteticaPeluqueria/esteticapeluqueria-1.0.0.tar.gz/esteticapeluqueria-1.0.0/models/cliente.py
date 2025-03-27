class Cliente:
    def __init__(self, dni, nombre, apellido, telefono, email, bonos=None):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.bonos = bonos if bonos else {}  # Diccionario: {tipo_bono: sesiones_restantes}

    def to_dict(self):
        return {
            "dni": self.dni,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "email": self.email,
            "bonos": self.bonos
        }
    
    def usar_sesion_bono(self, tipo_bono):
        if tipo_bono in self.bonos and self.bonos[tipo_bono] > 0:
            self.bonos[tipo_bono] -= 1
            return True
        return False
    
    def agregar_bono(self, tipo_bono, sesiones):
        if tipo_bono in self.bonos:
            self.bonos[tipo_bono] += sesiones
        else:
            self.bonos[tipo_bono] = sesiones