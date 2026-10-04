
import os
import time
import hmac
import hashlib
import requests

def generar_firma(key, timestamp):

    clave = bytes.fromhex(key)

    payload = str(timestamp)

    return hmac.new(
        clave,
        payload.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def main():
    CLIENT_ID = os.environ["HELIDA_CLIENT_ID"]
    KEY = os.environ["HELISA_API_KEY"]
    
    print(KEY)

    url = "https://webconektaorquestador.helisa.com/"
    
    date = int(time.time() * 1000)

    timestamp = int(time.time())

    signature = generar_firma(KEY, timestamp)

    headers = {
            "X-Conekta-Client-Id": CLIENT_ID,
            "X-Conekta-Timestamp": str(timestamp),
            "X-Conekta-Signature": signature
        }

    response = requests.get(
        url,
        headers=headers
    )

    print("Date:", date)
    print("Signature:", signature)
    print("Timestamp:", timestamp)
    print("Código:", response.status_code)
    print(response.text)



if __name__=="__main__":
    main()