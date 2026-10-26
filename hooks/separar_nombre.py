
import string

def separar_nombre(texto):

    palabras = texto.strip().upper().split()

    limpio = [p.strip(string.punctuation) for p in palabras]

    solo_letras = [p for p in limpio if p.isalpha()]

    return solo_letras



if __name__ == "__main__":

    texto = "LUCY EUGENIA ROJAS BOLIVAR"
    nombre = separar_nombre(texto)

    print(nombre)