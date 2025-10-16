"""
reloj_logica.py
Lógica del reloj: alarmas, cronómetro y temporizador.
La clase acepta un callback opcional 'on_alarm' que la interfaz proporcionará
para mostrar notificaciones/sonido cuando salte una alarma.
"""
import time
import datetime
import threading
import pytz

class LogicaRelojPro:
    def __init__(self, on_alarm_callback=None):
        self.on_alarm = on_alarm_callback

        # Alarmas: lista de dicts {hora: int, minuto: int, nombre: str, repetir: bool, activa: bool}
        self.alarmas = []

        # Iniciar hilo verificador de alarmas
        self._stop_alarm_thread = False
        self._alarm_thread = threading.Thread(target=self._verificar_alarmas_loop, daemon=True)
        self._alarm_thread.start()

        # Cronómetro
        self.cronometro_iniciado = False
        self.cronometro_corriendo = False
        self._crono_start = 0.0
        self._crono_acumulado = 0.0
        self.vueltas = []

        # Temporizador
        self.temporizador_segundos = 0
        self.temporizador_corriendo = False

    # ------------------ ALARMAS ------------------
    def agregar_alarma(self, hora: int, minuto: int, nombre: str = "Alarma", repetir: bool = False):
        if not (0 <= hora <= 23 and 0 <= minuto <= 59):
            raise ValueError("Hora o minuto fuera de rango")
        self.alarmas.append({
            "hora": int(hora),
            "minuto": int(minuto),
            "nombre": str(nombre),
            "repetir": bool(repetir),
            "activa": True
        })

    def eliminar_alarma(self, indice: int):
        if 0 <= indice < len(self.alarmas):
            self.alarmas.pop(indice)

    def obtener_alarmas(self):
        return list(self.alarmas)

    def _verificar_alarmas_loop(self):
        """Hilo que revisa cada 10s si hay alarmas que disparar.
           Se compara por hora y minuto (sin requerir segundos exactos)."""
        last_checked_minute = None
        while not self._stop_alarm_thread:
            ahora = datetime.datetime.now()
            hm = (ahora.hour, ahora.minute)
            if hm != last_checked_minute:
                last_checked_minute = hm
                # comprobar alarmas
                for alarma in list(self.alarmas):  # copia para poder modificar
                    if alarma["activa"] and alarma["hora"] == ahora.hour and alarma["minuto"] == ahora.minute:
                        # disparar alarma
                        if self.on_alarm:
                            try:
                                self.on_alarm(alarma)  # interfaz puede mostrar popup/sonar
                            except Exception:
                                pass
                        # si no repetir, desactivar
                        if not alarma.get("repetir", False):
                            alarma["activa"] = False
            time.sleep(6)

    def stop(self):
        self._stop_alarm_thread = True

    # ------------------ CRONÓMETRO ------------------
    def crono_start(self):
        if not self.cronometro_iniciado:
            self._crono_start = time.perf_counter()
            self.cronometro_iniciado = True
            self._crono_acumulado = 0.0
        elif not self.cronometro_corriendo:
            # reanudar
            self._crono_start = time.perf_counter() - self._crono_acumulado
        self.cronometro_corriendo = True

    def crono_pause(self):
        if self.cronometro_corriendo:
            self._crono_acumulado = time.perf_counter() - self._crono_start
            self.cronometro_corriendo = False

    def crono_reset(self):
        self.cronometro_iniciado = False
        self.cronometro_corriendo = False
        self._crono_start = 0.0
        self._crono_acumulado = 0.0
        self.vueltas.clear()

    def crono_vuelta(self):
        t = self.obtener_tiempo_cronometro()
        if t:
            self.vueltas.append(t)
            return t
        return None

    def obtener_vueltas(self):
        return list(self.vueltas)

    def obtener_tiempo_cronometro(self):
        if self.cronometro_corriendo:
            elapsed = time.perf_counter() - self._crono_start
        elif self.cronometro_iniciado:
            elapsed = self._crono_acumulado
        else:
            elapsed = 0.0
        horas, resto = divmod(elapsed, 3600)
        minutos, segundos = divmod(resto, 60)
        centesimas = int((segundos - int(segundos)) * 100)
        return f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}.{centesimas:02}"

    # ------------------ TEMPORIZADOR ------------------
    def iniciar_temporizador(self, segundos: int):
        if segundos <= 0:
            raise ValueError("El temporizador debe ser mayor a 0")
        self.temporizador_segundos = int(segundos)
        if not self.temporizador_corriendo:
            self.temporizador_corriendo = True
            threading.Thread(target=self._run_temporizador, daemon=True).start()

    def _run_temporizador(self):
        while self.temporizador_corriendo and self.temporizador_segundos > 0:
            time.sleep(1)
            self.temporizador_segundos -= 1
        if self.temporizador_segundos <= 0:
            # trigger
            if self.on_alarm:
                try:
                    self.on_alarm({"nombre": "Temporizador", "hora": None, "minuto": None, "repetir": False})
                except Exception:
                    pass
        self.temporizador_corriendo = False

    def detener_temporizador(self):
        self.temporizador_corriendo = False

    def obtener_tiempo_temporizador(self):
        s = max(0, int(self.temporizador_segundos))
        h, r = divmod(s, 3600)
        m, ss = divmod(r, 60)
        return f"{int(h):02}:{int(m):02}:{int(ss):02}"
