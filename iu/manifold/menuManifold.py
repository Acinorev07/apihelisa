
from hooks.limpiarPantalla import limpiar_pantalla
from hooks.validar_terceros import validar_terceros
from services.manifold.generar_supplier import generar_supplier_q10_helisa
from services.manifold.enviar_supplier_q10_helisa import enviar_supplier_q10_helisa
from services.manifold.generar_tercero_q10_helisa import (
    generar_terceros_q10_helisa,
    enviar_terceros_q10_helisa
)
from services.q10.obtener_facturas import obtener_facturas
from hooks.obtener_archivo_json import cargar_archivo
from hooks.obtener_estudiante_tercero import obtener_estudiante_tercero
from hooks.validarDi import validar_documento_tercero
from hooks.validar_existencia_recibo_en_factura import validar_existencia_recibo_en_factura
from hooks.validar_cuenta_factura import validar_cuenta_factura
import json
import traceback

def menu_manifold():

    try:
          
        nuevos = {}

        datos = []

        nuevos_pasivos = {}

        facturas_sin_recibo = None
        facturas_con_recibo = None

        clasificacion_con_recibo = None
        clasificacion_sin_recibo = None

        correctos = []
        errores = []

        while True:

            limpiar_pantalla()

            print("\n=====MENU API HELISA=======")
            print("1: Obtener facturas del día.")
            print("2: Validar terceros de Q10 en Helisa.")
            print("3: Insertar terceros a helisa.")
            print("4: Separar facturas con recibo y sin recibo.")
            print("5: Filtrar facturas por cuentas.")
            print("6: Validar pasivo tercero.")
            print("7: Validar cartera tercero.")
            print("8: Crear documento contable.")
            print("7: Salir")
            

            opcion = int(input("Opcion: "))


            if opcion == 1:

                try:
                    limpiar_pantalla()

                    # Reiniciar resultados de consultas anteriores
                    correctos = []
                    errores = []

                    nuevos = {}
                    nuevos_pasivos = {}

                    facturas_sin_recibo = None
                    facturas_con_recibo = None

                    clasificacion_con_recibo = None
                    clasificacion_sin_recibo = None

                    params = {
                        "fecha_inicio": "2026-11-19",
                        "fecha_fin": "2026-11-19",
                        "codigo_persona": "",
                        "consecutivo_tercero": "",
                        "codigo_producto": "",
                        "estado": "2",
                        "limite": 100,
                        "offset": 0
                    }

                    datos = obtener_facturas(params=params)

                    if isinstance(datos, list):
                        print(json.dumps(
                            datos[:1],
                            indent=4,
                            ensure_ascii=False
                        ))
                    else:
                        print(f"\nRespuesta de Q10: {datos}")

                except Exception as e:
                    print(f"\nError en la ejecución: {str(e)}")
                    traceback.print_exc()

                input("\nPresiona ENTER para continuar...")

            elif opcion == 2: 
                try:
                    limpiar_pantalla()

                    

                    # Caso 1: No se recibió respuesta válida
                    if datos is None:
                        print("No fue posible obtener las facturas.")

                    # Caso 2: Helisa devolvió un diccionario
                    elif isinstance(datos, dict):

                        codigo = datos.get("code")

                        if codigo == 404:
                            print("No se encontraron facturas para los parámetros indicados.")

                        else:
                            print(f"Error en la consulta: {datos.get('message', datos)}")

                    # Caso 3: Helisa devolvió una lista de facturas
                    elif isinstance(datos, list):

                        if not datos:
                            print("La consulta no devolvió facturas.")

                        else:
                            correctos, errores = validar_terceros(datos=datos)

                            print(f"\nCorrectos: {json.dumps(
                                correctos[1],
                                indent=4,
                                ensure_ascii=False
                            )}")

                            print(f"\nErrores: {json.dumps(
                                errores,
                                indent=4,
                                ensure_ascii=False
                            )}")
                         

                            for factura in datos:

                                id_tercero = obtener_estudiante_tercero(
                                            "Numero_identificacion_estudiante",
                                            "Numero_identificacion_tercero",
                                            factura
                                        )
                                
                                identificacion = validar_documento_tercero(id_tercero)

                                for error in errores:

                                    if error.get("identificacion") == identificacion:

                                        if identificacion not in nuevos:
                                            nuevos[identificacion] = {
                                                "facturas": []
                                            }

                                        nuevos[identificacion]["facturas"].append(factura)

                            print(f"\nNuevos:{json.dumps(
                                nuevos,
                                indent=4,
                                ensure_ascii=False
                            )}")
                    else:
                        print(f"Tipo de respuesta no esperado: {type(datos).__name__}")

                except Exception as e:
                    print(f"\nError en la ejecución: {str(e)}")
                    traceback.print_exc()

                input("\nPresiona ENTER para continuar...")
 

                
            elif opcion == 3:

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
                            f"{generacion['errores']}"
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
            elif opcion == 4:

                limpiar_pantalla()

                # Caso 1: No se recibió respuesta válida
                if not isinstance(datos, list):
                    print("Primero debes ejecutar la opción 1 y obtener las facturas.")

                else:

                    resultados = validar_existencia_recibo_en_factura(
                        facturas=datos
                    )

                    facturas_sin_recibo = resultados.get(
                        "facturas_sin_recibo", []
                    )

                    facturas_con_recibo = resultados.get(
                        "facturas_con_recibo", []
                    )

                    print("\n========== RESULTADOS ==========")
                    print(f"Total de facturas: {len(datos)}")
                    print(f"Facturas sin recibo: {len(facturas_sin_recibo)}")
                    print(f"Facturas con recibo: {len(facturas_con_recibo)}")

                input("\nPresiona ENTER para continuar...")
  
            elif opcion == 5:

                limpiar_pantalla()

                # Validar que primero se haya ejecutado la opción 4
                if facturas_sin_recibo is None or facturas_con_recibo is None:

                    print(
                        "\nPrimero debes ejecutar la opción 4 "
                        "para separar las facturas con recibo y sin recibo."
                    )

                else:

                    # Clasificar facturas con recibo
                    clasificacion_con_recibo = validar_cuenta_factura(
                        facturas_con_recibo
                    )

                    # Clasificar facturas sin recibo
                    clasificacion_sin_recibo = validar_cuenta_factura(
                        facturas_sin_recibo
                    )

                    grupos = [
                        "ingresos",
                        "pasivos",
                        "cartera",
                        "sin_clasificar"
                    ]

                    print("\n========== FACTURAS CON RECIBO ==========")

                    print(f"Total: {len(facturas_con_recibo)}")

                    for grupo in grupos:
                        print(
                            f"{grupo.capitalize()}: "
                            f"{len(clasificacion_con_recibo[grupo])}"
                        )

                    print("\n========== FACTURAS SIN RECIBO ==========")

                    print(f"Total: {len(facturas_sin_recibo)}")

                    for grupo in grupos:
                        print(
                            f"{grupo.capitalize()}: "
                            f"{len(clasificacion_sin_recibo[grupo])}"
                        )

                    print("\n========== RESUMEN GENERAL ==========")

                    for grupo in grupos:

                        total = (
                            len(clasificacion_con_recibo[grupo])
                            + len(clasificacion_sin_recibo[grupo])
                        )

                        print(f"{grupo.capitalize()}: {total}")


                    facturas_sin_clasificar = clasificacion_con_recibo["sin_clasificar"]

                    facturas_pasivos = clasificacion_con_recibo["pasivos"]

                    print(f"\nfacturas sin clasificar: {json.dumps(
                                            facturas_sin_clasificar,
                                            indent=4,
                                            ensure_ascii=False
                                        )}")
                    print(f"\nfacturas pasivos: {json.dumps(
                        facturas_pasivos,
                        indent=4,
                        ensure_ascii=False
                    )}")

                input("\nPresiona ENTER para continuar...")

            elif opcion == 6:

                limpiar_pantalla()

                if clasificacion_con_recibo is None:
                    print(
                        "\nPrimero debes ejecutar la opción 5 "
                        "para clasificar las facturas."
                    )

                elif not isinstance(correctos, list):
                    print("\nNo hay resultados válidos de la opción 2.")

                else:

                    facturas_pasivos = clasificacion_con_recibo.get(
                        "pasivos", {}
                    )

                    nuevos_pasivos = {}

                    # Crear un índice de terceros por identificación.
                    terceros_por_identificacion = {
                        tercero.get("identificacion"): tercero
                        for tercero in correctos
                        if isinstance(tercero, dict)
                    }

                    # Recorrer las facturas clasificadas como pasivos.
                    for numero_factura, factura in facturas_pasivos.items():

                        id_tercero = obtener_estudiante_tercero(
                            "Numero_identificacion_estudiante",
                            "Numero_identificacion_tercero",
                            factura
                        )

                        identificacion = validar_documento_tercero(id_tercero)

                        if identificacion is None:
                            print(
                                f"\nFactura {numero_factura}: "
                                "no tiene una identificación válida."
                            )
                            continue

                        # Buscar el tercero consultado anteriormente en Helisa.
                        tercero = terceros_por_identificacion.get(identificacion)

                        if tercero is None:
                            print(
                                f"\nFactura {numero_factura}: "
                                f"no se encontró el tercero {identificacion} "
                                "en los resultados de la opción 2."
                            )
                            continue

                        # Verificar si está registrado como proveedor.
                        if not tercero.get("es_proveedor", False):

                            if identificacion not in nuevos_pasivos:
                                nuevos_pasivos[identificacion] = {
                                    "nombre": tercero.get("nombre"),
                                    "facturas": []
                                }

                            nuevos_pasivos[identificacion]["facturas"].append(
                                {
                                    "numero_factura": numero_factura,
                                    "factura": factura
                                }
                            )

                    print(
                        "\n========== TERCEROS PENDIENTES COMO PROVEEDORES =========="
                    )

                    print(
                        f"\nTerceros pendientes: {len(nuevos_pasivos)}"
                    )
                    
                    print(json.dumps(
                        nuevos_pasivos,
                        indent=4,
                        ensure_ascii=False
                    ))


                    if not nuevos_pasivos:
                       print(
                            "\nNo hay supplier pendientes por anexar a los terceros. "
                        )

                    else: 
                        # Extraer todas las facturas de los terceros nuevos
                        facturas = []

                        for identificacion, informacion in nuevos_pasivos.items():

                            for registro in informacion.get("facturas", []):

                                factura = registro.get("factura")

                                if isinstance(factura, dict):
                                    facturas.append(factura)
                            
                        
                        print(f"Facturas: {facturas}")

                        
                        
                        print("\n========== RESUMEN DE ENVÍO ==========")
                        print(f"Pasivos nuevos: {len(nuevos_pasivos)}")
                        print(f"Facturas asociadas: {len(facturas)}")

                        generacion = generar_supplier_q10_helisa(
                                        facturas=facturas
                                    )

                        print("\n===== RESUMEN DE GENERACIÓN =====")

                        print(
                            f"Suppliers únicos: "
                            f"{len(generacion['suppliers'])}"
                        )

                        print(
                            f"Errores de generación: "
                            f"{len(generacion['errores'])}"
                        )

                        print(json.dumps(
                            generacion["errores"],
                            indent=4,
                            ensure_ascii=False
                        ))

                        if not generacion["suppliers"]:
                            print("\nNo hay proveedores para enviar.")

                        print("\n========== SUPPLIERS GENERADOS ==========")

                        for identificacion, informacion in generacion["suppliers"].items():

                            print(f"\nIdentificación: {identificacion}")

                            print("Facturas asociadas:")
                            for numero in informacion["facturas"]:
                                print(f"  - {numero}")

                            print("\nPayload del supplier:")
                            print(json.dumps(
                                informacion["supplier"],
                                indent=4,
                                ensure_ascii=False
                            ))


                        if not generacion["suppliers"]:
                            print("\nNo hay terceros para enviar.")

                        else:

                            confirmacion = input(
                                "\n¿Deseas enviar estos terceros a Helisa? (S/N): "
                            ).strip().upper()

                            if confirmacion == "S":


                                resultado = enviar_supplier_q10_helisa(
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



                input("\nPresiona ENTER para continuar...")

            elif opcion == 7:
                limpiar_pantalla()


                if clasificacion_con_recibo is None:
                    print(
                        "\nPrimero debes ejecutar la opción 5 "
                        "para clasificar las facturas."
                    )

                else:

                    facturas_pasivos = clasificacion_con_recibo.get(
                        "pasivos", {}
                    )

                    facturas_ingresos = clasificacion_con_recibo.get(
                        "ingresos",{}
                    )



                documento = generar_documento_helisa(facturas_pasivos, facturas_ingresos)


                input("\nPresiona ENTER para continuar...")

            elif opcion == 8:
                limpiar_pantalla()


                     


                input("\nPresiona ENTER para continuar...")



            elif opcion == 9:
                print("Saliendo del programa")
                break


    except Exception as e:
            print(f"\nError en la ejecución: {str(e)}")
            return None   