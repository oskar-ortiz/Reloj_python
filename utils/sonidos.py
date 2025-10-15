import threading
from playsound import playsound
import os

class ReproductorSonidos:
    def __init__(self):
        self.ruta_base = os.path.join(os.path.dirname(__file__), "sounds")

    def reproducir(self, nombre_sonido):
        """
        Reproduce el archivo MP3 dentro de la carpeta 'sounds' en un hilo aparte.
        """
        ruta_sonido = os.path.join(self.ruta_base, f"{nombre_sonido}.mp3")
        if os.path.exists(ruta_sonido):
            threading.Thread(target=lambda: playsound(ruta_sonido)).start()
        else:
            print(f"⚠️ No se encontró el sonido: {ruta_sonido}")
