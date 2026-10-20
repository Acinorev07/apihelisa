
from repositorio.llamadas import get
import os
from dotenv import load_dotenv


def GET(url, params=None):
    try:
        load_dotenv()
        api_key = os.getenv("Q10_KEY")

        if not api_key:
            raise RuntimeError(
                "No se encontró la variable Q10_KEY."
            )

        headers = {
            "Accept": "application/json",
            "Api-Key": api_key,
        }

        response = get(
            url,
            headers=headers,
            params=params,
        )

        return response

    except Exception as e:
        print(f"\nError en la ejecución: {e}")
        return None
