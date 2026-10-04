from hooks.limpiarPantalla import limpiar_pantalla
from api.helisa.route import POST
from hooks.date import dateMillisec

def menu_helisa():



    config = {
        "url_raiz": "https://webconektaorquestador.helisa.com",
        "url_final":{
            "1":"/KansasWS/get/thirdParty2_0",
            "2":"/KansasWS/summary/thirdPartyFromAccount"
        }
    }

    try:

          while True:

            limpiar_pantalla()

            print("\n=====MENU API HELISA=======")
            print("1: Obtner cartilla de terceros.")
            print("2: Lectura de saldos de una cuenta por terceros.")
            print("3: Descargar información a excel")
            print("4: Salir")
            
        

            opcion = int(input("Opcion: "))

            if opcion == 1:
                limpiar_pantalla()
                url = (
                        config["url_raiz"] +
                        config["url_final"]["1"]
                    )

                print("Opción 1 todavía en construcción.") 

                input("\nPresiona ENTER para continuar...")


            elif opcion == 2:
                limpiar_pantalla()   

                url = (
                    config["url_raiz"]
                    +
                    config["url_final"]["2"]
                    )


                # Epoch en milisegundos
                date = dateMillisec()

                # Pedir al usuario la cuenta contable a consultar
                cuenta = input("cuenta contable: ")
            
                # IMPORTANTE:
                # La firma se calcula sobre ESTE STRING exacto.
                json_data = (
                    '{"date":' + str(date) +
                    ',"account":"' + cuenta + '"}'
                )

                print("Estamos en la opción 2 url: ",url)
                print("Estamos en la opción 2 json_data: ",json_data)

                response = POST(
                    url, 
                    json_data
                    )

                

                if response is not None:

                    print("\nCódigo:", response.status_code)
                    print("Respuesta:")
                    print(response.text)

                    input("\nPresiona ENTER para continuar...")

            elif opcion == 3:
                limpiar_pantalla() 


                print("Opción 3 todavía en construcción.")

                input("\nPresiona ENTER para continuar...")

                 

            elif opcion == 4:
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida, intenta de nuevo.")

            

    except Exception as e:
            print(f"\nError en la ejecución: {str(e)}")
            return None