
import json
from pathlib import Path


# Raíz del proyecto: carpeta apihelisa
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

# Archivo que contiene las URL
ARCHIVO_CONFIG = RAIZ_PROYECTO / "api" / "punto_acceso.json"


def cargar_configuracion():
    """Lee la configuración de puntos de acceso."""
    with ARCHIVO_CONFIG.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def obtener_url(servicio, punto_acceso):
    """Construye la URL de un punto de acceso."""
    config = cargar_configuracion()

    raiz = config["url_raiz"][servicio].rstrip("/")
    ruta = config["puntos_acceso"][servicio][punto_acceso].strip("/")

    return f"{raiz}/{ruta}"
