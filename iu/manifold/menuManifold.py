
from hooks.limpiarPantalla import limpiar_pantalla
from hooks.validar_terceros import validar_terceros
from services.manifold.generar_tercero_q10_helisa import (
    generar_terceros_q10_helisa,
    enviar_terceros_q10_helisa
)
from hooks.obtener_archivo_json import cargar_archivo

import json
import traceback

def menu_manifold():

    try:
          
          nuevos = {}

          while True:

            limpiar_pantalla()

            print("\n=====MENU API HELISA=======")
            print("1: Validar terceros de Q10 en Helisa.")
            print("2: Insertar terceros a helisa.")
            print("3: En construcción")
            print("4: Salir")
            

            opcion = int(input("Opcion: "))

            if opcion == 1:
                try:
                    limpiar_pantalla()

                    nuevos = validar_terceros()

                    if not nuevos:
                        print("\nNo se encontraron terceros nuevos.")
                    else:
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

                    print(
                        f"\nTotal de terceros pendientes: {len(nuevos)}"
                    )
                                
                except Exception as e:
                    print(f"\nError en la ejecución: {str(e)}")
                    return None

                input("\nPresiona ENTER para continuar...")


            elif opcion == 2: 

                try:
                    limpiar_pantalla()

                    if not nuevos:
                        print(
                            "\nNo hay terceros pendientes. "
                            "Primero ejecuta la opción 1."
                        )

                    else: 
                        # Extraer todas las facturas de los terceros nuevos
                        facturas = []

                        for identificacion, informacion in nuevos.items():

                            facturas.extend(
                                informacion.get("facturas", [])
                            )
                            
                        
                        print(f"Facturas: {facturas}")

                        
                        
                        print("\n========== RESUMEN DE ENVÍO ==========")
                        print(f"Terceros nuevos: {len(nuevos)}")
                        print(f"Facturas asociadas: {len(facturas)}")

                        generacion = generar_terceros_q10_helisa(
                                        facturas=facturas
                                    )

                        print("\n===== RESUMEN DE GENERACIÓN =====")

                        print(
                            f"Terceros únicos: "
                            f"{len(generacion['terceros'])}"
                        )

                        print(
                            f"Errores de generación: "
                            f"{len(generacion['errores'])}"
                        )

                        if not generacion["terceros"]:
                            print("\nNo hay terceros para enviar.")

                        else:

                            confirmacion = input(
                                "\n¿Deseas enviar estos terceros a Helisa? (S/N): "
                            ).strip().upper()

                            if confirmacion == "S":


                                resultado = enviar_terceros_q10_helisa(
                                        resultado_generacion=generacion
                                    )

                                print("\n========== RESUMEN DE INSERCIÓN ==========")

                                print(
                                    f"Terceros procesados: "
                                    f"{resultado['total_terceros']}"
                                )

                                print(
                                    f"Inserciones exitosas: "
                                    f"{len(resultado['insertados'])}"
                                )

                                print(
                                    f"Errores de generación: "
                                    f"{len(resultado['errores_generacion'])}"
                                )

                                print(
                                    f"Errores de inserción: "
                                    f"{len(resultado['errores_insercion'])}"
                                )

                            else:
                                print("\nProceso cancelado. No se enviaron terceros.")

                except Exception:
                    traceback.print_exc()

                
                
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