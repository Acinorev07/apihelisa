from hooks.dividir_texto import dividir_texto

def solicitar(mensaje, longitud_maxima=None):
    """Solicita un dato, valida su longitud y si el dato esta vacio o es nulo, lo coviente a vacio ""."""

    if mensaje is None:
        return ""

    valor = str(mensaje).strip()

    if valor.lower() in ("null", "none"):
        return ""

    if longitud_maxima is not None and len(valor) > longitud_maxima:
        return dividir_texto(valor, longitud_maxima)

    return valor