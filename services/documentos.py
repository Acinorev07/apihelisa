# Construye y valida la NIED


def crear_documento(
    dia,
    mes,
    anio,
    tipo,
    numero,
    nit,
    cuenta_debito,
    cuenta_credito,
    valor
):
    documento = {
        "document": {
            "date": {
                "day": dia,
                "month": mes,
                "year": anio
            },
            "document": {
                "type": tipo,
                "number": numero
            },
            "transactions": [
                {
                    "nature": {"tag": "D"},
                    "costCenter": "061002",
                    "concept": "Prueba API Helisa",
                    "accountingClass": {"value": 0},
                    "value": valor,
                    "idThirdParty": nit,
                    "account": cuenta_debito,
                    "userCode": 1,
                    "taxBase": 0
                },
                {
                    "nature": {"tag": "C"},
                    "costCenter": "061002",
                    "concept": "Prueba API Helisa",
                    "accountingClass": {"value": 0},
                    "value": valor,
                    "idThirdParty": nit,
                    "account": cuenta_credito,
                    "userCode": 1,
                    "taxBase": 0
                }
            ]
        }
    }

    return documento