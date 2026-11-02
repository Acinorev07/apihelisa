
from hooks.limpiarPantalla import limpiar_pantalla
from hooks.validar_terceros import validar_terceros
import json


def menu_manifold():

    try:

          while True:

            limpiar_pantalla()

            print("\n=====MENU API HELISA=======")
            print("1: Validar terceros de Q10 en Helisa.")
            print("2: En construcción")
            print("3: En construcción")
            print("4: Salir")
            
        

            opcion = int(input("Opcion: "))

            if opcion == 1:
                try:
                    limpiar_pantalla()

                    nuevos = validar_terceros()

                    print("\n========== TERCEROS PENDIENTES ==========")

                    for identificacion, informacion in nuevos.items():
                        print(f"\nIdentificación: {identificacion}")
                        print(f"\nInformacion: {json.dumps(
                            informacion,
                            indent=4,
                            ensure_ascii=False
                            )}")
                        print(f"Facturas asociadas: {len(informacion['facturas'])}")

                        for factura in informacion["facturas"]:
                            print(
                                "Factura:",
                                factura.get("Numero_factura"),
                                "| Nombre:",
                                factura.get("Nombre_completo_estudiante")
                                or factura.get("Nombre_completo_tercero"),
                            )

                                    # print(response)

                except Exception as e:
                    print(f"\nError en la ejecución: {str(e)}")
                    return None

                input("\nPresiona ENTER para continuar...")


            elif opcion == 2: 

                # try:
                #     limpiar_pantalla()

                #     # response = obtener_saldos_cuenta()

                #     # print("\nCódigo:", response.status_code)
                #     print("Respuesta:")
                #     # print(response.text)

                # except Exception as e:
                #             print(f"\nError en la ejecución: {str(e)}")
                #             return None
                
                
                input("\nPresiona ENTER para continuar...")

            elif opcion == 3:

                try:

                    limpiar_pantalla()

                    # insertar_documento()

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