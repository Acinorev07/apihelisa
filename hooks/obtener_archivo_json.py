import json
from pathlib import Path


# Raíz del proyecto: carpeta apihelisa
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

# Archivo que contiene las URL
# ARCHIVO_CONFIG = RAIZ_PROYECTO / "api" / "dataFEq10.json"


def cargar_archivo(archivo =""):

    """Lee la configuración de puntos de acceso."""

    if archivo == "":
        ARCHIVO_CONFIG = (
            RAIZ_PROYECTO / "api" / "dataFEq10.json"
        )
    else:
        ARCHIVO_CONFIG = (
            RAIZ_PROYECTO / "api" / str(archivo).strip()
        )

    with ARCHIVO_CONFIG.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


