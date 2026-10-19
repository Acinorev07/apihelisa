from hooks.limpiarPantalla import limpiar_pantalla
from services.helisa.obtener_tercero import obtener_tercero
from services.helisa.obtener_saldos_cuentas import obtener_saldos_cuenta
from services.helisa.insertar_documento import insertar_documento


def menu_helisa():

    try:

          while True:

            limpiar_pantalla()

            print("\n=====MENU API HELISA=======")
            print("1: Obtner cartilla de terceros.")
            print("2: Lectura de saldos de una cuenta por terceros.")
            print("3: Insertar documento a helisa.")
            print("4: Salir")
            
        

            opcion = int(input("Opcion: "))

            if opcion == 1:
                try:
                    limpiar_pantalla()

                    response = obtener_tercero()

                    print(response)

                except Exception as e:
                            print(f"\nError en la ejecución: {str(e)}")
                            return None

                input("\nPresiona ENTER para continuar...")


            elif opcion == 2: 

                try:
                    limpiar_pantalla()

                    response = obtener_saldos_cuenta()

                    print("\nCódigo:", response.status_code)
                    print("Respuesta:")
                    print(response.text)

                except Exception as e:
                            print(f"\nError en la ejecución: {str(e)}")
                            return None
                
                
                input("\nPresiona ENTER para continuar...")

            elif opcion == 3:

                try:

                    limpiar_pantalla()

                    insertar_documento()

                except Exception as e:
                    print(f"\nError en la ejecución: {str(e)}")
                    return None

                input(
                    "\nPresiona ENTER para continuar..."
                    )

            elif opcion == 4:
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida, intenta de nuevo.")

            

    except Exception as e:
            print(f"\nError en la ejecución: {str(e)}")
            return None