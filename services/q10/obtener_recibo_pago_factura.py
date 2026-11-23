from hooks.configuracion_APIs import obtener_url
from api.q10.route import GET


def obtener_recibo_pago_factura(id_pago):

    url = obtener_url(
        "q10",
        "detalle_pago_factura"
    )

    print(f"url: {url}")

    

    url_enviar = url.format(id=int(id_pago))

    print(f"url: {url_enviar}")

    response = GET(url_enviar)

    return response.json()