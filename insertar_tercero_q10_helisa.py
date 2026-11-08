
from iu.forms.solicitar_id  import solicitar_id
from hooks.validarDi import validar_documento_tercero
from hooks.validar_correo import validar_correo
from services.q10.obtener_estudiante import obtener_estudiante
from services.q10.obtener_tercero import obtener_tercero
from api.helisa.route import POST
from hooks.obtener_archivo_json import cargar_facturas
from datetime import datetime
from hooks.configuracion_APIs import obtener_url
import json
import string
import unicodedata
import requests
from requests import post

def normalizar_texto(texto):
    texto = str(texto).strip().lower()

    texto = unicodedata.normalize("NFD", texto)

    return "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )


def separar_identificacion(numero):
    if numero is None:
        raise ValueError("La identificación está vacía.")

    partes = str(numero).strip().rsplit("-", 1)

    identificacion = "".join(
        c for c in partes[0] if c.isdigit()
    )

    digito = ""

    if len(partes) == 2:
        digito = "".join(
            c for c in partes[1] if c.isdigit()
        )

    if not identificacion:
        raise ValueError("La identificación no es válida.")

    return identificacion, digito


def obtener_regimen_helisa(responsabilidades, regimen_tag):
    if not isinstance(responsabilidades, list):
        return {
            "ok": False,
            "mensaje": "Las responsabilidades del RUT no tienen un formato válido."
        }

    if not responsabilidades:
        return {
            "ok": False,
            "mensaje": "El tercero no tiene responsabilidades del RUT registradas."
        }

    etiquetas = []

    for responsabilidad in responsabilidades:

        clave = normalizar_texto(responsabilidad)

        codigo = regimen_tag.get(clave)

        if codigo is None:
            return {
                "ok": False,
                "mensaje": f"Responsabilidad no reconocida: {responsabilidad}"
            }

        if codigo not in etiquetas:
            etiquetas.append(codigo)

    if len(etiquetas) > 1:
        return {
            "ok": False,
            "mensaje": (
                "El tercero tiene varias responsabilidades tributarias. "
                "Se necesita definir cuál debe enviarse a Helisa."
            )
        }

    return {
        "ok": True,
        "tag": etiquetas[0]
    }



def dividir_texto(texto, limite):
    if texto is None:
        return []

    texto = str(texto)

    fragmentos = []

    for i in range(0, len(texto),limite):

        fragmento = texto[i:i + limite]
        fragmentos.append(fragmento)

        return fragmentos[0]

    

def solicitar(mensaje, longitud_maxima=None):
    """Solicita un dato y valida su longitud."""

    if mensaje is None:
        return ""

    valor = str(mensaje).strip()

    if valor.lower() in ("null", "none"):
        return ""

    if longitud_maxima is not None and len(valor) > longitud_maxima:
        return dividir_texto(valor, longitud_maxima)

    return valor


def solicitar_obligatorio(mensaje, longitud_maxima):
    """Solicita un dato hasta que el usuario introduzca un valor."""
    if mensaje is None:

        return {
            "status": 422,
            "mensaje": "El campo obligatorio está vacío."
        }

    valor = str(mensaje).strip()

    if not valor or valor.lower() in ("null", "none"):
        return {
            "status": 422,
            "mensaje": "El campo obligatorio está vacío."
        }

    if longitud_maxima is not None and len(valor) > longitud_maxima:
        cortado = dividir_texto(
                texto=valor,
                limite=longitud_maxima
                )
        return cortado
    
    return valor



def construir_nombre(
    primer_apellido,
    segundo_apellido,
    primer_nombre,
    segundo_nombre
):
    partes = [
        primer_apellido,
        segundo_apellido,
        primer_nombre,
        segundo_nombre
    ]

    return " ".join(
        str(parte).strip()
        for parte in partes
        if parte is not None and str(parte).strip()
    )


