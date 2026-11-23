
from hooks.configuracion_APIs import obtener_url
from hooks.procesar_respuesta_helisa import procesar_respuesta_helisa
from api.helisa.route import POST
import json


def insertar(json_data):
    """
    Envía un tercero a Helisa y devuelve la respuesta HTTP.
    """

    print("\n===== INSERTAR TERCERO =====")

    try:
        url = obtener_url("helisa", "add_supplier")

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

        print("\n========== RESPUESTA COMPLETA DE HELISA ==========")
        print("HTTP:", response.status_code)
        print("Headers:", dict(response.headers))
        print("Body:", response.text)

        return response

    except Exception as e:
        return {
            "status": 500,
            "mensaje": f"Error al intentar insertar el tercero: {str(e)}"
        }


    

def enviar_supplier_q10_helisa(resultado_generacion):
    """
    Envía a Helisa cada tercero único generado.

    Conserva los errores de construcción y registra
    los resultados de cada intento de inserción.
    """

    resultado = {
        "total_terceros": len(resultado_generacion.get("suppliers", {})),
        "insertados": [],
        "errores_generacion": resultado_generacion.get("errores", []).copy(),
        "errores_insercion": []
    }

    suppliers = resultado_generacion.get("suppliers", {})

    for identificacion, registro in suppliers.items():

        datos_tercero = registro["supplier"]
        facturas = registro["facturas"]

        nombre = datos_tercero.get("name", "Sin nombre")

        print("\n-----------------------------------")
        print(f"supplier: {nombre}")
        print(f"Identificación: {identificacion}")
        print(f"Facturas asociadas: {facturas}")

        try:

            json_data = json.dumps(
                {"supplier": datos_tercero},
                separators=(",", ":"),
                ensure_ascii=False
            )

            respuesta = insertar(json_data=json_data)

            resultado_http = procesar_respuesta_helisa(
                respuesta
            )

            if resultado_http["status"] == 200:
                resultado["insertados"].append({
                    "identificacion": identificacion,
                    "nombre": nombre,
                    "facturas": facturas,
                    "status": resultado_http["status"],
                    "respuesta": resultado_http["respuesta"]
                })

            elif resultado_http["status"] == 202:
                resultado.setdefault("pendientes", []).append({
                    "identificacion": identificacion,
                    "nombre": nombre,
                    "facturas": facturas,
                    "status": 202,
                    "respuesta": resultado_http["respuesta"]
                })

            else:
                resultado["errores_insercion"].append({
                    "identificacion": identificacion,
                    "nombre": nombre,
                    "facturas": facturas,
                    "status": resultado_http["status"],
                    "error": resultado_http.get("mensaje")
                })

        except Exception as e:

            resultado["errores_insercion"].append({
                "identificacion": identificacion,
                "nombre": nombre,
                "facturas": facturas,
                "error": str(e)
            })

    return resultado