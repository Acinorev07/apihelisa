from hooks.configuracion_APIs import obtener_url
from api.q10.route import GET

def obtener_tercero(consecutivo_tercero):

    url = obtener_url(
        "q10",
        "obtener_tercero"
    )


    # Construir la ruta con el identificador del tercero.
    if "{id}" in url:
        url = url.replace("{id}", int(consecutivo_tercero))
    else:
        url = f"{url.rstrip('/')}/{int(consecutivo_tercero)}"

    # parametros = {
    #     "id":int(consecutivo_tercero)
    # }

    print(f"\nURL solicitada: {url}")
    # print(f"Parámetros: {parametros}")


    # Realizar la petición.
    response = GET(url)

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
        # print("\nDetalle del estudiante:")
        return respuesta

    return respuesta

