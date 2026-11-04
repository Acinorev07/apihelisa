from hooks.configuracion_APIs import obtener_url
from api.q10.route import GET
import json




def obtener_programas_Q10():

    url = obtener_url(
        "q10",
        "obtener_programas"
    )

    limite = input("Límite de registros (ENTER = 100): ").strip()

    offset = input("Offset (ENTER = 0): ").strip()

    estado = input("Ingrese el estado del programa, activo por defecto: ").strip()

    incluir_pensum = input("¿Se debe incluir los pénsum asociados?: ").strip()

    parametros={}

    try:
        parametros["Limit"] = int(limite) if limite else 100
        parametros["Offset"] = int(offset) if offset else 0

        if estado:
            parametros["estado"] = estado

        if incluir_pensum:
            parametros["incluir_pensum"] = incluir_pensum


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
    respuesta = obtener_programas_Q10()

    print("\nProgramas: ")
    print(json.dumps(
         respuesta,
         indent=4,
         ensure_ascii=False
    ))