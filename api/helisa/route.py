from repositorio.llamadas import post
from repositorio.llamadas import get
from hooks.generarFirma import generar_firma
import os 
from dotenv import load_dotenv


def GET(url, date=None):

    load_dotenv()

    try:
        # Obtener las credenciales desde el archivo .env
        key = os.environ["HELISA_API_KEY"]
        client_id = os.environ["HELISA_CLIENT_ID"]

        # Helisa exige firmar el valor de date como texto.
        # Si date no existe, el payload debe ser literalmente "null".
        payload = str(date) if date is not None else "null"

        sign = generar_firma(
            key,
            payload
        )

        # Parámetros que se enviarán en la URL
        params = {
            "id": client_id,
            "sign": sign
        }

        # Solo enviar date si tiene un valor.
        if date is not None:
            params["date"] = str(date)

        # Ejecutar la petición y conservar la respuesta.
        response = get(
            url,
            params=params
        )

        return response

    except KeyError as e:
        print(f"Error: falta una variable de entorno: {e}")
        return None

    except Exception as e:
        print(f"\nError en la ejecución: {e}")
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