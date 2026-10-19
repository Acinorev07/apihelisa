from hooks.configuracion_APIs import obtener_url
from api.q10.route import GET
import json

def obtener_facturas():
     url = obtener_url(
                    "q10",
                    "facturas"
            )
    
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

     print("parametros", parametros)

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
     