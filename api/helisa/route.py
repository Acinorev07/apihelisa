from repositorio.helisa import post
from repositorio.helisa import get
from hooks.generarFirma import generar_firma
import os 



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

