
import re

def validar_documento_tercero(mensaje="Introduce el documento de identidad del tercero: "):
    """
    Solicita un documento de identidad y valida que contenga
    únicamente dígitos del 0 al 9.

    Retorna el documento como str para conservar los ceros iniciales.
    """
    while True:
        documento = input(mensaje).strip()

        if re.fullmatch(r"[0-9]+", documento):
            return documento

        print(
            "Error: el documento debe contener únicamente números. "
            "Inténtalo nuevamente."
        )
