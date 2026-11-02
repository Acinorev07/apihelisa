


def solicitar_documento(mensaje, documentos):

    # Construimos un conjunto con los códigos permitidos
    tipos_validos = {
        str(dcto["type"]).strip().upper()
        for dcto in documentos
        if dcto.get("type")
    }

    if not tipos_validos:
        raise ValueError("No hay tipos de documentos disponibles para validar.")

    while True:

        document_type = input(mensaje).strip().upper()

        if not document_type:
            print("Error: el tipo de documento es obligatorio.")
            continue

        if document_type in tipos_validos:
            return document_type

        print(
            f"El documento '{document_type}' no existe en Helisa. "
            "Por favor, ingresa un código válido."
        )