
from hooks.build_tercero_q10_helisa import build_tercero_q10_helisa
from hooks.configuracion_APIs import obtener_url
from api.helisa.route import POST
import json
import requests


def insertar(json_data):

    print("\n===== INSERTAR TERCERO =====")

    try:
        url = obtener_url("helisa", "create_tercero")

        if not url:
            return {
                "status": 500,
                "mensaje": "No se encontró la URL de creación de terceros."
            }

        response = POST(url, json_data)

        if response is None:
            return {
                "status": 502,
                "mensaje": "No se recibió respuesta de Helisa."
            }

        return response

    except Exception as e:
        return {
            "status": 500,
            "mensaje": f"Error al intentar insertar el tercero: {str(e)}"
        }


def insertar_tercero_q10_helisa(factura):

    tercero = build_tercero_q10_helisa(factura=factura)

    if not isinstance(tercero, dict) or "thirdParty" not in tercero:
    
            print("No se puede enviar el tercero a Helisa.")
    
            print(json.dumps(
                tercero,
                indent=4,
                ensure_ascii=False
            ))
    
    else:

        print(json.dumps(
                    tercero,
                    indent=4,
                    ensure_ascii=False
                ))

        json_data = json.dumps(
                tercero,
                separators=(",", ":")
            )

        # respuesta = insertar(
        #     json_data=json_data
        #     )

        if isinstance(respuesta, dict):

            return respuesta

        else:

            print(f"Código HTTP: {respuesta.status_code}")

            try:
                resultado = respuesta.json()
                return resultado
            
               
            except requests.exceptions.JSONDecodeError:
                print(respuesta.text)
