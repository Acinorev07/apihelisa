from api.helisa.route import GET_TERCERO
from hooks.configuracion_APIs import obtener_url
from hooks.date import dateMillisec
from datetime import datetime
# import generar_firma

def main():

    
    url = obtener_url(
        "helisa",
        "thirdParty2_0"
    )

    parametros = {
        "Fecha_inicio": "2026-10-23",
        "Fecha_fin": "2026-10-23",
        "di":"1097780022"
    }

    fecha = parametros["Fecha_inicio"]
    di = parametros["di"]
    year = datetime.strptime(fecha, "%Y-%m-%d").year
    date = dateMillisec(fecha)


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
            
             print(response.json())
        
        except ValueError:
            print(response.text)


if __name__ == "__main__":
    main()