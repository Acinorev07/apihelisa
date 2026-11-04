
from iu.forms.solicitar_id  import solicitar_id
from hooks.validarDi import validar_documento_tercero
from services.q10.obtener_estudiante import obtener_estudiante
from services.q10.obtener_tercero import obtener_tercero
from hooks.obtener_facturas_json import cargar_facturas
from datetime import datetime
import json
import string


def insertar_tercero_q10_helisa():
    # Se obtienen todas las facturas.
    facturas = cargar_facturas()

    # Se selecciona una factura del conjunto de datos
    factura = facturas[0]

    # Obtener el tipo de identificación desde Q10.
    equivalencias_documentos = {
        "1": "C",
        "70": "X",
        "2": "T",
        "13": "A"

    }


    # Convertir la fecha de la factura.
    fecha_factura = factura.get("Fecha_factura")

    if not fecha_factura:
        print("La factura no tiene una fecha válida.")
        return None

    try:
        fecha = datetime.fromisoformat(fecha_factura)
        year_est = fecha.year

    except ValueError:
        print(f"Formato de fecha no válido: {fecha_factura}")
        return None


    # Se valida que la factura sea para un estudiante o para un tercero
    nombre_estudiante = factura.get("Nombre_completo_estudiante")
    nombre_tercero = factura.get("Nombre_completo_tercero")


    # Si el campo de Nombre_completo_estudiante tiene información se ejecuta este bloque
    if nombre_estudiante:
        print(f"Nombre estudiante: {nombre_estudiante}")

        response = obtener_estudiante(
                codigo_estudiante=factura.get("Codigo_estudiante"),
                codigo_programa = ""
                )

        tipo_identificacion = response.get("Codigo_tipo_identificacion")
        
        tipo_documento = equivalencias_documentos.get(
            tipo_identificacion,
            ""
        )


        print(json.dumps(
                response,
                indent=4,
                ensure_ascii=False
            ))

            
        nuevo_tercero = {
            "thirdParty": {
                "secondLastName": response.get("Segundo_apellido"),
                "cree": False,
                "firstName": response.get("Primer_nombre"),
                "economicActivity": "",
                "city": response.get("Lugar_residencia"),
                "documentType": {
                    "tag": tipo_documento
                },
                "year": year_est,
                "nature": {
                    "value": 0
                },
                "firstLastName": response.get("Primer_apellido"),
                "name": nombre_estudiante,
                "id": response.get("Numero_identificacion"),
                "checkDigit": "",
                "regimen": {
                    "tag": ""
                },
                "secondName": response.get("Segundo_nombre"),
                "userCode": 1,
                "telephones": response.get("Telefono"),
                "cellphone": response.get("Celular"),
                "email": response.get("Email"),
                "address": response.get("Direccion"),
            }
        }
        # 4. Serializar una sola vez.
        json_data = json.dumps(
            nuevo_tercero,
            ensure_ascii=False,
            separators=(",", ":"),
        )


        print("\nTercero preparado:")
        print(json.dumps(
            nuevo_tercero,
            ensure_ascii=False,
            indent=4,
        ))

        return nuevo_tercero

    # Si el campo de Nombre_completo_tercero tiene información se ejecuta este bloque
    if nombre_tercero:

        print(f"Nombre tercero: {factura.get("Nombre_completo_tercero")}")

        consecutivo_tercero = factura.get("Consecutivo_tercero")

        response = obtener_tercero(
                consecutivo_tercero
        )
        tipo_identificacion = response.get("Codigo_tipo_identificacion")
        
        tipo_documento = equivalencias_documentos.get(
            tipo_identificacion,
            ""
        )

        numero_identificacio = response.get("Numero_identificacion").strip().split("-")

        limpio = [p.strip(string.punctuation) for p in numero_identificacio ]

        naturaleza = response.get("Tipo")


        nuevo_tercero = {
                    "thirdParty": {
                        "secondLastName": "",
                        "cree": False,
                        "firstName": "",
                        "economicActivity": "",
                        "city": "",
                        "documentType": {
                            "tag": tipo_documento
                        },
                        "year": year_est,
                        "nature": {
                            "value": 0 if naturaleza == "Jurídica" else 1
                        },
                        "firstLastName": "",
                        "name": nombre_tercero,
                        "id": limpio[0],
                        "checkDigit": limpio[1] if limpio[1] is not "" else "",
                        "regimen": {
                            "tag": ""
                        },
                        "secondName": "",
                        "userCode": 1,
                        "telephones": "",
                        "cellphone": response.get("Telefono"),
                        "email": response.get("Correo_electronico"),
                        "address": response.get("Direccion"),
                    }
                }

        return nuevo_tercero

         


        



if __name__ == "__main__":

    facturas = insertar_tercero_q10_helisa()   

    print(json.dumps(
        facturas,
        indent=4,
        ensure_ascii=False
    ))