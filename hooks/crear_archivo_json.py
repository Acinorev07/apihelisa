import json


def crear_archivo_json(response, nombre_archivo):

    if response is not None:
    
        print(f"\nCantidad de facturas: {len(response)}")

        # Guardar respuesta en JSON
        with open(
            nombre_archivo,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                response,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        print("\nArchivo facturas_q10.json guardado correctamente.")

        print(json.dumps(
            response,
            indent=4,
            ensure_ascii=False
        ))

    else:
        print("No fue posible obtener las facturas.")