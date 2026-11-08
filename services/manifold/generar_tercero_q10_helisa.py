
from hooks.build_tercero_q10_helisa import build_tercero_q10_helisa
from hooks.configuracion_APIs import obtener_url
from api.helisa.route import POST
import json


def insertar(json_data):
    """
    Envía un tercero a Helisa y devuelve la respuesta HTTP.
    """

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


def generar_terceros_q10_helisa(facturas):
    """
    Construye los terceros y los agrupa por identificación.
    Todavía no realiza inserciones en Helisa.
    """

    resultado = {
        "terceros": {},
        "errores": []
    }

    for indice, factura in enumerate(facturas, start=1):

        try:
            tercero = build_tercero_q10_helisa(
                factura=factura
            )

            if (
                not isinstance(tercero, dict)
                or "thirdParty" not in tercero
            ):
                resultado["errores"].append({
                    "factura_indice": indice,
                    "numero_factura": factura.get("Numero_factura"),
                    "error": tercero
                })
                continue

            datos_tercero = tercero["thirdParty"]

            identificacion = str(
                datos_tercero.get("id") or ""
            ).strip()

            digito = str(
                datos_tercero.get("checkDigit") or ""
            ).strip()

            if not identificacion:
                resultado["errores"].append({
                    "factura_indice": indice,
                    "numero_factura": factura.get("Numero_factura"),
                    "error": "El tercero no tiene identificación."
                })
                continue

            clave = (
                f"{identificacion}-{digito}"
                if digito
                else identificacion
            )

            numero_factura = factura.get("Numero_factura")

            if clave in resultado["terceros"]:

                resultado["terceros"][clave]["facturas"].append(
                    numero_factura
                )

            else:

                resultado["terceros"][clave] = {
                    "thirdParty": datos_tercero,
                    "facturas": [numero_factura]
                }

        except Exception as e:

            resultado["errores"].append({
                "factura_indice": indice,
                "numero_factura": factura.get("Numero_factura"),
                "error": str(e)
            })

    return resultado


def procesar_respuesta_helisa(respuesta):
    """
    Normaliza la respuesta de Helisa.
    """

    # Si insertar() devuelve un diccionario,
    # significa que ocurrió un error antes de recibir HTTP.
    if isinstance(respuesta, dict):

        return {
            "ok": False,
            "status": respuesta.get("status", 500),
            "mensaje": respuesta.get("mensaje", "Error desconocido.")
        }

    status_code = respuesta.status_code

    try:
        contenido = respuesta.json()

    except ValueError:
        contenido = respuesta.text

    if 200 <= status_code < 300:

        return {
            "ok": True,
            "status": status_code,
            "respuesta": contenido
        }

    return {
        "ok": False,
        "status": status_code,
        "respuesta": contenido
    }


def enviar_terceros_q10_helisa(resultado_generacion):
    """
    Envía a Helisa cada tercero único generado.

    Conserva los errores de construcción y registra
    los resultados de cada intento de inserción.
    """

    resultado = {
        "total_terceros": len(resultado_generacion.get("terceros", {})),
        "insertados": [],
        "errores_generacion": resultado_generacion.get("errores", []).copy(),
        "errores_insercion": []
    }

    terceros = resultado_generacion.get("terceros", {})

    for identificacion, registro in terceros.items():

        datos_tercero = registro["thirdParty"]
        facturas = registro["facturas"]

        nombre = datos_tercero.get("name", "Sin nombre")

        print("\n-----------------------------------")
        print(f"Tercero: {nombre}")
        print(f"Identificación: {identificacion}")
        print(f"Facturas asociadas: {facturas}")

        try:

            json_data = json.dumps(
                {"thirdParty": datos_tercero},
                separators=(",", ":"),
                ensure_ascii=False
            )

            respuesta = insertar(json_data=json_data)

            resultado_http = procesar_respuesta_helisa(
                respuesta
            )

            if resultado_http["ok"]:

                print(
                    f"Helisa respondió HTTP {resultado_http['status']}"
                )

                resultado["insertados"].append({
                    "identificacion": identificacion,
                    "nombre": nombre,
                    "facturas": facturas,
                    "status": resultado_http["status"],
                    "respuesta": resultado_http["respuesta"]
                })

            else:

                print(
                    f"Error HTTP {resultado_http['status']}"
                )

                resultado["errores_insercion"].append({
                    "identificacion": identificacion,
                    "nombre": nombre,
                    "facturas": facturas,
                    "status": resultado_http["status"],
                    "error": resultado_http.get(
                        "mensaje",
                        resultado_http.get("respuesta")
                    )
                })

        except Exception as e:

            resultado["errores_insercion"].append({
                "identificacion": identificacion,
                "nombre": nombre,
                "facturas": facturas,
                "error": str(e)
            })

    return resultado

