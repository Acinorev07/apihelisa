from hooks.configuracion_APIs import obtener_url
from api.q10.route import GET
import json


def obtener_productos_q10():

    url = obtener_url(
        "q10",
        "obtener_productos"
    )

    estado = input("Ingrese el estado del producto (true/false): ").strip()
    limite = input("Límite de registros (ENTER = 100): ").strip()

    offset = input("Offset (ENTER = 0): ").strip()

    parametros={}

    try:
        
        parametros["estado"] = str(estado) if estado else "true"

        parametros["Limit"] = int(limite) if limite else 100
        parametros["Offset"] = int(offset) if offset else 0

    except ValueError:
        print("El límite y el offset deben ser números enteros.")
        return

    if not 1 <= parametros["Limit"] <= 5000:
             print("El límite debe estar entre 1 y 5000.")
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


if __name__ == "__main__":
    respuesta = obtener_productos_q10()

    print("\nProductos: ")
    print(f"\nCantidad de productos: {len(respuesta)}")
    
    for producto in respuesta:

        print(f"Codigo: {producto.get("Codigo")} | Nombre: {producto.get("Nombre")} | Valor neto: {producto.get("Valor_neto")}")
         
    
