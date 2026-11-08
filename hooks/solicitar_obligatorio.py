from hooks.dividir_texto import dividir_texto

def solicitar_obligatorio(mensaje, longitud_maxima):
    """Solicita un dato hasta que el usuario introduzca un valor."""
    if mensaje is None:

        return {
            "status": 422,
            "mensaje": "El campo obligatorio está vacío."
        }

    valor = str(mensaje).strip()

    if not valor or valor.lower() in ("null", "none"):
        return {
            "status": 422,
            "mensaje": "El campo obligatorio está vacío."
        }

    if longitud_maxima is not None and len(valor) > longitud_maxima:
        cortado = dividir_texto(
                texto=valor,
                limite=longitud_maxima
                )
        return cortado
    
    return valor

