import hmac
import hashlib

def generar_firma(key, payload):
    clave = bytes.fromhex(key)

    return hmac.new(
        clave,
        payload.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()