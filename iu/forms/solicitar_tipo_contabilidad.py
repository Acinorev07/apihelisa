


def solicitar_tipo_contabilidad():
    """Solicita el tipo de contabilidad aceptado por Helisa."""

    while True:
        tipo = input(
            "Tipo de contabilidad (0 = Local, 1 = NIIF): "
        ).strip()

        if tipo in ("0", "1"):
            return int(tipo)

        print("Opción inválida. Ingresa 0 o 1.")