
from hooks.obtener_regimen_helisa import obtener_regimen_helisa
from hooks.obtener_archivo_json import cargar_archivo
from hooks.separar_identificacion import separar_identificacion
from hooks.validarDi import validar_documento_tercero
from hooks.solicitar_obligatorio import solicitar_obligatorio
from hooks.solicitar import solicitar
from hooks.validar_correo import validar_correo


def build_thirdParty(
          response,
          year_est
            ):


    equivalencias = cargar_archivo(
         "validaciones_tercero_helisa.json"
    )

    regimen_tag = equivalencias["regimen_tag"]
    equivalencias_documentos = equivalencias["equivalencias_documentos"]

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

    if natur == "Jurídica":
        naturaleza_helisa = 0
    elif natur == "Natural":
        naturaleza_helisa = 1
    else:
        return {
            "status": 422,
            "mensaje": f"Naturaleza del tercero no reconocida: {naturaleza}"
        }

    tipo_documento = equivalencias_documentos.get(
        str(tipo_identificacion)
    )

    if not tipo_documento:
         tipo_doc = solicitar(
                 mensaje="A",
                 longitud_maxima=2
             )


    tipo_doc = solicitar(
        mensaje=tipo_documento,
        longitud_maxima=2
    )

    nombre_tercero = response.get("Nombre_completo")

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
                        "value": naturaleza_helisa
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