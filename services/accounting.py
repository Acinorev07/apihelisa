
# Aplica las reglas contables

from decimal import Decimal, InvalidOperation


def validar_asiento(movimientos):
    """
    Comprueba que un asiento tenga movimientos válidos
    y que sus débitos sean iguales a sus créditos.

    Cada movimiento debe tener:
    - cuenta
    - naturaleza: D o C
    - valor
    """

    if not movimientos:
        return {
            "valido": False,
            "mensaje": "El asiento no contiene movimientos."
        }

    total_debitos = Decimal("0")
    total_creditos = Decimal("0")

    for indice, movimiento in enumerate(movimientos, start=1):
        cuenta = movimiento.get("cuenta")
        naturaleza = movimiento.get("naturaleza")
        valor_original = movimiento.get("valor")

        if not cuenta:
            return {
                "valido": False,
                "mensaje": f"Movimiento {indice}: falta la cuenta."
            }

        if naturaleza not in ("D", "C"):
            return {
                "valido": False,
                "mensaje": (
                    f"Movimiento {indice}: "
                    "la naturaleza debe ser D o C."
                )
            }

        try:
            valor = Decimal(str(valor_original))
        except (InvalidOperation, ValueError, TypeError):
            return {
                "valido": False,
                "mensaje": f"Movimiento {indice}: valor inválido."
            }

        if not valor.is_finite() or valor <= 0:
            return {
                "valido": False,
                "mensaje": (
                    f"Movimiento {indice}: "
                    "el valor debe ser positivo y finito."
                )
            }

        if naturaleza == "D":
            total_debitos += valor
        else:
            total_creditos += valor

    diferencia = total_debitos - total_creditos

    return {
        "valido": diferencia == Decimal("0"),
        "total_debitos": total_debitos,
        "total_creditos": total_creditos,
        "diferencia": diferencia,
        "mensaje": (
            "Asiento cuadrado."
            if diferencia == Decimal("0")
            else "El asiento no cumple la partida doble."
        )
    }



def generar_movimientos_auxiliares(valor):
    """Genera los dos movimientos de la cuenta 28150609."""

    valor = Decimal(str(valor))

    if not valor.is_finite() or valor <= 0:
        raise ValueError("El valor debe ser positivo y finito.")

    return [
        {
            "cuenta": "28150609",
            "naturaleza": "C",
            "valor": valor,
        },
        {
            "cuenta": "28150609",
            "naturaleza": "D",
            "valor": valor,
        },
    ]





def calcular_saldo_pendiente(
    valor_factura,
    descuento=0,
    abonos_capital=0
):
    """
    Calcula el saldo pendiente de una factura.

    saldo = factura - descuento - abonos al capital
    """

    try:
        factura = Decimal(str(valor_factura))
        descuento = Decimal(str(descuento))
        abonos = Decimal(str(abonos_capital))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("La factura, el descuento y los abonos deben ser numéricos.")

    valores = (factura, descuento, abonos)

    if not all(valor.is_finite() for valor in valores):
        raise ValueError("Los valores deben ser finitos.")

    if factura <= 0:
        raise ValueError("El valor de la factura debe ser positivo.")

    if descuento < 0 or abonos < 0:
        raise ValueError("El descuento y los abonos no pueden ser negativos.")

    if descuento > factura:
        raise ValueError("El descuento no puede superar la factura.")

    saldo = factura - descuento - abonos

    if saldo < 0:
        raise ValueError(
            "Los descuentos y abonos superan el valor neto de la factura."
        )

    return saldo



