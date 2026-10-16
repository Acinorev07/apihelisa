from repositorio.helisa import post
from repositorio.helisa import get
from hooks.generarFirma import generar_firma
import os 
from dotenv import load_dotenv


def GET(url):

    key = os.environ["HELISA_API_KEY"]
    connection_id = os.environ["HELISA_CONNECTION_ID"]

    try:


       get(url)



    except Exception as e:
        print(f"\nError en la ejecución: {str(e)}")
        return None



def POST(url, json_data):



    try:

        # Busca el archivo .env desde la raíz del proyecto
        load_dotenv()  
        
        key = os.environ["HELISA_API_KEY"]
        client_id = os.environ["HELISA_CLIENT_ID"]

        sign = generar_firma(
            key,
            json_data
        )
        params = {
            "json": json_data,
            "id": client_id,
            "sign": sign
        }

        response = post(
            url,
            params=params
        )

        return response

    except Exception as e:
        print(f"\nError en la ejecución: {str(e)}")
        return None



def GET_TERCERO(url, payload, year, di, date):



    try:

        # Busca el archivo .env desde la raíz del proyecto
        load_dotenv()  
        
        key = os.environ["HELISA_API_KEY"]
        client_id = os.environ["HELISA_CLIENT_ID"]

        sign = generar_firma(
            key,
            payload
        )
        params = {
            "year": year,
            "identity": di,
            "id": client_id,
            "date": date,
            "sign": sign
        }

        response = post(
            url,
            params=params
        )

       # Si Helisa devuelve un error HTTP, lo mostramos.
        response.raise_for_status()

        return response

    except (KeyError, ValueError) as e:
        print(f"Error de configuración o datos: {e}")
        return None