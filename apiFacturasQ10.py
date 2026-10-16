
import os
import requests
from datetime import datetime
from dotenv import load_dotenv


def consultar_facturas():
    load_dotenv()

    api_key = os.getenv("Q10_KEY")

    if not api_key:
        print("Error: no se encontró Q10_KEY en el archivo .env")
        return

    url = "https://api.q10.com/v1/facturas"

    # Filtros de consulta
    fecha_inicio = input(
        "Fecha inicial (según formato de Q10, ENTER para omitir): "
    ).strip()

    fecha_fin = input(
        "Fecha final (según formato de Q10, ENTER para omitir): "
    ).strip()

    codigo_persona = input("Código de persona (opcional): ").strip()
    consecutivo_tercero = input("Consecutivo tercero (opcional): ").strip()
    codigo_producto = input("Código de producto (opcional): ").strip()
    estado = input("Estado (1 anulada, 2 pagada, 3 abonada, 4 pendiente): ").strip()
    limite = input("Límite de registros (ENTER = 100): ").strip()
    offset = input("Offset (ENTER = 0): ").strip()

    # Q10 exige fechas si no se envía código de persona
    # ni consecutivo de tercero.
    if not codigo_persona and not consecutivo_tercero:
        if not fecha_inicio or not fecha_fin:
            print(
                "Debes indicar ambas fechas, o proporcionar "
                "un código de persona o consecutivo de tercero."
            )
            return

    parametros = {}

    if fecha_inicio:
        parametros["Fecha_inicio"] = fecha_inicio

    if fecha_fin:
        parametros["Fecha_fin"] = fecha_fin

    if codigo_persona:
        parametros["Codigo_persona"] = codigo_persona

    if consecutivo_tercero:
        parametros["Consecutivo_tercero"] = consecutivo_tercero

    if codigo_producto:
        parametros["Codigo_producto"] = codigo_producto

    if estado:
        if estado not in {"1", "2", "3", "4"}:
            print("Estado inválido. Utiliza 1, 2, 3 o 4.")
            return
        parametros["Estado"] = estado

    try:
        parametros["Limit"] = int(limite) if limite else 100
        parametros["Offset"] = int(offset) if offset else 0
    except ValueError:
        print("El límite y el offset deben ser números enteros.")
        return

    if not 1 <= parametros["Limit"] <= 1000:
        print("El límite debe estar entre 1 y 1000.")
        return

    if parametros["Offset"] < 0:
        print("El offset no puede ser negativo.")
        return

    # IMPORTANTE:
    # La cabecera de autenticación debe coincidir con la
    # indicada en la documentación de tu API Q10.
    # No asumimos que sea Bearer, Api-Key ni HMAC.
    headers = {
        "Accept": "application/json",
        "Api-Key": api_key,
    }

    try:
        response = requests.get(
            url,
            params=parametros,
            headers=headers,
            timeout=30,
        )

        print("\nCódigo HTTP:", response.status_code)
        print("URL consultada:", response.url)

        try:
            resultado = response.json()
            print("\nRespuesta:")
            import json
            print(json.dumps(resultado, indent=4, ensure_ascii=False))
        except ValueError:
            print(response.text)

    except requests.RequestException as error:
        print("Error de conexión:", error)


if __name__ == "__main__":
    consultar_facturas()
