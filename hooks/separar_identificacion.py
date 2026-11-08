

def separar_identificacion(numero):
    if numero is None:
        raise ValueError("La identificación está vacía.")

    partes = str(numero).strip().rsplit("-", 1)

    identificacion = "".join(
        c for c in partes[0] if c.isdigit()
    )

    digito = ""

    if len(partes) == 2:
        digito = "".join(
            c for c in partes[1] if c.isdigit()
        )

    if not identificacion:
        raise ValueError("La identificación no es válida.")

    return identificacion, digito
