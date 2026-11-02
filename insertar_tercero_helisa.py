import json
import re
from hooks.configuracion_APIs import obtener_url
from hooks.validarDi import validar_documento_tercero
from api.helisa.route import POST


def solicitar_obligatorio(mensaje):
    """Solicita un dato hasta que el usuario introduzca un valor."""
    while True:
        valor = input(mensaje).strip()

        if valor and valor.lower() != "null":
            return valor

        print("Este campo es obligatorio. Inténtalo nuevamente.")


def solicitar_opcional(mensaje, longitud_maxima=None):
    """Solicita un dato opcional y valida su longitud."""
    while True:
        valor = input(mensaje).strip()

        if valor.lower() == "null":
            valor = ""

        if longitud_maxima is not None and len(valor) > longitud_maxima:
            print(
                f"El campo admite como máximo "
                f"{longitud_maxima} caracteres."
            )
            continue

        return valor


def validar_correo(email):
    """Valida de forma básica la estructura de un correo electrónico."""
    if not email:
        return True

    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.fullmatch(patron, email) is not None


def solicitar_correo():
    """Solicita un correo opcional y valida su estructura."""
    while True:
        email = solicitar_opcional(
            "Correo electrónico (opcional): ",
            longitud_maxima=60,
        )

        if validar_correo(email):
            return email

        print("El correo no tiene una estructura válida.")


def solicitar_naturaleza():
    """Solicita la naturaleza jurídica o natural del tercero."""
    while True:
        naturaleza = input(
            "Naturaleza (J = Jurídica, N = Natural): "
        ).strip().upper()

        if naturaleza in ("J", "N"):
            return naturaleza

        print("Opción inválida. Introduce J o N.")


def insertar_tercero_helisa():

    url = obtener_url(
        "helisa",
        "create_tercero",
    )

    # 1. Recopilar los datos.
    nit_original = solicitar_obligatorio(
        "Documento de identidad del tercero: "
    )

    try:
        identificacion = validar_documento_tercero(nit_original)
    except ValueError as error:
        print(f"Documento inválido: {error}")
        return None

    nombre = solicitar_obligatorio(
        "Nombre completo o razón social: "
    )

    direccion = solicitar_opcional(
        "Dirección (opcional): ",
        longitud_maxima=60,
    )

    ciudad = solicitar_opcional(
        "Código de ciudad (opcional, máximo 5 caracteres): ",
        longitud_maxima=5,
    )

    departamento = solicitar_opcional(
        "Departamento (opcional): "
    )

    telefono = solicitar_opcional(
        "Teléfono (opcional, máximo 20 caracteres): ",
        longitud_maxima=20,
    )

    email = solicitar_correo()

    naturaleza = solicitar_naturaleza()

    # 2. Validaciones adicionales.
    if ciudad and not ciudad.isdigit():
        print("El código de ciudad debe contener solo números.")
        return None

    if telefono and len(telefono) > 20:
        print("El teléfono supera la longitud permitida.")
        return None

    # 3. Preparar el JSON.
    #
    # IMPORTANTE:
    # Este es un ejemplo de estructura de datos.
    # Los valores de documentType, nature, year, regimen,
    # economicActivity y userCode deben ajustarse a los
    # códigos válidos de tu empresa en Helisa.

    nuevo_tercero = {
        "thirdParty": {
            "secondLastName": "",
            "cree": False,
            "firstName": "",
            "economicActivity": "",
            "city": ciudad,
            "documentType": {
                "tag": "C"
            },
            "year": 2026,
            "nature": {
                "value": 0 if naturaleza == "J" else 1
            },
            "firstLastName": "",
            "name": nombre,
            "id": identificacion,
            "checkDigit": "",
            "regimen": {
                "tag": ""
            },
            "secondName": "",
            "userCode": 1,
            "telephones": telefono,
            "cellphone": "",
            "email": email,
            "address": direccion,
        }
    }

    # 4. Serializar una sola vez.
    json_data = json.dumps(
        nuevo_tercero,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    print("\nTercero preparado:")
    print(json.dumps(
        nuevo_tercero,
        ensure_ascii=False,
        indent=4,
    ))

    # 5. No enviar aún datos incompletos o códigos desconocidos.
    print(
        "\nAntes de enviar, verifica que los códigos de "
        "documentType, nature, regimen, economicActivity y "
        "userCode correspondan a los valores válidos en Helisa."
    )

    confirmar = input(
        "¿Deseas continuar con el envío? (S/N): "
    ).strip().upper()

    if confirmar != "S":
        print("Operación cancelada. No se envió el tercero.")
        return None

    # 6. Envío pendiente de integrar con el contrato de POST.
    #
    # La documentación exige los parámetros:
    # json, id y sign.
    # El texto firmado debe ser exactamente json_data.
    #
    # Antes de activar esta llamada, verifica que POST reciba
    # esos parámetros y genere la firma HMAC correctamente.

    print(
        "\nLos datos están preparados, pero el envío debe "
        "integrarse con la firma HMAC y los parámetros "
        "requeridos por Helisa."
    )

    return nuevo_tercero


if __name__ == "__main__":
   
   print(insertar_tercero_helisa())

   
