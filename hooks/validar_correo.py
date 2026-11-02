import re

def validar_correo(email):
    """Valida de forma básica la estructura de un correo electrónico."""
    if not email:
        return True

    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.fullmatch(patron, email) is not None