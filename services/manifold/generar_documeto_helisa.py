

def generar_documento_helisa(facturas_pasivos, facturas_ingresos):

    if not facturas_pasivos:

        print("Las facturas pasivos estan vacias")

    if not facturas_ingresos:
    
            print("Las facturas pasivos estan vacias")




    


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
                        "value": 2
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
        

