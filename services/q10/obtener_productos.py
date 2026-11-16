
from hooks.configuracion_APIs import obtener_url
from hooks.procesar_respuesta_helisa import procesar_respuesta_helisa
from api.q10.route import GET


def obtener_productos(params=None):

    try:
        # 1. Obtener URL
        url = obtener_url(
            "q10",
            "obtener_productos"
        )

        if not url:
            return {
                "ok": False,
                "status": 500,
                "mensaje": "No se encontró la URL para obtener productos."
            }

        # 2. Preparar parámetros
        params = params or {}

        estado = str(params.get("Estado", "true")).strip().lower()
        limite = params.get("Limit", 100)
        offset = params.get("Offset", 0)

        # 3. Validar estado
        if estado not in ("true", "false"):
            return {
                "ok": False,
                "status": 422,
                "mensaje": "El estado debe ser true o false."
            }

        # 4. Validar límite y offset
        try:
            limite = int(limite) if str(limite).strip() else 100
            offset = int(offset) if str(offset).strip() else 0

        except (ValueError, TypeError):
            return {
                "ok": False,
                "status": 422,
                "mensaje": "El límite y el offset deben ser números enteros."
            }

        if not 1 <= limite <= 5000:
            return {
                "ok": False,
                "status": 422,
                "mensaje": "El límite debe estar entre 1 y 5000."
            }

        if offset < 0:
            return {
                "ok": False,
                "status": 422,
                "mensaje": "El offset no puede ser negativo."
            }

        # 5. Construir parámetros definitivos
        parametros = {
            "Estado": estado,
            "Limit": limite,
            "Offset": offset
        }

        print(f"\nParámetros enviados a Q10: {parametros}")

        # 6. Consultar API
        response = GET(
            url,
            params=parametros
        )

        if response is None:
            return {
                "ok": False,
                "status": 502,
                "mensaje": "No se recibió respuesta de Q10."
            }

        # 7. Procesar respuesta HTTP
        resultado_http = procesar_respuesta_helisa(response)

        if resultado_http["ok"]:

            print(
                f"Q10 respondió HTTP {resultado_http['status']}"
            )

            return {
                "ok": True,
                "status": resultado_http["status"],
                "respuesta": resultado_http["respuesta"]
            }

        # 8. Extraer el mensaje de error de Q10
        contenido = resultado_http.get("respuesta")

        if isinstance(contenido, dict):
            mensaje = contenido.get(
                "message",
                contenido.get("mensaje", "Error desconocido de Q10.")
            )
        else:
            mensaje = resultado_http.get(
                "mensaje",
                str(contenido or "Error desconocido de Q10.")
            )

        return {
            "ok": False,
            "status": resultado_http["status"],
            "mensaje": mensaje,
            "respuesta": contenido
        }

    except Exception as e:
        return {
            "ok": False,
            "status": 500,
            "mensaje": f"Error al consultar los productos: {str(e)}"
        }


