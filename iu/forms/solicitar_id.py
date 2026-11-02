


def solicitar_id(mensaje):


    while True:

        id = input(mensaje).strip()

        try:
            if not id:
                print("Error: el tipo de documento es obligatorio.")
                continue
            
            return id

        except ValueError:
            print(
                "Debes ingresar el código o identificación del estudiante."
            )

