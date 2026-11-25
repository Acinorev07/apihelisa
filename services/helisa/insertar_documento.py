from hooks.configuracion_APIs import obtener_url
import json
from api.helisa.route import POST

def insertar_documento(documento):
    print("\n===== INSERTAR DOCUMENTO =====")
    
    url = obtener_url(
            "helisa",
            "document"
        )
    
    # tipo = input("Tipo de documento: ")
    # numero = input("Número del documento: ")
    
    # fecha = input(
    #     "Fecha (DD/MM/YYYY): "
    # )

    # nit = input(
    #     "NIT del tercero: "
    # )

    # cuenta_debito = input(
    #     "Cuenta débito [41600509]: "
    # )

    # cuenta_credito = input(
    #     "Cuenta crédito [110505]: "
    # )

    # valor = int(
    #     input("Valor: ")
    # )

    # # --------------------------------
    # # Convertir fecha
    # # --------------------------------

    # dia, mes, anio = map(
    #     int,
    #     fecha.split("/")
    # )

    # # --------------------------------
    # # Construir documento
    # # --------------------------------

    # documento = {

    #     "document": {

    #         "date": {
    #             "day": dia,
    #             "month": mes,
    #             "year": anio
    #         },

    #         "document": {
    #             "type": tipo,
    #             "number": numero
    #         },

    #         "transactions": [

    #             {
    #                 "nature": {
    #                     "tag": "D"
    #                 },

    #                 "costCenter": "061002",

    #                 "concept": "Prueba API Helisa",

    #                 "accountingClass": {
    #                     "value": 0
    #                 },

    #                 "value": valor,

    #                 "idThirdParty": nit,

    #                 "account": cuenta_debito,

    #                 "userCode": 1,

    #                 "taxBase": 0
    #             },

    #             {
    #                 "nature": {
    #                     "tag": "C"
    #                 },

    #                 "costCenter": "061002",

    #                 "concept": "Prueba API Helisa",

    #                 "accountingClass": {
    #                     "value": 0
    #                 },

    #                 "value": valor,

    #                 "idThirdParty": nit,

    #                 "account": cuenta_credito,

    #                 "userCode": 1,

    #                 "taxBase": 0
    #             }
    #         ]
    #     }
    # }
    
    documento = {
        
        "document": {
            "date": {
                "day": 21,
                "month": 11,
                "year": 2026
            },
            "document": {
                "type": "NIED",
                "number": "00003451"
            },
            "transactions": [
                {
                    "nature": {
                        "tag": "D"
                    },
                    "costCenter": "",
                    "concept": "KAREN MARGARITA CARDONA MORENO-25950-SO2",
                    "accountingClass": {
                        "value": 0
                    },
                    "value": 52000.0,
                    "idThirdParty": "1099741540",
                    "account": "110505",
                    "userCode": 1,
                    "taxBase": 0
                },
                {
                    "nature": {
                        "tag": "C"
                    },
                    "costCenter": "060302",
                    "concept": "KAREN MARGARITA CARDONA MORENO-25950-SO2",
                    "accountingClass": {
                        "value": 0
                    },
                    "value": 52000.0,
                    "idThirdParty": "1099741540",
                    "account": "41600502",
                    "userCode": 1,
                    "taxBase": 0
                },
                {
                    "accountingClass": {
                        "value": 0
                    },
                    "nature": {
                        "tag": "D"
                    },
                    "matchCode": 1,
                    "concept": "KAREN JULIANA HERNANDEZ SERRANO-25949-F3",
                    "value": 35000.0,
                    "idThirdParty": "1095803707",
                    "account": "11201001",
                    "userCode": 1,
                    "taxBase": 0,
                    "bankAccount": "02-036-533244",
                    "bankCheckDate": {
                        "day": 21,
                        "month": 11,
                        "year": 2026
                    }
                },
                {
                    "nature": {
                        "tag": "C"
                    },
                    "costCenter": "060203",
                    "concept": "KAREN JULIANA HERNANDEZ SERRANO-25949-F3",
                    "accountingClass": {
                        "value": 0
                    },
                    "value": 35000.0,
                    "idThirdParty": "1095803707",
                    "account": "41600516",
                    "userCode": 1,
                    "taxBase": 0
                },
                {
                    "accountingClass": {
                        "value": 0
                    },
                    "nature": {
                        "tag": "D"
                    },
                    "matchCode": 1,
                    "concept": "MARCELL JULIAN RUEDA ACUÑA-25948-C2",
                    "value": 35000.0,
                    "idThirdParty": "1096539034",
                    "account": "11201001",
                    "userCode": 1,
                    "taxBase": 0,
                    "bankAccount": "02-036-533244",
                    "bankCheckDate": {
                        "day": 21,
                        "month": 11,
                        "year": 2026
                    }
                },
                {
                    "nature": {
                        "tag": "C"
                    },
                    "costCenter": "061002",
                    "concept": "MARCELL JULIAN RUEDA ACUÑA-25948-C2",
                    "accountingClass": {
                        "value": 0
                    },
                    "value": 35000.0,
                    "idThirdParty": "1096539034",
                    "account": "41600516",
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
        
    return response