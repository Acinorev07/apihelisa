from services.q10.obtener_facturas import obtener_facturas
from services.helisa.obtener_tercero import obtener_tercero
from hooks.validarDi import validar_documento_tercero
from hooks.obtener_estudiante_tercero import obtener_estudiante_tercero


def validar_terceros():

    params = {
            "fecha_inicio" : "2026-10-29",
            "fecha_fin" : "2026-10-29",
            "codigo_persona" : "",
            "consecutivo_tercero" : "",
            "codigo_producto" : "",
            "estado" : "2",
            "limite" : 100,
            "offset" : 0
        }


    datos = obtener_facturas(params=params)

    if datos is None:
        print("No fue posible obtener las facturas de Q10.")
        return {}

    # Diccionario de terceros que no están registrados en Helisa.
    terceros_nuevos = {}

    # Errores técnicos que requieren revisión.
    errores_consulta = []

    # Agrupar las facturas por identificación normalizada.
    terceros_q10 = {}

    for factura in datos:
        id = obtener_estudiante_tercero(
            "Numero_identificacion_estudiante",
            "Numero_identificacion_tercero",
            factura
            )

        identificacion = validar_documento_tercero(id)

        if identificacion is None:
            continue

        fecha_original = factura.get("Fecha_factura")

        if not fecha_original:
            errores_consulta.append({
                "factura": factura.get("Numero_factura"),
                "motivo": "La factura no tiene fecha.",
            })
            continue

        fecha = fecha_original.split("T", 1)[0]

        if identificacion not in terceros_q10:
            terceros_q10[identificacion] = {
                "identificacion": identificacion,
                "fecha_consulta": fecha,
                "facturas": [],
            }

        # Guardamos la factura original completa.
        terceros_q10[identificacion]["facturas"].append(factura)

    print("Identificaciones únicas:", len(terceros_q10))

    # Consultar cada identificación una sola vez.
    for identificacion, informacion in terceros_q10.items():

        respuesta = obtener_tercero(
            informacion["fecha_consulta"],
            identificacion,
        )

        if respuesta is None:
            errores_consulta.append({
                "identificacion": identificacion,
                "motivo": "No se recibió respuesta de Helisa.",
            })
            continue

        if respuesta.status_code == 204:
            # Guardar el tercero y todas sus facturas.
            terceros_nuevos[identificacion] = informacion

            print(
                f"Tercero no encontrado: {identificacion} "
                f"| Facturas: {len(informacion['facturas'])}"
            )
            continue

        if respuesta.status_code != 200:
            errores_consulta.append({
                "identificacion": identificacion,
                "codigo_http": respuesta.status_code,
                "respuesta": respuesta.text,
            })
            continue

        try:
            resultado = respuesta.json()
        except ValueError:
            errores_consulta.append({
                "identificacion": identificacion,
                "motivo": "Helisa devolvió un JSON inválido.",
            })
            continue

        tercero = (
            resultado.get("thirdParty")
            if isinstance(resultado, dict)
            else None
        )

        if not isinstance(tercero, dict):
            errores_consulta.append({
                "identificacion": identificacion,
                "motivo": "No se encontró el objeto thirdParty.",
            })
            continue

        id_helisa = tercero.get("id")

        if id_helisa is None:
            errores_consulta.append({
                "identificacion": identificacion,
                "motivo": "La respuesta no contiene la identificación.",
            })
            continue

        try:
            id_helisa = validar_documento_tercero(str(id_helisa))
        except ValueError:
            errores_consulta.append({
                "identificacion": identificacion,
                "motivo": "La identificación devuelta por Helisa no es válida.",
            })
            continue

        if id_helisa == identificacion:
            print(f"Tercero encontrado: {identificacion}")
        else:
            errores_consulta.append({
                "identificacion": identificacion,
                "motivo": (
                    "La identificación devuelta por Helisa "
                    "no coincide con la consultada."
                ),
            })

    print("\n========== RESUMEN ==========")
    print("Terceros nuevos:", len(terceros_nuevos))
    print("Errores de consulta:", len(errores_consulta))

    return terceros_nuevos


