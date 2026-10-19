from hooks.configuracion_APIs import obtener_url
import json
from api.helisa.route import POST

def insertar_documento():
    print("\n===== INSERTAR DOCUMENTO =====")
    
    url = obtener_url(
            "helisa",
            "document"
        )
    
    tipo = input("Tipo de documento: ")
    numero = input("Número del documento: ")
    
    fecha = input(
        "Fecha (DD/MM/YYYY): "
    )

    nit = input(
        "NIT del tercero: "
    )

    cuenta_debito = input(
        "Cuenta débito [41600509]: "
    )

    cuenta_credito = input(
        "Cuenta crédito [110505]: "
    )

    valor = int(
        input("Valor: ")
    )

    # --------------------------------
    # Convertir fecha
    # --------------------------------

    dia, mes, anio = map(
        int,
        fecha.split("/")
    )

    # --------------------------------
    # Construir documento
    # --------------------------------

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
                    "nature": {
                        "tag": "D"
                    },

                    "costCenter": "061002",

                    "concept": "Prueba API Helisa",

                    "accountingClass": {
                        "value": 0
                    },

                    "value": valor,

                    "idThirdParty": nit,

                    "account": cuenta_debito,

                    "userCode": 1,

                    "taxBase": 0
                },

                {
                    "nature": {
                        "tag": "C"
                    },

                    "costCenter": "061002",

                    "concept": "Prueba API Helisa",

                    "accountingClass": {
                        "value": 0
                    },

                    "value": valor,

                    "idThirdParty": nit,

                    "account": cuenta_credito,

                    "userCode": 1,

                    "taxBase": 0
                }
            ]
        }
    }

    # --------------------------------
    # Convertir Python → JSON
    # --------------------------------

    json_data = json.dumps(
        documento,
        separators=(",", ":")
    )

    print("\nJSON que se enviará:")
    print(json_data)

    # --------------------------------
    # Enviar a Helisa
    # --------------------------------

    response = POST(
        url,
        json_data
    )

    if response is not None:

        print("\nCódigo:", response.status_code)

        print("Respuesta:")

        print(response.text)