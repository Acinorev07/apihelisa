from hooks.limpiarPantalla import limpiar_pantalla
from services.q10.obtener_facturas import obtener_facturas
from services.q10.obtener_pago_facturas import obtener_pago_facturas
from services.q10.obtener_pago_creditos import obtener_pago_creditos
import json
from datetime import datetime
import time


def menu_q10():

    try:

          while True:

            limpiar_pantalla()

            print("\n=====MENU API HELISA=======")
            print("1: Obtener facturas: ")
            print("2: Obtener pago facturas: ")
            print("3: Obtener recivos de pago credito: ")
            print("4: Salir")
            
        

            opcion = int(input("Opcion: "))

            if opcion == 1:
                limpiar_pantalla()
                response = obtener_facturas()

                print(response)

                input("\nPresiona ENTER para continuar...")


            elif opcion == 2:
                limpiar_pantalla()  
                response = obtener_pago_facturas()

                print(response)

                input("\nPresiona ENTER para continuar...")

            elif opcion == 3:
                    limpiar_pantalla()  
                    response = obtener_pago_creditos()

                    print(response)


                    input("\nPresiona ENTER para continuar...")
                
            elif opcion == 4:
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida, intenta de nuevo.")

            

    except Exception as e:
            print(f"\nError en la ejecución: {str(e)}")
            return None