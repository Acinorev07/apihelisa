from services.q10.obtener_facturas import obtener_facturas
from hooks.crear_archivo_json import crear_archivo_json

def obtener_todas_las_facturas_q10(params, limite=1000):

    """
    Consulta todas las facturas de Q10 mediante paginación.
    Muestra el progreso de cada bloque consultado.

    """
    todas_las_facturas = []

    offset = 1


    while True:

        parametros = params.copy()

        parametros["limite"] = limite
        parametros["offset"] = offset


        print("\n" + "=" * 50 )
        print(f"Consultando bloque: {offset}")
        print(f"Registros solicitados: {limite}")
        print(f"Offset: {offset}")
        print("=" * 50)


        

        try:

            response = obtener_facturas(params=parametros)

            if not isinstance(response, list):
                print("La respuesta de Q10 no contiene una lista")
                break

            cantidad = len(response)

            if cantidad == 0:

                print("No se encontraron mas facturas.")
                break

            todas_las_facturas.extend(response)

            print(f"Registros recibidos: {cantidad}")
            print(f"Total acumulado: {len(todas_las_facturas)}")

            if cantidad < limite:
                print("Se alcanzó el último bloque")
                break

            offset +=1

        except Exception as e:
            print(f"Error consultando el bloque: {offset}")
            break

    print("\n" + "=" * 50)
    print("RESUMEN DE CONSULTA")
    print(f"Total de facturas: {len(todas_las_facturas)}")
    print(f"Bloque consultado: {offset}")
    print("=" * 50)
    return todas_las_facturas

       




 



if __name__ == "__main__":

   params = {
            "fecha_inicio" : "2025-01-01",
            "fecha_fin" : "2026-11-12",
            "codigo_persona" : "",
            "consecutivo_tercero" : "",
            "codigo_producto" : "",
            "estado" : "4",
            "limite" : 1000,
            "offset" : 1
        }

   facturas = obtener_todas_las_facturas_q10(params=params)

   print (f"Total facturas: {len(facturas)}")
#  No ejecutar este comando a menos que sea estrictamente necesario
   crear_archivo_json(
       response=facturas,
       nombre_archivo="todas_las_facturas_q10_(4).json"
    )

   print("Facturas creadas con exito...")