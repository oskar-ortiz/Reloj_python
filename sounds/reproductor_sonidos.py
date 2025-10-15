import os
import threading
from playsound import playsound


class ReproductorSonidos:
    def __init__(self):
        # Compatible con carpeta "sounds" o "sonidos"
        if os.path.exists("sounds"):
            self.ruta_base = "sounds"
        else:
            self.ruta_base = "sonidos"

    def reproducir(self, nombre):
        """Reproduce el sonido indicado (sin bloquear el hilo principal)."""
        nombre_archivo = f"{nombre}.mp3"
        ruta = os.path.join(self.ruta_base, nombre_archivo)

        if not os.path.exists(ruta):
            print(f"⚠️ No se encontró el archivo de sonidos: {ruta}")
            return

        try:
            # Usa threading para no bloquear el programa
            threading.Thread(target=lambda: playsound(ruta), daemon=True).start()
        except Exception as e:
            print(f"❌ Error al reproducir {ruta}: {e}")