
from hooks.configuracion_APIs import obtener_url
from api.q10.route import GET


def obtener_terceros(estado, offset=0, limite=100):

    url = obtener_url(
        "q10",
        "obtener_terceros"
    )

    # 1. Validar el estado.
    if not estado:
        print("Debes ingresar el estado del tercero.")
        return None

    estado = estado.strip().capitalize()

    if estado not in {"Activo", "Inactivo"}:
        print("Estado inválido. Utiliza Activo o Inactivo.")
        return None

    # 2. Validar el límite y el offset.
    try:
        offset = int(offset) if offset != "" else 0
        limite = int(limite) if limite != "" else 100

    except (ValueError, TypeError):
        print("El límite y el offset deben ser números enteros.")
        return None

    if offset < 0:
        print("El offset no puede ser negativo.")
        return None

    if not 1 <= limite <= 1000:
        print("El límite debe estar entre 1 y 1000.")
        return None

    # 3. Construir los parámetros de consulta.
    parametros = {
        "Estado": estado,
        "Offset": offset,
        "Limit": limite
    }

    print(f"\nURL solicitada: {url}")
    print(f"Parámetros: {parametros}")

    # 4. Consultar Q10.
    response = GET(url, params=parametros)

    if response is None:
        print("No se recibió una respuesta del servidor.")
        return None

    print("\nCódigo HTTP:", response.status_code)

    try:
        respuesta = response.json()

    except ValueError:
        print("La respuesta no contiene JSON válido.")
        print(response.text)
        return None

    if response.status_code == 200:
        print("\nTerceros obtenidos correctamente.")
        return respuesta

    return None

