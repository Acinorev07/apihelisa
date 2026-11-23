
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