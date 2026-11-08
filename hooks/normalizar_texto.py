import unicodedata

def normalizar_texto(texto):
    texto = str(texto).strip().lower()

    texto = unicodedata.normalize("NFD", texto)

    return "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )