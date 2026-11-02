




from datetime import datetime


def solicitar_fecha(mensaje):
    """Solicita una fecha válida en formato YYYY-MM-DD."""

    while True:
        fecha_texto = input(mensaje).strip()

        try:
            fecha = datetime.strptime(fecha_texto, "%Y-%m-%d")

            return fecha.strftime("%Y-%m-%d")

        except ValueError:
            print(
                "Fecha inválida. "
                "Utiliza el formato YYYY-MM-DD, "
                "por ejemplo 2026-10-12."
            )
