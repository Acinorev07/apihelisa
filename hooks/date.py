# apihelisa/hooks/date.py
import time as t
from datetime import datetime


def dateMillisec(fecha=None):

    if fecha is None or fecha == "":
        return int(t.time() * 1000)

    fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")

    return int(fecha_obj.timestamp() * 1000)
