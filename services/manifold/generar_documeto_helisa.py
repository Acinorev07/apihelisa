
from datetime import datetime
from calendar import monthrange
import unicodedata
from services.helisa.obtener_dcto_helisa import obtener_dcto_helisa
from services.q10.obtener_recibo_pago_factura import (
    obtener_recibo_pago_factura
)
from services.q10.obtener_tercero import obtener_tercero
from services.q10.obtener_estudiante import obtener_estudiante
from hooks.validarDi import validar_documento_tercero
from hooks.obtener_archivo_json import cargar_archivo
import copy

# ---------------------------------------------------------
# FUNCIONES AUXILIARES
# ---------------------------------------------------------

def convertir_fecha(fecha):
    """Convierte una fecha ISO de Q10 en datetime.date."""
    if not fecha:
        raise ValueError("Se recibió una fecha vacía.")

    return datetime.fromisoformat(
        str(fecha).replace("Z", "+00:00")
    ).date()


def normalizar_texto(texto):
    """Normaliza textos para comparar formas de pago."""
    texto = str(texto or "").strip().casefold()

    return "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caracter) != "Mn"
    )


def obtener_centro_costo(factura, equivalencias):
    """Busca el centro de costo en las observaciones."""

    codigos_centro_costos = [
        "E1", "E2", "E3",
        "F1", "F2", "F3",
        "SO1", "SO2", "SO3",
        "PI1", "PI2", "PI3",
        "AS1", "AS2", "AS3",
        "DONACION",
        "CF1", "CF2",
        "C1", "C2"
    ]

    observaciones = factura.get("Observaciones") or ""

    partes = [
        parte.strip().upper()
        for parte in observaciones.split("/")
    ]

    codigo_encontrado = next(
        (
            codigo
            for codigo in codigos_centro_costos
            if codigo in partes
        ),
        None
    )

    if codigo_encontrado is None:
        return "062001", ""

    centro = equivalencias.get(codigo_encontrado)

    if not centro:
        raise ValueError(
            f"No existe equivalencia de centro de costos "
            f"para {codigo_encontrado}."
        )

    return centro, codigo_encontrado


def obtener_datos_tercero(factura):
    """Obtiene nombre e identificación del estudiante o tercero."""

    nombre_estudiante = factura.get(
        "Nombre_completo_estudiante"
    )

    nombre_tercero = factura.get(
        "Nombre_completo_tercero"
    )

    if nombre_estudiante:
        estudiante = obtener_estudiante(
            codigo_estudiante=factura.get("Codigo_estudiante"),
            codigo_programa=""
        )

        if not isinstance(estudiante, dict):
            raise ValueError(
                "No se pudo consultar el estudiante en Q10."
            )

        identificacion = (
            estudiante.get("Numero_identificacion")
            or estudiante.get("Numero_identificacion_estudiante")
            or factura.get("Numero_identificacion_estudiante")
        )

        nombre = (
            estudiante.get("Nombre_completo")
            or nombre_estudiante
        )

    elif nombre_tercero:
        tercero = obtener_tercero(
            factura.get("Consecutivo_tercero")
        )

        if not isinstance(tercero, dict):
            raise ValueError(
                "No se pudo consultar el tercero en Q10."
            )

        identificacion = (
            tercero.get("Numero_identificacion")
            or factura.get("Numero_identificacion_tercero")
        )

        nombre = (
            tercero.get("Nombre_completo")
            or nombre_tercero
        )

    else:
        raise ValueError(
            "La factura no tiene estudiante ni tercero identificado."
        )

    if not identificacion:
        raise ValueError(
            "El tercero no tiene número de identificación."
        )

    doc_id = validar_documento_tercero(identificacion)

    if not doc_id:
        raise ValueError(
            "No fue posible validar la identificación del tercero."
        )

    return nombre, doc_id


# ---------------------------------------------------------
# OBTENER DÉBITOS DE LOS RECIBOS DE CAJA
# ---------------------------------------------------------

