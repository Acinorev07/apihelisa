
from datetime import datetime

def form_obtener_tercero():

    fecha_consulta = input(
            "Fecha de consulta YYYY-MM-DD, ENTER = hoy): "
        ).strip()

    # Documento de identidad del tercero
    docId = input("Introduce el documento de identidad del tercero").strip()

    return fecha_consulta, docId