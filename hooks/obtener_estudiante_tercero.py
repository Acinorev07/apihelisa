

def obtener_estudiante_tercero(campo_estudiante,campo_tercero,factura):
    """
    Busca primero la identificación del estudiante.
    Si no existe, utiliza la identificación del tercero.
    """

    for campo in (
        campo_estudiante,
        campo_tercero
    ):
        identificacion = factura.get(campo)

        if identificacion is None:
            continue

        identificacion = str(identificacion).strip()

        if identificacion and identificacion.lower() != "null":
            try:
                return identificacion
            except ValueError:
                continue

    return None