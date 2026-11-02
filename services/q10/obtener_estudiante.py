from hooks.configuracion_APIs import obtener_url
from api.q10.route import GET


def obtener_estudiante(codigo_estudiante, codigo_programa ):
     # Obtener la URL configurada para este endpoint.
        url = obtener_url(
            "q10",
            "obtener_estudiante"
        )

    # El código del estudiante es obligatorio.
        if not codigo_estudiante or codigo_estudiante.lower() == "null":
            print("Debes ingresar el código o identificación del estudiante.")
            return None

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

        return respuesta