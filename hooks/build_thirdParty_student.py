import json

from hooks.solicitar import solicitar
from hooks.obtener_archivo_json import cargar_archivo
from hooks.solicitar_obligatorio import solicitar_obligatorio
from hooks.validarDi import validar_documento_tercero
from hooks.construir_nombre import construir_nombre
from hooks.validar_correo import validar_correo

def build_thirdParty_student(response, year_est):

    equivalencias = cargar_archivo(
        "validaciones_tercero_helisa.json"
    )

    # 1. Obtener las equivalencias de documentos
    equivalencias_documentos = equivalencias["equivalencias_documentos"]

    tipo_identificacion = solicitar(
        response.get("Codigo_tipo_identificacion"),
        2
    )

    tipo_documento = equivalencias_documentos.get(
        tipo_identificacion
    )

    if not tipo_documento:
        return {
            "status": 422,
            "mensaje": f"Tipo de identificación no reconocido: {tipo_identificacion}"
        }

    # 2. Obtener los nombres y apellidos
    primer_apellido = solicitar(response.get("Primer_apellido"))
    segundo_apellido = solicitar(response.get("Segundo_apellido"))
    primer_nombre = solicitar(response.get("Primer_nombre"))
    segundo_nombre = solicitar(response.get("Segundo_nombre"))

    ciudad = solicitar(
        response.get("Lugar_residencia"),
        5
    )

    build_name = construir_nombre(
        primer_apellido,
        segundo_apellido,
        primer_nombre,
        segundo_nombre
    )

    nombre_completo = solicitar_obligatorio(
        mensaje=build_name,
        longitud_maxima=60
    )

    if isinstance(nombre_completo, dict):
        return nombre_completo

    # 3. Obtener el régimen desde el JSON
    regimenes = equivalencias["regimen_tag"]

    regimen = regimenes["persona natural"]

    # 4. Obtener los demás datos
    telefono = solicitar(
        response.get("Telefono"),
        longitud_maxima=20
    )

    celular = solicitar(
        response.get("Celular"),
        longitud_maxima=20
    )

    documento_identidad = validar_documento_tercero(
        response.get("Numero_identificacion")
    )

    correo_original = response.get("Email")

    correo = (
        correo_original
        if validar_correo(correo_original)
        else ""
    )

    direccion = solicitar(response.get("Direccion"))

    # 5. Construir el tercero
    nuevo_tercero = {
        "thirdParty": {
            "secondLastName": segundo_apellido,
            "cree": False,
            "firstName": primer_nombre,
            "economicActivity": "",
            "city": ciudad,
            "documentType": {
                "tag": tipo_documento
            },
            "year": year_est,
            "nature": {
                "value": 0
            },
            "firstLastName": primer_apellido,
            "name": nombre_completo,
            "id": documento_identidad,
            "checkDigit": "",
            "regimen": {
                "tag": regimen
            },
            "secondName": segundo_nombre,
            "userCode": 1,
            "telephones": "0000" if telefono == "" else telefono,
            "cellphone": celular,
            "email": correo,
            "address": direccion
        }
    }

    return nuevo_tercero