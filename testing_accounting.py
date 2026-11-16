

from hooks.configuracion_APIs import obtener_url
from hooks.obtener_archivo_json import cargar_archivo
from hooks.configuracion_APIs import obtener_url
from api.q10.route import GET
import urllib.request, json
from copy import deepcopy




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




if __name__ == "__main__":

    facturas = cargar_archivo(
            "todas_las_facturas_q10.json"
        )


    
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

    

    resultados = validar_existencia_recibo_en_factura(facturas=facturas)

    facturas_sin_recibo = resultados.get("facturas_sin_recibo")
    facturas_con_recibo = resultados.get("facturas_con_recibo")

    print(len(facturas_con_recibo))

    # print(json.dumps(
    #     facturas_con_recibo,
    #     indent=4,
    #     ensure_ascii=False
    # ))

    resultado = validar_cuenta_factura(facturas_con_recibo)

    print("Facturas de ingresos:", len(resultado["ingresos"]))
    print("Facturas de pasivos:", len(resultado["pasivos"]))
    print("Facturas de cartera:", len(resultado["cartera"]))
    print("Facturas sin clasificar:", len(resultado["sin_clasificar"]))
    
    for numero_factura, factura in resultado["pasivos"].items():

        for producto in factura["Productos"]:

            print(f"Fecha factura: {factura.get("Fecha_factura")} |Nombre cliente: {factura.get("Nombre_completo_estudiante")}| Numero Factura: {factura.get("Numero_factura")} | Codigo producto: {producto.get("Codigo_producto")} | Nombre producto: {producto.get("Nombre_producto")}")



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

        


    