def obtener_movimientos_debito(
    factura,
    concepto,
    doc_id
):
    movimientos = []
    
    accounting_class = 0

    fecha_factura = convertir_fecha(
        factura.get("Fecha_factura")
    )

    observaciones = (
        factura.get("Observaciones") or ""
    ).upper()

    # Conservamos tu identificación actual del banco.
    cuenta_consignacion = (
        "11201002"
        if "BCS" in observaciones
        else "11201001"
    )

    pagos = factura.get("Pagos") or []

    for pago in pagos:

        if not isinstance(pago, dict):
            continue

        # Ignorar pagos anulados y cualquier estado distinto de Pagado.
        if pago.get("Estado_pago") != "Pagado":
            continue

        fecha_pago = pago.get("Fecha_pago")

        if not fecha_pago:
            continue

        # Si el recibo de pago tiene fecha distinta a la factura, no lo toma
        if convertir_fecha(fecha_pago) != fecha_factura:
            continue

        codigo_recibo = pago.get("Numero_recibo_pago")

        if not codigo_recibo:
            continue

        recibo = obtener_recibo_pago_factura(
            codigo_recibo
        )

        if not isinstance(recibo, dict):
            raise ValueError(
                f"No se pudo consultar el recibo {codigo_recibo}."
            )

        if recibo.get("Estado_pago") != "Pagado":
            continue

        fecha_recibo = recibo.get("Fecha_pago")

        if not fecha_recibo:
            continue

        if convertir_fecha(fecha_recibo) != fecha_factura:
            continue

        # Confirmar que el recibo corresponde a esta factura.
        detalles = recibo.get("Detalles") or []

        detalle_factura = next(
            (
                detalle
                for detalle in detalles
                if str(detalle.get("Numero_factura"))
                == str(factura.get("Numero_factura"))
            ),
            None
        )

        if detalle_factura is None:
            continue

        formas_pago = recibo.get("Formas_pago") or []

        for forma_pago in formas_pago:

            nombre_forma = normalizar_texto(
                forma_pago.get("Nombre_forma_pago")
            )

            valor = float(
                forma_pago.get("Valor") or 0
            )

            # Si el valor del recibo de pago es negativo, no lo toma
            if valor <= 0:
                continue

            if nombre_forma == "efectivo":
                cuenta_debito = "110505"

                # Si la forma de pago es en Efectivo, agrega este asiento a los movimientos
                movimientos.append({
                    "nature": {
                        "tag": "D"
                    },
                    "costCenter": "",
                    "concept": concepto,
                    "accountingClass": {
                        "value": accounting_class
                    },
                    "value": round(valor, 2),
                    "idThirdParty": doc_id,
                    "account": cuenta_debito,
                    "userCode": 1,
                    "taxBase": 0
                })





            elif nombre_forma == "consignacion":
                cuenta_debito = cuenta_consignacion


                # Si la cuenta de pago es Bancaria, se agrega este asiento a los movimientos
                movimientos.append(
                {
                    "accountingClass": {
                            "value": accounting_class
                        },
                    "nature": {
                    "tag": "D"
                    },
                    "concept": concepto,
                    "value": round(valor, 2),
                    "idThirdParty": doc_id,
                    "account": cuenta_debito,
                    "userCode": 1,
                    "taxBase": 0,
                    "bankAccount": "02-036-533244",
                    "bankCheckDate": {
                    "day": fecha_factura.day,
                    "month": fecha_factura.month,
                    "year": fecha_factura.year
                    }
                }
            )


            elif nombre_forma.strip() == "tarjeta debito":
                # Si la cuenta de pago es Bancaria, se agrega este asiento a los movimientos
                movimientos.append(
                {
                    "accountingClass": {
                            "value": accounting_class
                        },
                    "nature": {
                    "tag": "D"
                    },
                    "concept": concepto,
                    "value": round(valor, 2),
                    "idThirdParty": doc_id,
                    "account": "11201002",
                    "userCode": 1,
                    "taxBase": 0,
                    "bankAccount": "02-036-533244",
                    "bankCheckDate": {
                    "day": fecha_factura.day,
                    "month": fecha_factura.month,
                    "year": fecha_factura.year
                    }
                }
            )              



            else:
                raise ValueError(
                    f"Forma de pago no configurada: "
                    f"{forma_pago.get('Nombre_forma_pago')}"
                )
    

    return movimientos


