



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