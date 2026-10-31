from datetime import datetime
from api.helisa.route import POST
from hooks.configuracion_APIs import obtener_url
import json



def obtener_dcto_helisa(fecha_inicial, fecha_final, document_type,accounting_type):

     # Obtener URL del endpoint
    url = obtener_url(
        "helisa",
        "summary_documento"
    )
    
    # Convertir los textos ingresados a fechas
    fecha_inicio = datetime.strptime(
        fecha_inicial,
        "%Y-%m-%d"
    )

    fecha_fin = datetime.strptime(
        fecha_final,
        "%Y-%m-%d"
    )

    # Construir las fechas como objetos JSON
    filtros = {
        "startDate": {
            "day": fecha_inicio.day,
            "month": fecha_inicio.month,
            "year": fecha_inicio.year
        },
        "endDate": {
            "day": fecha_fin.day,
            "month": fecha_fin.month,
            "year": fecha_fin.year
        },
        "documentType": document_type,
        "accountingType": accounting_type
    }

    # Serializar una sola vez para firmar y enviar
    json_data = json.dumps(
        filtros,
        separators=(",", ":"),
        ensure_ascii=False
    )

    print("\nURL:", url)
    print("Filtros de consulta:")
    print(json.dumps(filtros, indent=4, ensure_ascii=False))

    # Consultar Helisa
    response = POST(
        url,
        json_data
    )

    if response is None:
        print("No se recibió respuesta de Helisa.")
        return None

    print(f"\nCódigo HTTP: {response.status_code}")

    if response.status_code == 200:
        try:
            datos = response.json()

            return datos

        except ValueError:
            print("La respuesta no contiene JSON válido.")
            print(response.text)
            return None

    elif response.status_code == 204:
        print("No se encontraron documentos con esos filtros.")

    elif response.status_code == 400:
        print("Helisa rechazó los datos enviados.")
        print(response.text)

    elif response.status_code == 401:
        print("Firma HMAC inválida o cliente no registrado.")
        print(response.text)

    elif response.status_code == 409:
        print("Error de validación informado por Helisa.")
        print(response.text)

    elif response.status_code == 423:
        print("El archivo de parámetros de Helisa está bloqueado.")
        print(response.text)

    else:
        print("Respuesta inesperada de Helisa:")
        print(response.text)

    return None


