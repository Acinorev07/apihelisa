
def solicitar_obligatorio(mensaje):
    """Solicita un dato hasta que el usuario introduzca un valor."""
    while True:
        valor = input(mensaje).strip()

        if valor and valor.lower() != "null":
            return valor

        print("Este campo es obligatorio. Inténtalo nuevamente.")



def normalizar_nombres(nombre):
    """
    Normaliza un nombre completo y devuelve un diccionario
    con nombres, apellidos y nombre completo.

    Esta función supone que una persona tiene:
    - Un nombre.
    - Opcionalmente, un segundo nombre.
    - Un apellido.
    - Opcionalmente, un segundo apellido.

    Importante: la separación se basa en la posición de las palabras.
    No identifica automáticamente partículas como 'DE LA' o distingue
    nombres de razones sociales.
    """

    if nombre is None:
        raise ValueError("El nombre no puede estar vacío.")

    # Convertir a texto, eliminar espacios externos y convertir a mayúsculas.
    nombre = " ".join(str(nombre).upper().split())

    #Remplaza " DEL " por " "
    sin_del = nombre.replace(" DEL ", " ")

    #Remplaza " DE " por " "
    sin_de = sin_del.replace(" DE ", " ")

    if not sin_de or sin_de.lower() == "null":
        raise ValueError("El nombre no puede estar vacío.")

    # Separar las palabras ignorando espacios repetidos.
    palabras = sin_de.split()


    

    # Inicializar los campos.
    resultado = {
        "primer_nombre": "",
        "segundo_nombre": "",
        "primer_apellido": "",
        "segundo_apellido": "",
        "nombre_completo": nombre
    }

    # Para evitar asignaciones incorrectas, necesitamos al menos dos palabras.
    if len(palabras) < 2:
        raise ValueError(
            "Se necesitan al menos dos palabras para separar nombres y apellidos."
        )

    if len(palabras) == 2:
        resultado["primer_nombre"] = palabras[0]
        resultado["primer_apellido"] = palabras[1]

    elif len(palabras) == 3:
        resultado["primer_nombre"] = palabras[0]
        resultado["primer_apellido"] = palabras[1]
        resultado["segundo_apellido"] = palabras[2]

    else:
        resultado["primer_nombre"] = palabras[0]
        resultado["segundo_nombre"] = palabras[1]
        resultado["primer_apellido"] = palabras[2]
        resultado["segundo_apellido"] = " ".join(palabras[3:])


    return resultado

     




if __name__ == "__main__":


     nombre = solicitar_obligatorio(
         "Ingrese el nombre del tercero: "
     )

     lista = normalizar_nombres(nombre=nombre)
     print(f"Nombre: {lista}")
     