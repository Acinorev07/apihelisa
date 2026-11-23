from hooks.obtener_archivo_json import cargar_archivo
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