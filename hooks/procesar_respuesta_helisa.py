


def procesar_respuesta_helisa(respuesta):
    """
    Normaliza la respuesta de Helisa.
    """

    # Si insertar() devuelve un diccionario,
    # significa que ocurrió un error antes de recibir HTTP.
    if isinstance(respuesta, dict):

        return {
            "ok": False,
            "status": respuesta.get("status", 500),
            "mensaje": respuesta.get("mensaje", "Error desconocido.")
        }

    status_code = respuesta.status_code

    try:
        contenido = respuesta.json()

    except ValueError:
        contenido = respuesta.text

    # NUEVO: verificar si Helisa devuelve un error
    # dentro del contenido, incluso con HTTP 202.
    if isinstance(contenido, dict) and "error" in contenido:

        error = contenido["error"]

        return {
            "ok": False,
            "status": status_code,
            "respuesta": contenido,
            "mensaje": error.get(
                "message",
                "Helisa rechazó los datos."
            ),
            "campos": error.get("fields", [])
        }

    if 200 <= status_code < 300:

        return {
            "ok": True,
            "status": status_code,
            "respuesta": contenido
        }

    return {
        "ok": False,
        "status": status_code,
        "respuesta": contenido
    }
