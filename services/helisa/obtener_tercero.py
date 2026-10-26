from hooks.configuracion_APIs import obtener_url
from datetime import datetime
from hooks.date import dateMillisec
from hooks.validarDi import validar_documento_tercero
from api.helisa.route import GET_TERCERO
import json

def obtener_tercero(fecha, docId):

    url = obtener_url(
            "helisa",
            "thirdParty2_0"
        )

        # Interpretar la fecha
    if fecha:
        try:
            fecha_seleccionada = datetime.strptime(
                fecha, "%Y-%m-%d"
            )
        except ValueError:
            print("Fecha inválida. Utiliza el formato YYYY-MM-DD.")
            raise SystemExit(1)
    else:
        fecha_seleccionada = datetime.now()

    # Extraer el año para consultar Helisa
    year = fecha_seleccionada.year

    print("Año de consulta:", year)


    date = dateMillisec(fecha)

    # Documento de identidad del tercero
    di = validar_documento_tercero(docId)

        

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
     
        return response

        
        