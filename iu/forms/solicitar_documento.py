


def solicitar_documento(mensaje):


        while True:

        # Solicitar tipo de documento
            document_type = input(
                mensaje
            ).strip().upper()
            try:
        
                return document_type
                    
                
    
            except ValueError:
                print(
                    "Error: el tipo de documento es obligatorio."
                )