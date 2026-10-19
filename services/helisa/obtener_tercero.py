from hooks.configuracion_APIs import obtener_url
from datetime import datetime
from hooks.date import dateMillisec
from hooks.validarDi import validar_documento_tercero
from api.helisa.route import GET_TERCERO
import json

def obtener_tercero():

    url = obtener_url(
            "helisa",
            "thirdParty2_0"
        )
    fecha_consulta = input(
        "Fecha de consulta (DD-MM-YYYY, ENTER = hoy): "
    ).strip()

        # Interpretar la fecha
    if fecha_consulta:
        try:
            fecha_seleccionada = datetime.strptime(
                fecha_consulta, "%d-%m-%Y"
            )
        except ValueError:
            print("Fecha inválida. Utiliza el formato DD-MM-YYYY.")
            raise SystemExit(1)
    else:
        fecha_seleccionada = datetime.now()

    # Extraer el año para consultar Helisa
    year = fecha_seleccionada.year

    print("Año de consulta:", year)


    date = dateMillisec(fecha_consulta)

    # Documento de identidad del tercero
    di = validar_documento_tercero(
        "Introduce el NIT del proveedor: "
    )

        

    payload = f"{year}|{di}|{date}"

    response = GET_TERCERO(
        url, 
        payload,
        year,
        di,
        date
        )
            
    if response is not None:
        print("\nCódigo HTTP:", response.status_code)
        print("\nRespuesta de Helisa:")

        try:
            
             return json.dumps(
                    response.json(),
                    indent=4,
                    ensure_ascii=False,
                )
        
        except ValueError:
            print(response.text)