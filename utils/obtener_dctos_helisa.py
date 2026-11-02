from hooks.configuracion_APIs import obtener_url
from api.helisa.route import GET
from hooks.date import dateMillisec
import json



def obtener_dctos_helisa():

    fecha = input(
        "Ingresa la fecha en formato YYYY-MM-DD "
        "(presiona Enter para omitirla): "
    ).strip()

    # Obtener la dirección del endpoint
    url = obtener_url(
        "helisa",
        "lista_documentos"
    )

    # Convertir la fecha a milisegundos si se proporcionó.
    if fecha:
        try:
            date = dateMillisec(fecha)
        except (ValueError, TypeError) as e:
            print(f"Error al convertir la fecha: {e}")
            return
    else:
        date = None

    # Consultar Helisa
    response = GET(
        url,
        date
    )

    if response is None:
        print("No se pudo realizar la consulta.")
        return

    print(f"\nCódigo HTTP: {response.status_code}")

    if response.status_code == 200:
        try:
            datos = response.json()

            print("\nTipos de documentos contables:\n")

            print(json.dumps(
                    datos,
                    indent=4,
                    ensure_ascii=False,
                ))


            # print(datos)

        except ValueError:
            print("Helisa respondió, pero el contenido no es JSON válido.")
            print(response.text)

    elif response.status_code == 204:
        print("Helisa no tiene tipos de documentos configurados.")

    elif response.status_code == 401:
        print("Helisa rechazó la firma HMAC. Debemos revisar la clave y el payload.")

    elif response.status_code == 409:
        print("Helisa indica que el cliente no está registrado.")

    elif response.status_code == 423:
        print("El archivo de parámetros de Helisa está bloqueado.")

    else:
        print("Respuesta de Helisa:")
        print(response.text)


if __name__ == "__main__":
    obtener_dctos_helisa()