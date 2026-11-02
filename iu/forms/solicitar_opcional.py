

def solicitar_opcional(mensaje, longitud_maxima=None):
    """Solicita un dato opcional y valida su longitud."""
    while True:
        valor = input(mensaje).strip()

        if valor.lower() == "null":
            valor = ""

        if longitud_maxima is not None and len(valor) > longitud_maxima:
            print(
                f"El campo admite como máximo "
                f"{longitud_maxima} caracteres."
            )
            continue

        return valor