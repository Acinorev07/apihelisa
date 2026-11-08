import re

def validar_correo(email):
    """Valida de forma básica la estructura de un correo electrónico."""

    correo = email.strip()

    if  correo.lower() == "null":
        return ""

    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.fullmatch(patron, correo) is not None