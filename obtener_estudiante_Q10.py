
from hooks.configuracion_APIs import obtener_url
from api.q10.route import GET
import json


def obtener_estudiante_Q10():

    # Obtener la URL configurada para este endpoint.
    url = obtener_url(
        "q10",
        "obtener_estudiante"
    )

    codigo_estudiante = input(
        "Código o identificación del estudiante: "
    ).strip()

    # El código del estudiante es obligatorio.
    if not codigo_estudiante or codigo_estudiante.lower() == "null":
        print("Debes ingresar el código o identificación del estudiante.")
        return None

    codigo_programa = input(
        "Código del programa (opcional): "
    ).strip()

    # Construir la ruta con el identificador del estudiante.
    if "{id}" in url:
        url = url.replace("{id}", codigo_estudiante)
    else:
        url = f"{url.rstrip('/')}/{codigo_estudiante}"

    # Codigo_programa es un parámetro opcional.
    parametros = {}

    if codigo_programa and codigo_programa.lower() != "null":
        parametros["Codigo_programa"] = codigo_programa

    print(f"\nURL solicitada: {url}")
    print(f"Parámetros: {parametros}")

    # Realizar la petición.
    response = GET(url, params=parametros)

    if response is None:
        print("No se recibió una respuesta del servidor.")
        return None

    print("\nCódigo HTTP:", response.status_code)

    try:
        respuesta = response.json()
    except ValueError:
        print("\nLa respuesta no contiene JSON válido:")
        print(response.text)
        return None

    if response.status_code == 200:
        print("\nDetalle del estudiante:")
        return respuesta

    print("\nError en la consulta:")
    print(json.dumps(
        respuesta,
        indent=4,
        ensure_ascii=False
    ))

    return respuesta


if __name__ == "__main__":

    respuesta = obtener_estudiante_Q10()

    if respuesta is not None:
        print("\nRespuesta completa:")
        print(json.dumps(
            respuesta,
            indent=4,
            ensure_ascii=False
        ))