# ---------------------------------------------------------
# GENERAR PARTIDA DOBLE
# ---------------------------------------------------------

def generar_partida_doble(facturas):

    contabilidad = cargar_archivo(
        "clasificacion_contable_productos.json"
    )
    accounting_class = 0

    producto_cuenta = contabilidad["producto-cuenta"]

    equivalencias_centro = contabilidad["centro_costos"]

    transactions = []
    errores = []

    for factura in facturas:

        numero_factura = factura.get("Numero_factura")

        try:

            # 1. Obtener tercero.
            nombre, doc_id = obtener_datos_tercero(
                factura
            )

            # 2. Obtener centro de costo.
            centro_costo, codigo_cc = obtener_centro_costo(
                factura,
                equivalencias_centro
            )

            # 3. Construir concepto.
            concepto = (
                f"{nombre}-{numero_factura}-{codigo_cc}"
            )

            # 4. Obtener débitos de los pagos válidos.
            movimientos_debito = obtener_movimientos_debito(
                factura=factura,
                concepto=concepto,
                doc_id=doc_id
            )

            if not movimientos_debito:
                errores.append({
                    "factura": numero_factura,
                    "motivo": (
                        "No tiene recibos pagados y válidos "
                        "en la fecha de la factura."
                    )
                })
                continue

            total_pagado = round(
                sum(
                    movimiento["value"]
                    for movimiento in movimientos_debito
                ),
                2
            )

            productos = factura.get("Productos") or []

            if not productos:
                errores.append({
                    "factura": numero_factura,
                    "motivo": "La factura no contiene productos."
                })
                continue

            # 5. Preparar valores de productos.
            datos_productos = []

            for producto in productos:

                codigo_producto = producto.get(
                    "Codigo_producto"
                )

                cuenta_credito = producto_cuenta.get(
                    codigo_producto
                )

                if not cuenta_credito:
                    raise ValueError(
                        f"No existe cuenta contable para "
                        f"el producto {codigo_producto}."
                    )

                cantidad = float(
                    producto.get("Cantidad") or 1
                )

                valor_unidad = float(
                    producto.get("Valor_unidad") or 0
                )

                valor_bruto = round(
                    valor_unidad * cantidad,
                    2
                )

                descuento = float(
                    producto.get("Valor_descuento") or 0
                )

                valor_neto = producto.get("Valor_a_pagar")

                if valor_neto is None:
                    valor_neto = valor_bruto - descuento
                else:
                    valor_neto = float(valor_neto)

                if valor_neto < 0 or descuento < 0:
                    raise ValueError(
                        f"Valores inválidos en producto "
                        f"{codigo_producto}."
                    )

                # ÚNICA INCORPORACIÓN:
                # Para CGCR se obtiene también el valor del impuesto.
                valor_impuesto = float(
                    producto.get("Valor_impuesto") or 0
                )

                datos_productos.append({
                    "codigo": codigo_producto,
                    "cuenta": cuenta_credito,
                    "bruto": valor_bruto,
                    "descuento": descuento,
                    "neto": valor_neto,
                    "impuesto": valor_impuesto
                })

            total_neto_factura = round(
                sum(
                    producto["neto"]
                    for producto in datos_productos
                ),
                2
            )

            if total_neto_factura <= 0:
                raise ValueError(
                    "El valor neto de los productos es cero."
                )

            if total_pagado > total_neto_factura + 0.01:
                raise ValueError(
                    f"Los pagos del día ({total_pagado}) "
                    f"superan el valor neto de la factura "
                    f"({total_neto_factura})."
                )

            # 6. Agregar los débitos de los recibos.
            transactions.extend(
                movimientos_debito
            )

            # 7. Distribuir los valores pagados entre productos.
            proporcion = (
                total_pagado / total_neto_factura
            )

            for producto in datos_productos:

                codigo_producto = producto["codigo"]

                # -------------------------------------------------
                # CONTABILIZACIÓN ESPECIAL PARA CGCR
                # -------------------------------------------------
                if codigo_producto == "CGCR":

                    # Valor del servicio: Valor_unidad * Cantidad.
                    valor_servicio = round(
                        producto["bruto"],
                        2
                    )

                    # Valor del impuesto informado por Q10.
                    valor_impuesto = round(
                        producto["impuesto"],
                        2
                    )

                    # Distribuir proporcionalmente si el pago es parcial.
                    valor_servicio_contabilizado = round(
                        valor_servicio * proporcion,
                        2
                    )

                    valor_impuesto_contabilizado = round(
                        valor_impuesto * proporcion,
                        2
                    )

                    # Crédito de la comisión de garantía de crédito.
                    if valor_servicio_contabilizado > 0:

                        transactions.append({
                            "nature": {
                                "tag": "C"
                            },
                            "costCenter": centro_costo,
                            "concept": concepto,
                            "accountingClass": {
                                "value": accounting_class
                            },
                            "value": valor_servicio_contabilizado,
                            "idThirdParty": doc_id,
                            "account": "28150701",
                            "userCode": 1,
                            "taxBase": 0
                        })

                    # Crédito del impuesto de la comisión.
                    if valor_impuesto_contabilizado > 0:

                        transactions.append({
                            "nature": {
                                "tag": "C"
                            },
                            "costCenter": centro_costo,
                            "concept": concepto,
                            "accountingClass": {
                                "value": accounting_class
                            },
                            "value": valor_impuesto_contabilizado,
                            "idThirdParty": doc_id,
                            "account": "28150702",
                            "userCode": 1,
                            "taxBase": 0
                        })

                    # CGCR ya fue contabilizado en sus dos cuentas.
                    continue

                # -------------------------------------------------
                # CONTABILIZACIÓN ORIGINAL PARA LOS DEMÁS PRODUCTOS
                # -------------------------------------------------

                valor_neto_contabilizado = round(
                    producto["neto"] * proporcion,
                    2
                )

                descuento_contabilizado = round(
                    producto["descuento"] * proporcion,
                    2
                )

                valor_credito = round(
                    valor_neto_contabilizado
                    + descuento_contabilizado,
                    2
                )

                # Débito del descuento, si existe.
                if descuento_contabilizado > 0:

                    transactions.append({
                        "nature": {
                            "tag": "D"
                        },
                        "costCenter": centro_costo,
                        "concept": concepto,
                        "accountingClass": {
                            "value": accounting_class
                        },
                        "value": descuento_contabilizado,
                        "idThirdParty": doc_id,
                        "account": "41750103",
                        "userCode": 1,
                        "taxBase": 0
                    })

                # Crédito de la cuenta original del producto.
                if valor_credito > 0:

                    transactions.append({
                        "nature": {
                            "tag": "C"
                        },
                        "costCenter": centro_costo,
                        "concept": concepto,
                        "accountingClass": {
                            "value": accounting_class
                        },
                        "value": valor_credito,
                        "idThirdParty": doc_id,
                        "account": producto["cuenta"],
                        "userCode": 1,
                        "taxBase": 0
                    })

        except Exception as error:

            errores.append({
                "factura": numero_factura,
                "motivo": str(error)
            })

    # 8. Validar que los movimientos estén cuadrados.
    total_debitos = round(
        sum(
            movimiento["value"]
            for movimiento in transactions
            if movimiento["nature"]["tag"] == "D"
        ),
        2
    )

    total_creditos = round(
        sum(
            movimiento["value"]
            for movimiento in transactions
            if movimiento["nature"]["tag"] == "C"
        ),
        2
    )

    return {
        "transactions": transactions,
        "errores": errores,
        "total_debitos": total_debitos,
        "total_creditos": total_creditos,
        "cuadra": abs(total_debitos - total_creditos) <= 0.01
    }


