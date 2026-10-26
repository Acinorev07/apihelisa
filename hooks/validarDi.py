
import re


def validar_documento_tercero(di):
    """
    Limpia y valida el documento de identidad.

    Si contiene un guion seguido de un dígito de verificación,
    elimina el guion y el dígito de verificación.

    Retorna el documento como str para conservar los ceros iniciales.
    """

    if di is None:
        raise ValueError("El documento de identidad no puede estar vacío.")

    di = str(di).strip()

    # Si tiene un guion seguido de un dígito, elimina ambos.
    di = re.sub(r"-\d$", "", di)

    # Validar que el documento resultante contenga solo números.
    if not re.fullmatch(r"[0-9]+", di):
        raise ValueError(
            "El documento debe contener únicamente números, "
            "opcionalmente con un dígito de verificación al final "
            "separado por un guion."
        )

    return di