def generar_asiento_factura(factura):
    """
    Genera y valida los movimientos contables de una factura.

    Estructura esperada:
    {
        "numero": "00003413",
        "valor": "2797000",
        "descuento": "200000",
        "cuenta_cartera": "13050537",
        "pagos": [
            {
                "recibo": "RC001",
                "cuenta": "11201001",
                "valor": "597000"
            }
        ]
    }

    No envía información a Helisa.
    """

    try:
        valor_factura = Decimal(str(factura["valor"]))
        descuento = Decimal(str(factura.get("descuento", 0)))

        if (
            not valor_factura.is_finite()
            or not descuento.is_finite()
        ):
            raise ValueError("Los valores deben ser finitos.")

        if valor_factura <= 0:
            raise ValueError("La factura debe tener un valor positivo.")

        if descuento < 0 or descuento > valor_factura:
            raise ValueError(
                "El descuento debe estar entre cero y el valor de la factura."
            )

        cuenta_cartera = factura.get("cuenta_cartera")

        if not isinstance(cuenta_cartera, str) or not (
            cuenta_cartera.startswith("1305053")
        ):
            raise ValueError(
                "La cuenta de cartera debe comenzar por 1305053."
            )

        pagos = factura.get("pagos", [])

        if not isinstance(pagos, list):
            raise ValueError("Los pagos deben estar en una lista.")

        movimientos = []

        # 1. Crédito por el valor bruto de la factura.
        movimientos.append({
            "cuenta": "27054701",
            "naturaleza": "C",
            "valor": valor_factura,
        })

        # 2. Débito por el descuento, si existe.
        if descuento > 0:
            movimientos.append({
                "cuenta": "27054701",
                "naturaleza": "D",
                "valor": descuento,
            })

        # 3. Registrar cada recibo según su cuenta de pago.
        total_abonos = Decimal("0")

        for indice, pago in enumerate(pagos, start=1):
            if not isinstance(pago, dict):
                raise ValueError(
                    f"El pago {indice} no tiene un formato válido."
                )

            cuenta_pago = pago.get("cuenta")

            if cuenta_pago not in ("110505", "11201001"):
                raise ValueError(
                    f"Pago {indice}: cuenta de pago no reconocida."
                )

            valor_pago = Decimal(str(pago["valor"]))

            if not valor_pago.is_finite() or valor_pago <= 0:
                raise ValueError(
                    f"Pago {indice}: el valor debe ser positivo y finito."
                )

            movimientos.append({
                "cuenta": cuenta_pago,
                "naturaleza": "D",
                "valor": valor_pago,
            })

            total_abonos += valor_pago

        # 4. Calcular el saldo neto pendiente.
        saldo_pendiente = calcular_saldo_pendiente(
            valor_factura=valor_factura,
            descuento=descuento,
            abonos_capital=total_abonos,
        )

        # 5. Registrar cartera y movimientos auxiliares
        #    únicamente cuando quede un saldo pendiente.
        if saldo_pendiente > 0:
            movimientos.append({
                "cuenta": cuenta_cartera,
                "naturaleza": "D",
                "valor": saldo_pendiente,
            })

            movimientos.extend(
                generar_movimientos_auxiliares(saldo_pendiente)
            )

        # 6. Validar el asiento completo.
        validacion = validar_asiento(movimientos)

        return {
            "factura": factura.get("numero"),
            "valor_factura": valor_factura,
            "descuento": descuento,
            "total_abonos": total_abonos,
            "saldo_pendiente": saldo_pendiente,
            "movimientos": movimientos,
            "validacion": validacion,
        }

    except (KeyError, InvalidOperation, TypeError, ValueError) as error:
        return {
            "valido": False,
            "mensaje": str(error),
        }


def convertir_a_movimientos_helisa(asiento, factura):
    """
    Convierte los movimientos internos al formato de transacciones
    utilizado por el documento contable de Helisa.
    """
    if not asiento.get("movimientos"):
        raise ValueError("El asiento no contiene movimientos.")

    nit = factura.get("nit")
    centro_costo = factura.get("centro_costo")
    usuario = factura.get("usuario")

    if not nit:
        raise ValueError("Falta el NIT de la factura.")

    if not centro_costo:
        raise ValueError("Falta el centro de costos.")

    if usuario is None:
        raise ValueError("Falta el código de usuario.")

    transacciones = []

    for movimiento in asiento["movimientos"]:
        transaccion = {
            "nature": {
                "tag": movimiento["naturaleza"]
            },
            "account": movimiento["cuenta"],
            "value": int(movimiento["valor"]),
            "idThirdParty": str(nit),
            "costCenter": str(centro_costo),
            "userCode": usuario,
            "accountingClass": {
                "value": 0
            },
            "concept": f"Factura {factura.get('numero', '')}",
            "taxBase": 0
        }

        transacciones.append(transaccion)

    return transacciones




from datetime import date


def construir_documento_helisa(
    asiento,
    factura,
    fecha,
    tipo_documento
):
    """
    Construye el documento contable de Helisa.
    No realiza ninguna petición a la API.

    fecha: objeto datetime.date
    tipo_documento: código de documento configurado en Helisa
    """

    if not isinstance(asiento, dict):
        raise ValueError("El asiento debe ser un diccionario.")

    if not asiento.get("validacion", {}).get("valido", False):
        raise ValueError(
            "No se puede construir el documento: "
            "el asiento no está validado."
        )

    if not isinstance(fecha, date):
        raise ValueError(
            "La fecha debe ser un objeto datetime.date."
        )

    if not isinstance(tipo_documento, str) or not tipo_documento.strip():
        raise ValueError("Falta el tipo de documento de Helisa.")

    numero = factura.get("numero")
    if not numero:
        raise ValueError("Falta el número de la factura.")

    # Convertir los movimientos internos al formato de Helisa.
    transacciones = convertir_a_movimientos_helisa(
        asiento,
        factura
    )

    if not transacciones:
        raise ValueError("El documento no tiene transacciones.")

    # Helisa recibe los datos de fecha, comprobante y transacciones.
    documento = {
        "document": {
            "date": {
                "day": f"{fecha.day:02d}",
                "month": f"{fecha.month:02d}",
                "year": str(fecha.year)
            },
            "document": {
                "type": tipo_documento.strip(),
                "number": str(numero)
            },
            "transactions": [
                {
                    **transaccion,
                    "value": str(transaccion["value"])
                }
                for transaccion in transacciones
            ]
        }
    }

    return documento
