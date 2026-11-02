from iu.forms.solicitar_opcional import solicitar_opcional
from hooks.validar_correo import validar_correo

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