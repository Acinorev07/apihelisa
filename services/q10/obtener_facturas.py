from hooks.configuracion_APIs import obtener_url
from api.q10.route import GET
import json



def obtener_facturas(params):
    # 1. Extraer los valores del diccionario
     fecha_inicio = params.get("fecha_inicio", "")
     fecha_fin = params.get("fecha_fin", "")
     codigo_persona = params.get("codigo_persona", "")
     consecutivo_tercero = params.get("consecutivo_tercero", "")
     codigo_producto = params.get("codigo_producto", "")
     estado = params.get("estado", "")
     limite = params.get("limite", 100)
     offset = params.get("offset", 0)


     url = obtener_url(
                    "q10",
                    "facturas"
            )
    
   

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

     print(f"parametros: {parametros}")

     response = GET(url, params = parametros)

     if response is not None:
        print("\nCódigo HTTP:", response.status_code)
        print("\nRespuesta de Helisa:")

        try:
            
            return response.json()
        
        except ValueError:
            print(response.text)

     else:

        print("errrroooor")
           
     