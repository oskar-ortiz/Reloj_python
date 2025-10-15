
import time
from datetime import datetime

class Reloj:
    """Clase con utilidades de tiempo."""
    @staticmethod
    def ahora():
        return datetime.now()

    @staticmethod
    def hora_str(dt=None):
        if dt is None:
            dt = Reloj.ahora()
        return dt.strftime('%H:%M:%S')

    @staticmethod
    def hora_digital_12h(dt=None):
        if dt is None:
            dt = Reloj.ahora()
        return dt.strftime('%I:%M:%S %p')