def insertar_tercero_q10_helisa():
    # Se obtienen todas las facturas.
    facturas = cargar_facturas()

    # Se selecciona una factura del conjunto de datos
    factura = facturas[13]

    # Obtener el tipo de identificación desde Q10.
    equivalencias_documentos = {
        "1": "C",
        "70": "X",
        "2": "T",
        "13": "A"

    }

    regimen_tag = {
        "regimen comun": "C",
        "gran contribuyente": "G",
        "regimen simplificado": "S",
        "entidad oficial": "O",
        "especial": "E",
        "persona natural": "P",
        "profesional independiente": "I"
    }


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

        tipo_identificacion = solicitar(
            response.get("Codigo_tipo_identificacion"),
            2
        )
        
        tipo_documento = equivalencias_documentos.get(
            tipo_identificacion,
            ""
        )

        print(f"Registro estudiante helisa: {json.dumps(
                response,
                indent=4,
                ensure_ascii=False
            )}")

        primer_apellido = solicitar (
            response.get("Primer_apellido")
        )

        segundo_apellido = solicitar(
            response.get("Segundo_apellido")
        )

        primer_nombre = solicitar(
            response.get("Primer_nombre")
        )

        segundo_nombre = solicitar(
            response.get("Segundo_nombre")
        )

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

        if isinstance(nombre_completo,dict):
            return nombre_completo
        
        nombre = nombre_completo

        telefono = solicitar(
            mensaje = response.get("Telefono"),
            longitud_maxima=20
        )

        celular = solicitar(
            mensaje=response.get("Celular"),
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

        direccion = solicitar(
            response.get("Direccion")
        )
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
                    "value": 1
                },
                "firstLastName": primer_apellido,
                "name": nombre,
                "id": documento_identidad,
                "checkDigit": "",
                "regimen": {
                    "tag": "P"
                },
                "secondName": segundo_nombre,
                "userCode": 1,
                "telephones": "0000" if telefono == "" else telefono,
                "cellphone": celular,
                "email": correo,
                "address": direccion,
            }
        }

        return nuevo_tercero

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

        responsabilidades = response.get("Responsabilidades_rut", [])

        resultado_regimen = obtener_regimen_helisa(
            responsabilidades=responsabilidades,
            regimen_tag=regimen_tag
            )

        if not resultado_regimen["ok"]:

            regimen = "S"

        else: 
            # return {
            #     "status": 422,
            #     "mensaje": resultado_regimen["mensaje"]
            # }
             regimen = resultado_regimen["tag"]
        
        tipo_identificacion = response.get("Codigo_tipo_identificacion")
        
        # Validamos el numero de identificacion del tercero
        identificacion, dig_ver = separar_identificacion(
                response.get("Numero_identificacion")
            )

        doc_ident = validar_documento_tercero(
           identificacion
        )

        di = solicitar_obligatorio(
            mensaje=doc_ident,
            longitud_maxima=20
        )

        if isinstance(di,dict):
            return di
        
        doc_id = di


        # Validamos la naturaleza del tercero
        naturaleza = response.get("Tipo")
        natur = solicitar(
            mensaje = naturaleza
        )

        # Validamos el tipo de documento segun el diccionario definido
        tipo_documento = equivalencias_documentos.get(
                    tipo_identificacion,
                    ""
                )

        tipo_doc = solicitar(
            mensaje=tipo_documento,
            longitud_maxima=2
        )

        nombre_completo = solicitar_obligatorio(
            mensaje=nombre_tercero,
            longitud_maxima=60
        )

        if isinstance(nombre_completo,dict):
            return nombre_completo
        
        nombre = nombre_completo

        dv = solicitar(
            mensaje=dig_ver,
            longitud_maxima=2
        )

        telefono = solicitar(
            mensaje=response.get("Telefono"),
            longitud_maxima=20
        )        

        correo_original = response.get("Correo_electronico")

        correo = (
            correo_original
            if validar_correo(correo_original)
            else ""
        )

        direccion = solicitar(
            response.get("Direccion")
        )

        nuevo_tercero = {
                    "thirdParty": {
                        "secondLastName": "",
                        "cree": False,
                        "firstName": "",
                        "economicActivity": "",
                        "city": "",
                        "documentType": {
                            "tag": tipo_doc
                        },
                        "year": year_est,
                        "nature": {
                            "value": 0 if natur == "Jurídica" else 1
                        },
                        "firstLastName": "",
                        "name": nombre,
                        "id": doc_id,
                        "checkDigit": dv,
                        "regimen": {
                            "tag": regimen
                        },
                        "secondName": "",
                        "userCode": 1,
                        "telephones": "0000",
                        "cellphone": "0000" if telefono == "" else telefono,
                        "email": correo,
                        "address": direccion,
                    }
                }

        return nuevo_tercero

    else: 

        error = {
            "mensaje":"No hay Nombre en los capos de estudiante y tercero",
            "status":404
        }

        return error


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


if __name__ == "__main__":

    tercero = insertar_tercero_q10_helisa()   
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

        respuesta = insertar(
            json_data=json_data
            )

        if isinstance(respuesta, dict):

            print(json.dumps(
                respuesta,
                indent=4,
                ensure_ascii=False
            ))

        else:

            print(f"Código HTTP: {respuesta.status_code}")

            try:
                resultado = respuesta.json()

                print(json.dumps(
                    resultado,
                    indent=4,
                    ensure_ascii=False
                ))

            except requests.exceptions.JSONDecodeError:
                print(respuesta.text)

        