# ---------------------------------------------------------
# GENERAR DOCUMENTO HELISA
# ---------------------------------------------------------

def generar_documento_helisa(facturas):

    if not facturas:
        raise ValueError(
            "No hay facturas para contabilizar."
        )

    # 1. Validar que todas las facturas tengan la misma fecha.
    fechas = {
        convertir_fecha(factura.get("Fecha_factura"))
        for factura in facturas
    }

    if len(fechas) != 1:
        raise ValueError(
            "Las facturas no tienen una única fecha."
        )

    fecha_documento = fechas.pop()

    # 2. Consultar consecutivos del mes de contabilización.
    fecha_inicial = fecha_documento.replace(day=1)

    ultimo_dia = monthrange(
        fecha_documento.year,
        fecha_documento.month
    )[1]

    fecha_final = fecha_documento.replace(
        day=ultimo_dia
    )

    tipo_documento = "NIED"
    accounting_type = 0

    historial = obtener_dcto_helisa(
        fecha_inicial=fecha_inicial.isoformat(),
        fecha_final=fecha_final.isoformat(),
        document_type=tipo_documento,
        accounting_type=accounting_type
    )

    if not isinstance(historial, dict):
        raise ValueError(
            "No fue posible consultar los documentos de Helisa."
        )

    documentos = historial.get("documents") or []

    if not documentos:
        raise ValueError(
            "No se encontraron documentos para consultar "
            "el siguiente consecutivo."
        )

    numeros = []

    for registro in documentos:

        numero = (
            registro.get("document", {}).get("number")
        )

        if numero is not None:
            numeros.append(str(numero))

    if not numeros:
        raise ValueError(
            "Helisa no devolvió números de documentos."
        )

    ultimo_documento = max(
        numeros,
        key=lambda numero: int(numero)
    )

    siguiente_documento = str(
        int(ultimo_documento) + 1
    ).zfill(8)

    # 3. Generar todos los movimientos.
    resultado = generar_partida_doble(
        facturas
    )

    if resultado["errores"]:
        raise ValueError(
            "Hay facturas que no pudieron contabilizarse: "
            f"{resultado['errores']}"
        )

    if not resultado["transactions"]:
        raise ValueError(
            "No se generaron movimientos contables."
        )

    # 4. Validar partida doble.
    if not resultado["cuadra"]:
        raise ValueError(
            "El documento no está cuadrado. "
            f"Débitos: {resultado['total_debitos']}; "
            f"Créditos: {resultado['total_creditos']}."
        )

    # 5. Duplicar movimientos para Local y NIIF.

    transactions_local = []
    transactions_niif = []

    for movimiento in resultado["transactions"]:

        # Copia para contabilidad Local.
        movimiento_local = copy.deepcopy(movimiento)
        movimiento_local["accountingClass"] = {"value": "0"}
        transactions_local.append(movimiento_local)

        # Copia para contabilidad NIIF.
        movimiento_niif = copy.deepcopy(movimiento)
        movimiento_niif["accountingClass"] = {"value": "1"}
        transactions_niif.append(movimiento_niif)

    # Primero Local y después NIIF.
    transactions_finales = transactions_local + transactions_niif

    documento = {
        "document": {
            "date": {
                "day": fecha_documento.day,
                "month": fecha_documento.month,
                "year": fecha_documento.year
            },
            "document": {
                "type": tipo_documento,
                "number": siguiente_documento
            },
            "transactions": transactions_finales
        }
    }

    print("\nDocumento construido correctamente.")
    print("Consecutivo:", siguiente_documento)
    print("Fecha:", fecha_documento)
    print("Facturas procesadas:", len(facturas))
    print("Movimientos:", len(transactions_finales))
    print("Movimientos Local:", len(transactions_local))
    print("Movimientos NIIF:", len(transactions_niif))
    print("Total débitos:", resultado["total_debitos"])
    print("Total créditos:", resultado["total_creditos"])

    return documento
