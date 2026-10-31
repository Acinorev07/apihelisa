from hooks.limpiarPantalla import limpiar_pantalla
from services.helisa.obtener_tercero import obtener_tercero
from services.helisa.obtener_saldos_cuentas import obtener_saldos_cuenta
from services.helisa.insertar_documento import insertar_documento
from services.helisa.obtener_dcto_helisa import obtener_dcto_helisa
from iu.forms.form_obtener_tercero import form_obtener_tercero
from iu.forms.solicitar_fecha import solicitar_fecha
from iu.forms.solicitar_tipo_contabilidad import solicitar_tipo_contabilidad
from iu.forms.solicitar_documento import solicitar_documento

import json



def menu_helisa():

    try:

          while True:

            limpiar_pantalla()

            print("\n=====MENU API HELISA=======")
            print("1: Obtner cartilla de terceros.")
            print("2: Lectura de saldos de una cuenta por terceros.")
            print("3: Insertar documento a helisa.")
            print("4: Obtener documento de helisa.")
            print("5: Obtener documentos de helisa")
            print("6: Salir")
            
        

            opcion = int(input("Opcion: "))

            if opcion == 1:
                try:
                    limpiar_pantalla()

                    fecha, docId = form_obtener_tercero()
                    
                    response = obtener_tercero(fecha, docId)

                    print(json.dumps(
                            response.json(),
                            indent=4,
                            ensure_ascii=False,
                        ))

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
                
                 try:
                    limpiar_pantalla()

                        # Solicitar fechas
                    fecha_inicial = solicitar_fecha(
                        "Ingresa la fecha inicial (YYYY-MM-DD): "
                    )

                    fecha_final = solicitar_fecha(
                        "Ingresa la fecha final (YYYY-MM-DD): "
                    )


                    # Solicitar documento
                    documento = solicitar_documento(
                         "Ingresa el tipo de documento (ejemplo FV): "
                         )

                    # Solicitar tipo de contabilidad
                    accounting_type = solicitar_tipo_contabilidad()


                    response = obtener_dcto_helisa(
                         fecha_inicial=fecha_inicial,
                         fecha_final=fecha_final,
                         document_type= documento,
                         accounting_type=accounting_type
                         )


                    print(f"Respuesta documentos: {
                         json.dumps(
                            response,
                            indent=4,
                            ensure_ascii=False
                        )
                    
                    }"
                    )
                     
                    
                 except Exception as e:
                    print(f"\nError en la ejecución: {str(e)}")
                    return None

                 input(
                    "\nPresiona ENTER para continuar..."
                    )

            elif opcion == 5:
                 try:
                     limpiar_pantalla()

                 except Exeption as e:
                     print(f"\nError en la ejecución: {str(e)}")
                     return None

                    


            elif opcion == 6:
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida, intenta de nuevo.")

            

    except Exception as e:
            print(f"\nError en la ejecución: {str(e)}")
            return None