def validar_dni(dni):
    if len(dni) != 8 or not dni.isdigit():
        return False
    return True