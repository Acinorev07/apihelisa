from hooks.configuracion_APIs import obtener_url
import json
from api.helisa.route import POST
from hooks.validarDi import validar_documento_tercero

def insertar_tercero_helisa():
    #  Obtenemos el punto de acceso
    url = obtener_url(
        "helisa",
        "create_tercero"
    )

    # Pedimos los datos al usuario

    nit = input("Inserte el documento de identidada del tercero (Obligatorio): ").strip()

    nombre = input("Ingrese el nombre o razon social del tercero (Obligatorio): ").strip()

    direccion = input("Ingrese la direccion de residencia del tercero (Opcional): ").strip()

    ciudad = input("Ingrese la ciudad de residencia del tercero (opcional): ").strip()

    departamento = input("Ingrese el departamento del tercero (Opcional): ").strip()

    telefono = input("Ingrese el telefono del tercero (Opcional): ").strip()

    email = input("Ingrese el correo electronico (Opcional): ").strip()

    naturalesa = input("Ingrese la naturaleza (J= Juridica o N= Natural)(obligatorio)").strip()

    # Validamos que los datos tengala estructura que requiere helisa y que sean strings
    identificacion = str(nit)

    if identificacion and identificacion.lower() != "null":
        try:
            return validar_documento_tercero(identificacion)
        except ValueError:
            print(ValueError)

    if nombre == "null":

        while True:

            if nombre != "null":
                break
            else:
                print("El nombre es obligatorio, vuelve a introducirlo")
                nombre = input("Ingrese el nombre o razon social del tercero (Obligatorio): ").strip()

    if direccion != "null":
        # Validar que sea un string

    if ciudad != "null":
        #Validar que sea un string

    if departamento != "null":
        #validar que sea un string

    if telefono != "null":
        #Validar que sea un string

    if email != "null":
        # Validar con una expresion regular que la estructura del correo sea valida "example@example.com"

    if naturaleza == "null":
        while True:
        
            if nombre != "null":
                break
            else:
                print("El nombre es obligatorio, vuelve a introducirlo")
                naturalesa = input("Ingrese la naturaleza (J= Juridica o N= Natural)(obligatorio)").strip()


    # Agregamos las variables al json que sera enviado a helisa para ser registrado

    nuevo_tercero = {
        "thirdParty": {
            "secondLastName": "Apellido2",
            "cree": false,
            "firstName": "Nombre2",
            "economicActivity": "1311",
            "city": "05001",
            "documentType": {
                "tag": "C"
            },
            "year": 2022,
            "nature": {
            "value": 0
            },
            "firstLastName": "Apellido1",
            "name": "Name No. 1",
            "id": "1038393061",
            "checkDigit": "",
            "regimen": {
                "tag": "S"
            },
            "secondName": "Nombre1",
            "userCode": 1,
            "telephones": "3234840257",
            "cellphone": "4954800",
            "email": "antoniobanderas@gmail.com",
            "address": "CALLE 45"
        }
    }

    # Convertimos a tipo json para enviar a helisa
    json_data = json.dumps(
            nuevo_tercero,
            separators=(",", ":")
        )

    print("\nJSON que se enviará:")
    print(json_data)


    # Insertamnos el domcumento
    response = POST(
        url,
        json_data
    )

    # Analisamos la respuesta
    if response is not None:

        print("\nCódigo:", response.status_code)

        print("Respuesta:")

        print(response.text)