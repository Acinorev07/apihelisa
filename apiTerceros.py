import os
import time
import hmac
import hashlib
import requests

import generar_firma


def generar_firma(key, payload):
    clave = bytes.fromhex(key)

    return hmac.new(
        clave,
        payload.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def main():

    client_id = os.environ["HELIDA_CLIENT_ID"]
    key = os.environ["HELISA_API_KEY"]

    url = (
        "https://webconektaorquestador.helisa.com"
        "/KansasWS/summary/thirdPartyFromAccount"
    )

    # Epoch en milisegundos
    date = int(time.time() * 1000)

    # IMPORTANTE:
    # La firma se calcula sobre ESTE STRING exacto.
    json_data = (
        '{"date":' + str(date) +
        ',"account":"41600501"}'
    )

    sign = generar_firma(key, json_data)

    params = {
        "json": json_data,
        "id": client_id,
        "sign": sign
    }

    response = requests.post(
        url,
        params=params
    )

    print("Código:", response.status_code)
    print("Respuesta:")
    print(response.text)


if __name__ == "__main__":
    main()