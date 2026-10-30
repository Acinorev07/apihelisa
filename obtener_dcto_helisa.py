
from hooks.configuracion_APIs import obtener_url
from hooks.date import dateMillisec
import json
from datetime import datetime, time
from api.helisa.route import POST
from datetime import datetime


def solicitar_fecha(mensaje):
    """Solicita una fecha válida en formato YYYY-MM-DD."""

    while True:
        fecha_texto = input(mensaje).strip()

        try:
            return fecha_texto
                
            

        except ValueError:
            print(
                "Fecha inválida. "
                "Utiliza el formato YYYY-MM-DD, por ejemplo 2026-10-12."
            )





def solicitar_tipo_contabilidad():
    """Solicita el tipo de contabilidad aceptado por Helisa."""

    while True:
        tipo = input(
            "Tipo de contabilidad (0 = Local, 1 = NIIF): "
        ).strip()

        if tipo in ("0", "1"):
            return int(tipo)

        print("Opción inválida. Ingresa 0 o 1.")


def obtener_dcto_helisa():

    # Obtener URL del endpoint
    url = obtener_url(
        "helisa",
        "summary_documento"
    )

    # Solicitar fechas
    fecha_inicial = solicitar_fecha(
        "Ingresa la fecha inicial (YYYY-MM-DD): "
    )

    fecha_final = solicitar_fecha(
        "Ingresa la fecha final (YYYY-MM-DD): "
    )

    if fecha_inicial > fecha_final:
        print(
            "Error: la fecha inicial no puede ser posterior "
            "a la fecha final."
        )
        return None

    # Solicitar tipo de documento
    document_type = input(
        "Ingresa el tipo de documento (ejemplo FV): "
    ).strip().upper()

    if not document_type:
        print("Error: el tipo de documento es obligatorio.")
        return None

    # Solicitar tipo de contabilidad
    accounting_type = solicitar_tipo_contabilidad()

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

            print("\nDocumentos encontrados:")
            print(
                json.dumps(
                    datos,
                    indent=4,
                    ensure_ascii=False
                )
            )

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


if __name__ == "__main__":
    obtener_dcto_helisa()