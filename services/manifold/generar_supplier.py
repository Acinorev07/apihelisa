
from hooks.build_supplier_q10_helisa import build_supplier_q10_helisa

def generar_supplier_q10_helisa(facturas):
    """
    Construye los terceros y los agrupa por identificación.
    Todavía no realiza inserciones en Helisa.
    """

    resultado = {
        "suppliers": {},
        "errores": []
    }

    for indice, factura in enumerate(facturas, start=1):

        try:
            supplier = build_supplier_q10_helisa(
                factura=factura
            )

            if (
                not isinstance(supplier, dict)
                or "supplier" not in supplier
            ):
                resultado["errores"].append({
                    "factura_indice": indice,
                    "numero_factura": factura.get("Numero_factura"),
                    "error": supplier
                })
                continue

            datos_supplier = supplier["supplier"]

            identificacion = str(
                datos_supplier.get("id") or ""
            ).strip()

            digito = str(
                datos_supplier.get("checkDigit") or ""
            ).strip()

            if not identificacion:
                resultado["errores"].append({
                    "factura_indice": indice,
                    "numero_factura": factura.get("Numero_factura"),
                    "error": "El tercero no tiene identificación."
                })
                continue

            clave = (
                f"{identificacion}-{digito}"
                if digito
                else identificacion
            )

            numero_factura = factura.get("Numero_factura")

            if clave in resultado["suppliers"]:

                resultado["suppliers"][clave]["facturas"].append(
                    numero_factura
                )

            else:

                resultado["suppliers"][clave] = {
                    "supplier": datos_supplier,
                    "facturas": [numero_factura]
                }

        except Exception as e:

            resultado["errores"].append({
                "factura_indice": indice,
                "numero_factura": factura.get("Numero_factura"),
                "error": str(e)
            })

    return resultado