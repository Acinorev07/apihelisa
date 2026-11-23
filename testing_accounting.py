

from hooks.configuracion_APIs import obtener_url
from hooks.obtener_archivo_json import cargar_archivo
from hooks.configuracion_APIs import obtener_url
from api.q10.route import GET
from services.helisa.obtener_tercero import obtener_tercero
from hooks.obtener_estudiante_tercero import obtener_estudiante_tercero
from hooks.validarDi import validar_documento_tercero
import urllib.request, json
from copy import deepcopy
from hooks.crear_archivo_json import crear_archivo_json




def obtener_recibo_pago_factura(id_pago):

    url = obtener_url(
        "q10",
        "detalle_pago_factura"
    )

    print(f"url: {url}")

    

    url_enviar = url.format(id=int(id_pago))

    print(f"url: {url_enviar}")

    response = GET(url_enviar)

    return response.json()


def validar_existencia_recibo_en_factura(facturas):

    print(f"Cantidad de facturas: {len(facturas)}")

    # Facturas que no tienen recibo de pago
    facturas_sin_recibo = []

    # Facturas que si tienen recibo de pago
    facturas_con_recibo = []

    # Errores técnicos o de estructura
    errores_consulta = []

    for factura in facturas:

        numero_factura = factura.get("Numero_factura")

        # Obtener los pagos de la factura
        pagos = factura.get("Pagos")

        # Validar que exista la lista de pagos
        if pagos is None:
            errores_consulta.append({
                "factura": numero_factura,
                "motivo": "La factura no contiene la clave Pagos."
            })
            continue

        # Validar que tenga al menos un pago
        if not pagos:
            facturas_sin_recibo.append(factura)
            continue

        # Revisar los recibos de pago
        tiene_recibo = False

        for pago in pagos:

            if not isinstance(pago, dict):
                errores_consulta.append({
                    "factura": numero_factura,
                    "motivo": "Uno de los pagos tiene una estructura inválida."
                })
                continue

            codigo_recibo = pago.get("Numero_recibo_pago")

            if codigo_recibo is not None and str(codigo_recibo).strip():
                tiene_recibo = True
                facturas_con_recibo.append(factura)
                break

        # Si ninguno de sus pagos tiene número de recibo
        if not tiene_recibo:
            facturas_sin_recibo.append(factura)

    print("\n========== RESULTADOS ==========")

    print(f"Total de facturas: {len(facturas)}")

    print(
        f"Facturas sin recibo: {len(facturas_sin_recibo)}"
    )

    print(
        f"Facturas con recibo: {len(facturas_con_recibo)}"
     )

    print(
        f"Errores de estructura: {len(errores_consulta)}"
    )

    return {
        "facturas_sin_recibo": facturas_sin_recibo,
        "facturas_con_recibo": facturas_con_recibo,
        "errores_consulta": errores_consulta
    }



from copy import deepcopy


def validar_cuenta_factura(facturas):

    contabilidad = cargar_archivo(
        "clasificacion_contable_productos.json"
    )

    productos = contabilidad["productos"]
    cuentas = contabilidad["cuentas_contables"]
    producto_cuenta = contabilidad["producto-cuenta"]
    producto_cuenta_2 = contabilidad["producto-cuenta-2"]

    # Códigos exactos que identifican productos de cartera
    codigos_cartera = [
        "CC",
        "C",
        "CAS",
        "CTAPI",
        "CSO",
        "CAR",
        "PANADERIA 2016"
    ]

    clasificacion = {
        "ingresos": {},
        "pasivos": {},
        "cartera": {},
        "sin_clasificar": {}
    }

    for factura in facturas:

        numero_factura = factura.get("Numero_factura")

        factura_grupos = {
            "ingresos": [],
            "pasivos": [],
            "cartera": [],
            "sin_clasificar": []
        }

        for producto in factura.get("Productos", []):

            codigo_producto = producto.get(
                "Codigo_producto", ""
            )

            codigo_normalizado = codigo_producto.strip().upper()

            # Buscar la cuenta contable
            cuenta = producto_cuenta.get(codigo_producto)

            # Clasificación exacta de cartera
            if codigo_normalizado in codigos_cartera:

                factura_grupos["cartera"].append(producto)

            elif cuenta is None:

                factura_grupos["sin_clasificar"].append(producto)

            elif cuenta.startswith("4160"):

                factura_grupos["ingresos"].append(producto)

            elif cuenta.startswith("2"):

                factura_grupos["pasivos"].append(producto)

            else:

                factura_grupos["sin_clasificar"].append(producto)

        # Guardar las facturas clasificadas
        for grupo, productos_factura in factura_grupos.items():

            if productos_factura:

                factura_clasificada = deepcopy(factura)

                factura_clasificada["Productos"] = productos_factura

                clasificacion[grupo][numero_factura] = (
                    factura_clasificada
                )

    return clasificacion



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



