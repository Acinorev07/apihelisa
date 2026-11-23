def validar_tercero_helisa(respuesta, identificacion):

    if respuesta is None:
        return {
            "status": 404,
            "identificacion": identificacion,
            "motivo": "No se recibió respuesta de Helisa."
        }

    if respuesta.status_code == 204:
        return {
            "status": 204,
            "identificacion": identificacion,
            "motivo": "El tercero no existe en Helisa."
        }

    if respuesta.status_code != 200:
        return {
            "status": respuesta.status_code,
            "identificacion": identificacion,
            "respuesta": respuesta.text
        }

    try:
        resultado = respuesta.json()

    except ValueError:
        return {
            "status": 406,
            "identificacion": identificacion,
            "motivo": "Helisa devolvió un JSON inválido."
        }

    tercero = resultado.get("thirdParty") if isinstance(resultado, dict) else None

    if not isinstance(tercero, dict):
        return {
            "status": 406,
            "identificacion": identificacion,
            "motivo": "No se encontró el objeto thirdParty."
        }

    clientes = tercero.get("clients", [])
    proveedores = tercero.get("suppliers", [])

    return {
        "status": 200,
        "identificacion": tercero.get("id", identificacion),
        "nombre": tercero.get("name"),
        "es_cliente": bool(clientes),
        "es_proveedor": bool(proveedores),
        "clientes": clientes,
        "proveedores": proveedores,
        "tercero": tercero
    }