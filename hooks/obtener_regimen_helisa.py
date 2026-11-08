
from hooks.normalizar_texto import normalizar_texto

def obtener_regimen_helisa(responsabilidades, regimen_tag):
    if not isinstance(responsabilidades, list):
        return {
            "ok": False,
            "mensaje": "Las responsabilidades del RUT no tienen un formato válido."
        }

    if not responsabilidades:
        return {
            "ok": False,
            "mensaje": "El tercero no tiene responsabilidades del RUT registradas."
        }

    etiquetas = []

    for responsabilidad in responsabilidades:

        clave = normalizar_texto(responsabilidad)

        codigo = regimen_tag.get(clave)

        if codigo is None:
            return {
                "ok": False,
                "mensaje": f"Responsabilidad no reconocida: {responsabilidad}"
            }

        if codigo not in etiquetas:
            etiquetas.append(codigo)

    if len(etiquetas) > 1:
        return {
            "ok": False,
            "mensaje": (
                "El tercero tiene varias responsabilidades tributarias. "
                "Se necesita definir cuál debe enviarse a Helisa."
            )
        }

    return {
        "ok": True,
        "tag": etiquetas[0]
    }