if __name__ == "__main__":

    facturas = cargar_archivo(
        "todas_las_facturas_q10.json"
    )

    errores_consulta = []
    terceros_correctos = []

    identificaciones = set()

    # Obtener identificaciones únicas
    for factura in facturas:

        id_tercero = obtener_estudiante_tercero(
            "Numero_identificacion_estudiante",
            "Numero_identificacion_tercero",
            factura
        )

        identificacion = validar_documento_tercero(id_tercero)

        if identificacion:
            identificaciones.add(identificacion)

    print(f"Identificaciones únicas: {len(identificaciones)}")

    # Consultar cada tercero una sola vez
    fecha = "2026-11-21"

    for identificacion in identificaciones:

        try:
            respuesta_http = obtener_tercero(
                fecha,
                identificacion
            )

            resultado = validar_tercero_helisa(
                respuesta=respuesta_http,
                identificacion=identificacion
            )

        except Exception as error:

            errores_consulta.append({
                "identificacion": identificacion,
                "motivo": str(error)
            })

            continue

        if resultado["status"] != 200:
            errores_consulta.append(resultado)

        else:
            terceros_correctos.append(resultado)

    print("\nRESUMEN DE CONSULTAS")
    print(f"Identificaciones consultadas: {len(identificaciones)}")
    print(f"Terceros correctos: {len(terceros_correctos)}")
    print(f"Errores de consulta: {len(errores_consulta)}")

    crear_archivo_json(
        response=errores_consulta,
        nombre_archivo="Errores consulta.json"
    )

    crear_archivo_json(
        response=terceros_correctos,
        nombre_archivo="Terceros correctos.json"
    )


    # for tercero in terceros_correctos:

    #     print(
    #         f"Identificación: {tercero['identificacion']} | "
    #         f"Nombre: {tercero['nombre']} | "
    #         f"Cliente: {tercero['es_cliente']} | "
    #         f"Proveedor: {tercero['es_proveedor']}"
    #     )
        

        

    
    #     fecha_original = factura.get("Fecha_factura")

    #     numero_factura = factura.get("Numero_factura")

    #     if not fecha_original:
    #         errores_consulta.append({
    #             "factura": numero_factura,
    #             "identificacion": identificacion,
    #             "motivo": "La factura no tiene fecha."
    #         })
    #         continue

    #     fecha = fecha_original.split("T", 1)[0]

    #     try:
    #         respuesta_http = obtener_tercero(
    #             fecha,
    #             identificacion
    #         )

    #         resultado = validar_tercero_helisa(
    #             respuesta=respuesta_http,
    #             identificacion=identificacion
    #         )

    #     except Exception as error:

    #         errores_consulta.append({
    #             "factura": numero_factura,
    #             "identificacion": identificacion,
    #             "motivo": str(error)
    #         })

    #         continue

    #     resultado["factura"] = numero_factura

    # print("Identificaciones únicas:", len(identificaciones))



    
    
    # for tercero in terceros_correctos:

    #     print(
    #         f"Identificación: {tercero['identificacion']} | "
    #         f"Nombre: {tercero['nombre']} | "
    #         f"Cliente: {tercero['es_cliente']} | "
    #         f"Proveedor: {tercero['es_proveedor']}"
    #     )

    # for factura in facturas:

    #     if factura.get("Numero_factura") == "25834":

    #         print(json.dumps(
    #             factura,
    #             indent=4,
    #             ensure_ascii=False
    #         ))
       
    #    contabilidad = cargar_archivo(
    #        "clasificacion_contable_productos.json",
    #    )

    #    print(f"Contabilidad: {contabilidad["producto-cuenta"].get("C")}")

    

    # resultados = validar_existencia_recibo_en_factura(facturas=facturas)

    # facturas_sin_recibo = resultados.get("facturas_sin_recibo")
    # facturas_con_recibo = resultados.get("facturas_con_recibo")

    # print(len(facturas_con_recibo))

    # print(json.dumps(
    #     facturas_con_recibo,
    #     indent=4,
    #     ensure_ascii=False
    # ))

    # resultado = validar_cuenta_factura(facturas_con_recibo)

    # print("Facturas de ingresos:", len(resultado["ingresos"]))
    # print("Facturas de pasivos:", len(resultado["pasivos"]))
    # print("Facturas de cartera:", len(resultado["cartera"]))
    # print("Facturas sin clasificar:", len(resultado["sin_clasificar"]))
    
    # for numero_factura, factura in resultado["pasivos"].items():

    #     for producto in factura["Productos"]:

    #         print(f"Fecha factura: {factura.get("Fecha_factura")} |Nombre cliente: {factura.get("Nombre_completo_estudiante")}| Numero Factura: {factura.get("Numero_factura")} | Codigo producto: {producto.get("Codigo_producto")} | Nombre producto: {producto.get("Nombre_producto")}")



    # id_pago = input("Ingrese el número de recibo de pago: ").strip()
    # respuesta = obtener_recibo_pago_factura(id_pago=id_pago)


    # if respuesta.get("code") != "200":

    #     print(f"Respuesta: {
    #                 json.dumps(
    #                     respuesta,
    #                     indent=4,
    #                     ensure_ascii=False
    #                 )
    #             }")

    # else:

    #     print (f"Error: {
    #                 respuesta.get("message")
    #             }")

        


    