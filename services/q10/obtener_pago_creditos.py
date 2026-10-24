from hooks.configuracion_APIs import obtener_url
from api.q10.route import GET
import json


def obtener_pago_creditos():

    url = obtener_url(
        "q10",
        "pago_creditos"
    )

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

    print(f"parametros: {parametros}")

    response = GET(url, params = parametros)

    if response is not None:
        print("\nCódigo HTTP:", response.status_code)
        print("\nRespuesta de Helisa:")

        try:
            
            return json.dumps(
                    response.json(),
                    indent=4,
                    ensure_ascii=False,
                )
        
        except ValueError:
            print(response.text)
    
    else:

         print("errrroooor")