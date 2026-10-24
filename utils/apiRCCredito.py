import os
import requests
from dotenv import load_dotenv


def recibo_caja():

    load_dotenv()

    api_key = os.getenv("Q10_KEY")

    if not api_key:
        print("Error: no se encontró Q10_KEY en el archivo .env")
        return

    url = "https://api.q10.com/v1/pagos/creditos"

    # Filtros de consulta
    fecha_inicio = input(
        "Fecha inicial (según formato de Q10, ENTER para omitir): "
    ).strip()

    fecha_fin = input(
        "Fecha final (según formato de Q10, ENTER para omitir): "
    ).strip()

    offset = input("Offset (ENTER = 0): ").strip()

    limite = input("Límite de registros (ENTER = 100): ").strip()

    codigo_persona = input("Código de persona (opcional): ").strip()


    consecutivo_credito = input("Consecutivo tercero (opcional): ").strip()


    # Q10 exige fechas si no se envía código de persona
    # ni consecutivo de tercero.
    if not codigo_persona and not consecutivo_credito:
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


    try:
        parametros["Offset"] = int(offset) if offset else 0
        parametros["Limit"] = int(limite) if limite else 100
    except ValueError:
        print("El límite y el offset deben ser números enteros.")
        return
    
    if parametros["Offset"] < 0:
        print("El offset no puede ser negativo.")
        return
    
    if not 1 <= parametros["Limit"] <= 1000:
        print("El límite debe estar entre 1 y 1000.")
        return

    if codigo_persona:
        parametros["Codigo_persona"] = codigo_persona

    if consecutivo_credito:
        parametros["Consecutivo_tercero"] = consecutivo_credito


    # IMPORTANTE:
    # La cabecera de autenticación debe coincidir con la
    # indicada en la documentación de tu API Q10.
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
    recibo_caja()