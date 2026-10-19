from iu.helisa.menuHelisa import menu_helisa
from iu.q10.menuQ10 import menu_q10
from hooks.limpiarPantalla import limpiar_pantalla


def main():

    config = {
            "id_API": {
                "1": "Helisa",
                "2": "Q10"
            },
            "format_date":{
                "1":'%Y%m%d',
                "2":'%d/%m/%Y'
                },
            "id_url_final":{
                "1":"helisa",
                "2":"Q10"
            }

        }

    try:

        while True:
            limpiar_pantalla()

            print("\n--- Acceder APIs ---")
            print("1: Helisa")
            print("2: Q10")
            print("3: Salir")

            opcion = int(input("Opción: "))

            if opcion == 1:

                try:

                    menu_helisa()

                except Exception as e:
                        print(f"\nError en la ejecución: {str(e)}")

            elif opcion == 2:
                try:
                
                    menu_q10()
                                    
                except Exception as e:
                    print(f"\nError en la ejecución: {str(e)}")

                
                input("\nPresiona ENTER para continuar...")
                  
            elif opcion == 3:
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida, intenta de nuevo.")

    except Exception as e:
        print(f"\nError en la ejecución: {str(e)}")




 
if __name__ == "__main__":
    main()