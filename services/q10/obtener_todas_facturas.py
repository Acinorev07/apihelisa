from services.q10.obtener_facturas import obtener_facturas

def obtener_todas_las_facturas(params, limite=1000):
    """
    Consulta todas las facturas de Q10 mediante paginación.
    Muestra el progreso de cada bloque consultado.
    """

    todas_las_facturas = []
    offset = int(params.get("offset") or 0)
    bloque = 1

    while True:

        parametros = params.copy()
        parametros["limite"] = limite
        parametros["offset"] = offset

        print("\n" + "=" * 50)
        print(f"CONSULTANDO BLOQUE: {bloque}")
        print(f"Registros solicitados: {limite}")
        print(f"Offset: {offset}")
        print("=" * 50)

        try:
            response = obtener_facturas(params=parametros)

            if not isinstance(response, list):
                print("La respuesta de Q10 no contiene una lista.")
                break

            cantidad = len(response)

            if cantidad == 0:
                print("No se encontraron más facturas.")
                break

            todas_las_facturas.extend(response)

            print(f"Registros recibidos: {cantidad}")
            print(f"Total acumulado: {len(todas_las_facturas)}")

            if cantidad < limite:
                print("Se alcanzó el último bloque.")
                break

            offset += cantidad
            bloque += 1

        except Exception as e:
            print(f"Error consultando el bloque {bloque}: {e}")
            break

    print("\n" + "=" * 50)
    print("RESUMEN DE CONSULTA")
    print(f"Total de facturas: {len(todas_las_facturas)}")
    print(f"Bloques consultados: {bloque}")
    print("=" * 50)

    return todas_las_facturas
