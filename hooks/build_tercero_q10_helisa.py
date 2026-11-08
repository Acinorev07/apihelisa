from datetime import datetime
import json
from hooks.build_thirdParty_student import build_thirdParty_student
from hooks.build_thirdParty import build_thirdParty
from services.q10.obtener_tercero import obtener_tercero
from services.q10.obtener_estudiante import obtener_estudiante

def build_tercero_q10_helisa(factura):

    # Convertir la fecha de la factura.
    fecha_factura = factura.get("Fecha_factura")

    if not fecha_factura:
        print("La factura no tiene una fecha válida.")

        error = {
            "mensaje":"La factura no tiene una fecha valida",
            "status":404
        }
        return error

    try:
        fecha = datetime.fromisoformat(fecha_factura)
        year_est = fecha.year

    except ValueError:
        print(f"Formato de fecha no válido: {fecha_factura}")

        error = {
            "mensaje":"La factura no tiene un formato de fecha valida",
            "status":404
        }
        return error

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

        if not isinstance(response, dict):
            return {
                "status": 502,
                "mensaje": "No se pudo obtener la información del estudiante desde Q10."
            }

        if not response.get("Numero_identificacion"):
            return {
                "status": 422,
                "mensaje": "El estudiante no tiene número de identificación."
            }

        json_data = build_thirdParty_student(
                         response=response,
                         year_est=year_est
                        )

        return json_data

        

        # Si el campo de Nombre_completo_tercero tiene información se ejecuta este bloque
    elif nombre_tercero:

        print(f"Nombre tercero: {factura.get("Nombre_completo_tercero")}")
          
        consecutivo_tercero = factura.get("Consecutivo_tercero")

        response = obtener_tercero(
                consecutivo_tercero
        )


        if not isinstance(response, dict):
            return {
                "status": 502,
                "mensaje": "No se pudo obtener la información del Tercero desde Q10."
            }

        if not response.get("Numero_identificacion"):
            return {
                "status": 422,
                "mensaje": "El tercero no tiene número de identificación."
            }

        print(f"Registro tercero helisa: {json.dumps(
                        response,
                        indent=4,
                        ensure_ascii=False
                    )}")


        json_data = build_thirdParty(
              response=response,
              year_est=year_est
          )

        return json_data

        
