from hooks.limpiarPantalla import limpiar_pantalla
from services.q10.obtener_facturas import obtener_facturas
from services.q10.obtener_pago_facturas import obtener_pago_facturas
from services.q10.obtener_pago_creditos import obtener_pago_creditos
from services.q10.obtener_estudiante import obtener_estudiante
from services.q10.obtener_terceros import obtener_terceros
from services.q10.obtener_tercero import obtener_tercero
from hooks.obtener_estudiante_tercero import obtener_estudiante_tercero
from hooks.validarDi import validar_documento_tercero
from hooks.crear_archivo_json import crear_archivo_json
from iu.forms.solicitar_id import solicitar_id
from iu.forms.solicitar_fecha import solicitar_fecha
import json
from datetime import datetime
import time


def menu_q10():

    try:

          while True:

            limpiar_pantalla()

            print("\n=====MENU API HELISA=======")
            print("1: Obtener facturas.")
            print("2: Obtener pago facturas.")
            print("3: Obtener recivos de pago credito.")
            print("4: Obtener información estudiante.")
            print("5: Obtener todos los terceros registrados.")
            print("6: Obtener información tercero.")
            print("7: Salir.")
            
        

            opcion = int(input("Opcion: "))

            if opcion == 1:
                limpiar_pantalla()

                fecha_inicio = solicitar_fecha(
                            "Fecha inicial (según formato de Q10, ENTER para omitir): "
                        )
                
                fecha_fin = solicitar_fecha(
                    "Fecha final (según formato de Q10, ENTER para omitir): "
                )
        
                codigo_persona  = input("Código de persona (opcional): ").strip()

                consecutivo_tercero = input("Consecutivo tercero (opcional): ").strip()
                codigo_producto = input("Código de producto (opcional): ").strip()
                estado = input("Estado (1 anulada, 2 pagada, 3 abonada, 4 pendiente): ").strip()
                limite = input("Límite de registros (ENTER = 100): ").strip()
                offset = input("Offset (ENTER = 0): ").strip()


                params = {
                    "fecha_inicio" : fecha_inicio,
                    "fecha_fin" : fecha_fin,
                    "codigo_persona" : codigo_persona,
                    "consecutivo_tercero" : consecutivo_tercero,
                    "codigo_producto" : codigo_producto,
                    "estado" : estado,
                    "limite" : limite,
                    "offset" : offset
                }


                response = obtener_facturas(
                    params = params
                    )

                
                print(json.dumps(
                    response,
                    indent=4,
                    ensure_ascii=False
                ))

                # crear_archivo_json(
                #    response=response,
                #    nombre_archivo="facturas_q10"
                # )

                # for factura in response:
                #     nombre = obtener_estudiante_tercero(
                #          "Nombre_completo_estudiante",
                #          "Nombre_completo_tercero",
                #          factura
                #     )

                #     num_fecha = factura.get("Fecha_factura")
                    
                #     print(f" {nombre}")
                    

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

                limpiar_pantalla()
                di = solicitar_id(
                    "Código o identificación del estudiante: "
                )

                codigo_estudiante = validar_documento_tercero(di)

                codigo_programa = input(       
                    "Código del programa (opcional): "
                )

                response = obtener_estudiante(
                    codigo_estudiante=codigo_estudiante,
                    codigo_programa = codigo_programa
                    )

                print(json.dumps(
                    response,
                    indent=4,
                    ensure_ascii=False
                ))

                input("\nPresiona ENTER para continuar...")


            elif opcion == 5: 
                limpiar_pantalla()

                estado = input("Ingrese el estado del tercero True o False")
                offset = input("Offset (ENTER = 0): ").strip()
                limite = input("Límite de registros (ENTER = 100): ").strip()

                response = obtener_terceros(
                    estado=estado,
                    offset=offset,
                    limite = limite 
                )


                # crear_archivo_json(
                #    response=response,
                #    nombre_archivo="terceros_q10"
                # )

                for tercero in response:
                    nombre = tercero.get("Nombre_completo")
                    codigo_tipo_idetificacion = tercero.get("Codigo_tipo_identificacion")
                    numero_id = tercero.get("Numero_identificacion")

                    print(f"Total terceros activos: {len(response)}")
                    print(f"\nNombre: {nombre} | codigo_tipo_id: {codigo_tipo_idetificacion} | numero_id: {numero_id}")




                input("\nPresiona ENTER para continuar...")

            elif opcion == 6:

                consecutivo_tercero = input("Ingrese el consecutivo del tercero a consultar: ")
                response = obtener_tercero(consecutivo_tercero)

                print(json.dumps(
                    response,
                    indent=4,
                    ensure_ascii=False
                ))

                input("\nPresiona ENTER para continuar...")
            elif opcion == 7:
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida, intenta de nuevo.")

            

    except Exception as e:
            print(f"\nError en la ejecución: {str(e)}")
            return None