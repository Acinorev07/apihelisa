
def construir_nombre(
    primer_apellido,
    segundo_apellido,
    primer_nombre,
    segundo_nombre
):
    partes = [
        primer_apellido,
        segundo_apellido,
        primer_nombre,
        segundo_nombre
    ]

    return " ".join(
        str(parte).strip()
        for parte in partes
        if parte is not None and str(parte).strip()
    )

