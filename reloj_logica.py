import time
import datetime
import threading
from sounds.reproductor_sonidos import ReproductorSonidos

class RelojLogic:
    def __init__(self, lbl_hora, lbl_fecha, sound_path=None):
        self.lbl_hora = lbl_hora
        self.lbl_fecha = lbl_fecha
        self.sound_path = sound_path
        
        # 🔔 Alarmas y sonidos
        self.alarmas = []  # Lista de múltiples alarmas
        self.reproductor = ReproductorSonidos()
        
        # ⏱️ Cronómetro
        self.cronometro_corriendo = False
        self.cronometro_iniciado = False
        self.tiempo_inicial_crono = 0
        self.tiempo_pausado_crono = 0
        self.tiempo_actual_crono = 0
        self.vueltas = []  # Para registrar vueltas
        
        # ⏲️ Temporizador
        self.temporizador_corriendo = False
        self.tiempo_temporizador = 0
        self.tiempo_inicial_temp = 0
        
        # 🧵 Control de hilos
        self._reloj_activo = False
        self._hilo_cronometro = None
        self._hilo_temporizador = None
        
    # 🕒------------------- RELOJ -------------------🕒
    def iniciar_reloj(self):
        """Inicia el hilo del reloj si aún no está activo."""
        if not self._reloj_activo:
            self._reloj_activo = True
            threading.Thread(target=self._actualizar_reloj, daemon=True).start()
    
    def _actualizar_reloj(self):
        while self._reloj_activo:
            ahora = datetime.datetime.now()
            hora_texto = ahora.strftime("%H:%M:%S")
            fecha_texto = ahora.strftime("%A, %d de %B de %Y")
            
            # Actualiza etiquetas en Tkinter (thread-safe)
            try:
                self.lbl_hora.config(text=hora_texto)
                self.lbl_fecha.config(text=fecha_texto)
            except:
                pass
            
            # Verifica todas las alarmas
            for alarma in self.alarmas[:]:  # Copia para evitar problemas
                if alarma['activa'] and hora_texto.startswith(alarma['hora']):
                    print(f"🔔 Alarma activada a las {hora_texto}")
                    self.reproductor.reproducir("alarma")
                    alarma['activa'] = False  # Desactivar hasta el próximo día
            
            time.sleep(1)
    
    # ⏰------------------- ALARMAS -------------------⏰
    def agregar_alarma(self, hora, nombre="Alarma"):
        """Agrega una nueva alarma"""
        self.alarmas.append({
            'hora': hora.strip(),
            'nombre': nombre,
            'activa': True
        })
        return len(self.alarmas) - 1  # Retorna el índice
    
    def eliminar_alarma(self, indice):
        """Elimina una alarma por índice"""
        if 0 <= indice < len(self.alarmas):
            del self.alarmas[indice]
    
    def toggle_alarma(self, indice):
        """Activa/desactiva una alarma"""
        if 0 <= indice < len(self.alarmas):
            self.alarmas[indice]['activa'] = not self.alarmas[indice]['activa']
    
    def obtener_alarmas(self):
        """Retorna la lista de alarmas"""
        return self.alarmas
    
    # ⏱️------------------- CRONÓMETRO -------------------⏱️
    def sw_start(self):
        """Inicia o reanuda el cronómetro"""
        if not self.cronometro_corriendo:
            self.cronometro_corriendo = True
            
            if not self.cronometro_iniciado:
                # Primera vez que se inicia
                self.tiempo_inicial_crono = time.time()
                self.cronometro_iniciado = True
            else:
                # Reanudar después de pausa
                self.tiempo_inicial_crono = time.time() - self.tiempo_pausado_crono
            
            # Iniciar hilo del cronómetro
            if self._hilo_cronometro is None or not self._hilo_cronometro.is_alive():
                self._hilo_cronometro = threading.Thread(
                    target=self._actualizar_cronometro_interno, 
                    daemon=True
                )
                self._hilo_cronometro.start()
    
    def sw_pause(self):
        """Pausa el cronómetro"""
        if self.cronometro_corriendo:
            self.cronometro_corriendo = False
            self.tiempo_pausado_crono = time.time() - self.tiempo_inicial_crono
    
    def sw_reset(self):
        """Reinicia el cronómetro"""
        self.cronometro_corriendo = False
        self.cronometro_iniciado = False
        self.tiempo_inicial_crono = 0
        self.tiempo_pausado_crono = 0
        self.tiempo_actual_crono = 0
        self.vueltas = []
    
    def sw_vuelta(self):
        """Registra una vuelta/lap"""
        if self.cronometro_corriendo:
            tiempo_vuelta = self.obtener_tiempo_cronometro()
            self.vueltas.append({
                'numero': len(self.vueltas) + 1,
                'tiempo': tiempo_vuelta
            })
            return tiempo_vuelta
        return None
    
    def _actualizar_cronometro_interno(self):
        """Actualiza el cronómetro en un hilo separado"""
        while self.cronometro_corriendo:
            self.tiempo_actual_crono = time.time() - self.tiempo_inicial_crono
            time.sleep(0.01)
    
    def obtener_tiempo_cronometro(self):
        """Obtiene el tiempo actual del cronómetro formateado"""
        if self.cronometro_corriendo:
            tiempo = self.tiempo_actual_crono
        elif self.cronometro_iniciado:
            tiempo = self.tiempo_pausado_crono
        else:
            tiempo = 0
        
        horas = int(tiempo // 3600)
        minutos = int((tiempo % 3600) // 60)
        segundos = int(tiempo % 60)
        centesimas = int((tiempo % 1) * 100)
        
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}.{centesimas:02d}"
    
    def obtener_vueltas(self):
        """Retorna la lista de vueltas registradas"""
        return self.vueltas
    
    # ⏲️------------------- TEMPORIZADOR -------------------⏲️
    def temp_start(self, minutos, segundos):
        """Inicia el temporizador"""
        if not self.temporizador_corriendo:
            self.tiempo_temporizador = (minutos * 60) + segundos
            self.tiempo_inicial_temp = time.time()
            self.temporizador_corriendo = True
            
            # Iniciar hilo del temporizador
            if self._hilo_temporizador is None or not self._hilo_temporizador.is_alive():
                self._hilo_temporizador = threading.Thread(
                    target=self._actualizar_temporizador_interno,
                    daemon=True
                )
                self._hilo_temporizador.start()
    
    def temp_pause(self):
        """Pausa el temporizador"""
        if self.temporizador_corriendo:
            self.temporizador_corriendo = False
            tiempo_transcurrido = time.time() - self.tiempo_inicial_temp
            self.tiempo_temporizador -= int(tiempo_transcurrido)
    
    def temp_reset(self):
        """Reinicia el temporizador"""
        self.temporizador_corriendo = False
        self.tiempo_temporizador = 0
    
    def _actualizar_temporizador_interno(self):
        """Actualiza el temporizador en un hilo separado"""
        while self.temporizador_corriendo:
            tiempo_transcurrido = time.time() - self.tiempo_inicial_temp
            tiempo_restante = self.tiempo_temporizador - int(tiempo_transcurrido)
            
            if tiempo_restante <= 0:
                self.temporizador_corriendo = False
                self.tiempo_temporizador = 0
                # Reproducir sonido cuando termina
                self.reproductor.reproducir("alarma")
                break
            
            time.sleep(0.1)
    
    def obtener_tiempo_temporizador(self):
        """Obtiene el tiempo restante del temporizador"""
        if self.temporizador_corriendo:
            tiempo_transcurrido = time.time() - self.tiempo_inicial_temp
            tiempo_restante = max(0, self.tiempo_temporizador - int(tiempo_transcurrido))
        else:
            tiempo_restante = self.tiempo_temporizador
        
        minutos = int(tiempo_restante // 60)
        segundos = int(tiempo_restante % 60)
        
        return f"{minutos:02d}:{segundos:02d}"
    
    def temporizador_activo(self):
        """Verifica si el temporizador está corriendo"""
        return self.temporizador_corriendo