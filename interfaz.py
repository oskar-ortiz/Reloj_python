import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from reloj_logica import RelojLogic
from interfaz_estilos import EstiloApp

class InterfazReloj:
    def __init__(self, root, sound_path=None, tema_inicial="darkly"):
        self.root = root
        self.sound_path = sound_path
        self.logic = None
        self.modo_actual = "reloj"
        self.actualizando_cronometro = False
        self.actualizando_temporizador = False
        
        # Inicializar sistema de estilos
        self.estilos = EstiloApp(root, tema_inicial)
        
    def crear_marcas_hora(self, lbl_hora, lbl_fecha):
        """Crea la interfaz completa profesional"""
        self.lbl_hora = lbl_hora
        self.lbl_fecha = lbl_fecha
        
        # Crear la lógica del reloj
        self.logic = RelojLogic(self.lbl_hora, self.lbl_fecha, sound_path=self.sound_path)
        self.logic.iniciar_reloj()
        
        # Crear indicador de estado
        self.crear_indicador_estado()
        
        # Separador decorativo superior
        sep1 = self.estilos.crear_separador_elegante(self.root)
        sep1.pack(fill='x', padx=40, pady=(5, 15))
        
        # Panel de controles principales
        self.crear_panel_controles()
        
        # Separador entre secciones
        sep2 = self.estilos.crear_separador_elegante(self.root)
        sep2.pack(fill='x', padx=40, pady=15)
        
        # Panels (inicialmente ocultos)
        self.crear_panel_cronometro()
        self.crear_panel_temporizador()
        self.crear_panel_alarmas()
        
        # Footer con información
        self.crear_footer()
    
    def crear_indicador_estado(self):
        """Crea el indicador visual de estado"""
        frame_estado = tk.Frame(self.root, bg=self.estilos.colores['bg_primary'])
        frame_estado.pack(pady=(5, 10))
        
        self.badge_estado = self.estilos.crear_badge(frame_estado, "● RELOJ ACTIVO", tipo='success')
        self.badge_estado.pack()
    
    def crear_panel_controles(self):
        """Crea el panel principal de controles"""
        card = self.estilos.crear_card_moderna(self.root, padding=25)
        card.pack(pady=10, padx=30, fill='x')
        
        # Header del panel
        frame_header = tk.Frame(card, bg=self.estilos.colores['bg_card'])
        frame_header.pack(fill='x', pady=(0, 20))
        
        titulo_frame = self.estilos.crear_titulo_seccion(frame_header, "⚡ PANEL DE CONTROL")
        titulo_frame.pack(side='left', fill='x', expand=True)
        
        # Grid de botones 2x2
        frame_btns = tk.Frame(card, bg=self.estilos.colores['bg_card'])
        frame_btns.pack(pady=10, fill='x', padx=10)
        
        # Fila 1
        self.btn_alarma = self.estilos.crear_boton_premium(
            frame_btns, "Alarmas", self.toggle_alarmas, variant='primary', icon='⏰'
        )
        self.btn_alarma.grid(row=0, column=0, padx=8, pady=8, sticky='ew')
        
        self.btn_cronometro = self.estilos.crear_boton_premium(
            frame_btns, "Cronómetro", self.toggle_cronometro, variant='success', icon='⏱️'
        )
        self.btn_cronometro.grid(row=0, column=1, padx=8, pady=8, sticky='ew')
        
        # Fila 2
        self.btn_temporizador = self.estilos.crear_boton_premium(
            frame_btns, "Temporizador", self.toggle_temporizador, variant='warning', icon='⏲️'
        )
        self.btn_temporizador.grid(row=1, column=0, padx=8, pady=8, sticky='ew')
        
        self.btn_hora = self.estilos.crear_boton_premium(
            frame_btns, "Ver Reloj", self.mostrar_reloj, variant='dark', icon='🕐'
        )
        self.btn_hora.grid(row=1, column=1, padx=8, pady=8, sticky='ew')
        
        # Hacer columnas uniformes
        frame_btns.grid_columnconfigure(0, weight=1)
        frame_btns.grid_columnconfigure(1, weight=1)
    
    # ═══════════════════════════════════════════════════════
    # PANEL CRONÓMETRO
    # ═══════════════════════════════════════════════════════
    def crear_panel_cronometro(self):
        """Crea el panel del cronómetro mejorado"""
        self.card_crono = self.estilos.crear_card_moderna(self.root, padding=30)
        
        # Header
        frame_header = tk.Frame(self.card_crono, bg=self.estilos.colores['bg_card'])
        frame_header.pack(fill='x', pady=(0, 20))
        
        titulo_frame = self.estilos.crear_titulo_seccion(
            frame_header, "⏱️ CRONÓMETRO DE PRECISIÓN", color='#10b981'
        )
        titulo_frame.pack(side='left', fill='x', expand=True)
        
        self.badge_crono = self.estilos.crear_badge(frame_header, "DETENIDO", tipo='secondary')
        self.badge_crono.pack(side='right')
        
        # Display grande del cronómetro
        frame_display = tk.Frame(
            self.card_crono, bg='#0a0e1a',
            highlightthickness=3, highlightbackground='#10b981'
        )
        frame_display.pack(pady=20, padx=20, fill='x')
        
        self.lbl_cronometro = tk.Label(
            frame_display, text="00:00:00.00",
            font=("Consolas", 56, "bold"), bg='#0a0e1a', fg='#10b981', pady=25
        )
        self.lbl_cronometro.pack()
        
        # Botones de control
        frame_btns = tk.Frame(self.card_crono, bg=self.estilos.colores['bg_card'])
        frame_btns.pack(pady=15)
        
        self.btn_crono_iniciar = self.estilos.crear_boton_premium(
            frame_btns, "Iniciar", self.iniciar_cronometro, variant='success', icon='▶'
        )
        self.btn_crono_iniciar.pack(side='left', padx=8, ipadx=15)
        
        self.btn_crono_pausar = self.estilos.crear_boton_premium(
            frame_btns, "Pausar", self.pausar_cronometro, variant='warning', icon='⏸'
        )
        self.btn_crono_pausar.pack(side='left', padx=8, ipadx=15)
        self.btn_crono_pausar.configure(state='disabled')
        
        self.btn_crono_vuelta = self.estilos.crear_boton_premium(
            frame_btns, "Vuelta", self.vuelta_cronometro, variant='info', icon='🔄'
        )
        self.btn_crono_vuelta.pack(side='left', padx=8, ipadx=15)
        self.btn_crono_vuelta.configure(state='disabled')
        
        self.btn_crono_reiniciar = self.estilos.crear_boton_premium(
            frame_btns, "Reiniciar", self.reiniciar_cronometro, variant='danger', icon='⟲'
        )
        self.btn_crono_reiniciar.pack(side='left', padx=8, ipadx=15)
        
        # Lista de vueltas
        sep = self.estilos.crear_separador_con_texto(self.card_crono, "VUELTAS REGISTRADAS")
        sep.pack(fill='x', padx=20, pady=15)
        
        frame_vueltas = tk.Frame(self.card_crono, bg=self.estilos.colores['bg_card'])
        frame_vueltas.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Scrollbar y lista
        scrollbar = ttk.Scrollbar(frame_vueltas, bootstyle="success-round")
        scrollbar.pack(side='right', fill='y')
        
        self.lista_vueltas = tk.Listbox(
            frame_vueltas, bg='#0a0e1a', fg='#10b981',
            font=("Consolas", 11), height=5, bd=0, highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.lista_vueltas.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.lista_vueltas.yview)
    
    def iniciar_cronometro(self):
        """Inicia el cronómetro"""
        self.logic.sw_start()
        self.btn_crono_iniciar.configure(state='disabled')
        self.btn_crono_pausar.configure(state='normal')
        self.btn_crono_vuelta.configure(state='normal')
        self.badge_crono.configure(text="EN MARCHA", bg=self.estilos.colores['success'])
        self.actualizando_cronometro = True
        self.actualizar_display_cronometro()
    
    def pausar_cronometro(self):
        """Pausa el cronómetro"""
        self.logic.sw_pause()
        self.btn_crono_iniciar.configure(state='normal', text="▶ Reanudar")
        self.btn_crono_pausar.configure(state='disabled')
        self.btn_crono_vuelta.configure(state='disabled')
        self.badge_crono.configure(text="PAUSADO", bg=self.estilos.colores['warning'])
        self.actualizando_cronometro = False
    
    def vuelta_cronometro(self):
        """Registra una vuelta"""
        tiempo_vuelta = self.logic.sw_vuelta()
        if tiempo_vuelta:
            vueltas = self.logic.obtener_vueltas()
            self.lista_vueltas.insert('end', f"Vuelta {len(vueltas)}: {tiempo_vuelta}")
            self.lista_vueltas.see('end')
    
    def reiniciar_cronometro(self):
        """Reinicia el cronómetro"""
        self.logic.sw_reset()
        self.btn_crono_iniciar.configure(state='normal', text="▶ Iniciar")
        self.btn_crono_pausar.configure(state='disabled')
        self.btn_crono_vuelta.configure(state='disabled')
        self.badge_crono.configure(text="DETENIDO", bg=self.estilos.colores['text_secondary'])
        self.lbl_cronometro.config(text="00:00:00.00")
        self.lista_vueltas.delete(0, 'end')
        self.actualizando_cronometro = False
    
    def actualizar_display_cronometro(self):
        """Actualiza el display del cronómetro"""
        if self.actualizando_cronometro and self.logic.cronometro_corriendo:
            tiempo = self.logic.obtener_tiempo_cronometro()
            self.lbl_cronometro.config(text=tiempo)
            self.root.after(10, self.actualizar_display_cronometro)
    
    # ═══════════════════════════════════════════════════════
    # PANEL TEMPORIZADOR
    # ═══════════════════════════════════════════════════════
    def crear_panel_temporizador(self):
        """Crea el panel del temporizador"""
        self.card_temp = self.estilos.crear_card_moderna(self.root, padding=30)
        
        # Header
        frame_header = tk.Frame(self.card_temp, bg=self.estilos.colores['bg_card'])
        frame_header.pack(fill='x', pady=(0, 20))
        
        titulo_frame = self.estilos.crear_titulo_seccion(
            frame_header, "⏲️ TEMPORIZADOR", color='#f59e0b'
        )
        titulo_frame.pack(side='left', fill='x', expand=True)
        
        self.badge_temp = self.estilos.crear_badge(frame_header, "DETENIDO", tipo='secondary')
        self.badge_temp.pack(side='right')
        
        # Display del temporizador
        frame_display = tk.Frame(
            self.card_temp, bg='#0a0e1a',
            highlightthickness=3, highlightbackground='#f59e0b'
        )
        frame_display.pack(pady=20, padx=20, fill='x')
        
        self.lbl_temporizador = tk.Label(
            frame_display, text="00:00",
            font=("Consolas", 56, "bold"), bg='#0a0e1a', fg='#f59e0b', pady=25
        )
        self.lbl_temporizador.pack()
        
        # Configuración de tiempo
        frame_config = tk.Frame(self.card_temp, bg=self.estilos.colores['bg_card'])
        frame_config.pack(pady=15)
        
        tk.Label(
            frame_config, text="Minutos:", font=("Segoe UI", 11),
            bg=self.estilos.colores['bg_card'], fg=self.estilos.colores['text_secondary']
        ).grid(row=0, column=0, padx=10)
        
        self.spin_minutos = ttk.Spinbox(
            frame_config, from_=0, to=59, width=8, font=("Consolas", 14), bootstyle="warning"
        )
        self.spin_minutos.set(5)
        self.spin_minutos.grid(row=0, column=1, padx=10)
        
        tk.Label(
            frame_config, text="Segundos:", font=("Segoe UI", 11),
            bg=self.estilos.colores['bg_card'], fg=self.estilos.colores['text_secondary']
        ).grid(row=0, column=2, padx=10)
        
        self.spin_segundos = ttk.Spinbox(
            frame_config, from_=0, to=59, width=8, font=("Consolas", 14), bootstyle="warning"
        )
        self.spin_segundos.set(0)
        self.spin_segundos.grid(row=0, column=3, padx=10)
        
        # Botones
        frame_btns = tk.Frame(self.card_temp, bg=self.estilos.colores['bg_card'])
        frame_btns.pack(pady=15)
        
        self.btn_temp_iniciar = self.estilos.crear_boton_premium(
            frame_btns, "Iniciar", self.iniciar_temporizador, variant='warning', icon='▶'
        )
        self.btn_temp_iniciar.pack(side='left', padx=8, ipadx=15)
        
        self.btn_temp_pausar = self.estilos.crear_boton_premium(
            frame_btns, "Pausar", self.pausar_temporizador, variant='secondary', icon='⏸'
        )
        self.btn_temp_pausar.pack(side='left', padx=8, ipadx=15)
        self.btn_temp_pausar.configure(state='disabled')
        
        self.btn_temp_reiniciar = self.estilos.crear_boton_premium(
            frame_btns, "Reiniciar", self.reiniciar_temporizador, variant='danger', icon='⟲'
        )
        self.btn_temp_reiniciar.pack(side='left', padx=8, ipadx=15)
    
    def iniciar_temporizador(self):
        """Inicia el temporizador"""
        minutos = int(self.spin_minutos.get())
        segundos = int(self.spin_segundos.get())
        
        if minutos == 0 and segundos == 0:
            messagebox.showwarning("Temporizador", "Configura un tiempo mayor a 0")
            return
        
        self.logic.temp_start(minutos, segundos)
        self.btn_temp_iniciar.configure(state='disabled')
        self.btn_temp_pausar.configure(state='normal')
        self.spin_minutos.configure(state='disabled')
        self.spin_segundos.configure(state='disabled')
        self.badge_temp.configure(text="EN MARCHA", bg=self.estilos.colores['warning'])
        self.actualizando_temporizador = True
        self.actualizar_display_temporizador()
    
    def pausar_temporizador(self):
        """Pausa el temporizador"""
        self.logic.temp_pause()
        self.btn_temp_iniciar.configure(state='normal')
        self.btn_temp_pausar.configure(state='disabled')
        self.badge_temp.configure(text="PAUSADO", bg=self.estilos.colores['text_secondary'])
        self.actualizando_temporizador = False
    
    def reiniciar_temporizador(self):
        """Reinicia el temporizador"""
        self.logic.temp_reset()
        self.btn_temp_iniciar.configure(state='normal')
        self.btn_temp_pausar.configure(state='disabled')
        self.spin_minutos.configure(state='normal')
        self.spin_segundos.configure(state='normal')
        self.badge_temp.configure(text="DETENIDO", bg=self.estilos.colores['text_secondary'])
        self.lbl_temporizador.config(text="00:00")
        self.actualizando_temporizador = False
    
    def actualizar_display_temporizador(self):
        """Actualiza el display del temporizador"""
        if self.actualizando_temporizador and self.logic.temporizador_activo():
            tiempo = self.logic.obtener_tiempo_temporizador()
            self.lbl_temporizador.config(text=tiempo)
            self.root.after(100, self.actualizar_display_temporizador)
        elif self.actualizando_temporizador:
            # Terminó el temporizador
            self.lbl_temporizador.config(text="00:00")
            self.badge_temp.configure(text="¡TERMINADO!", bg=self.estilos.colores['danger'])
            self.btn_temp_iniciar.configure(state='normal')
            self.btn_temp_pausar.configure(state='disabled')
            self.spin_minutos.configure(state='normal')
            self.spin_segundos.configure(state='normal')
            self.actualizando_temporizador = False
            messagebox.showinfo("⏲️ Temporizador", "¡El tiempo ha terminado!")
    
    # ═══════════════════════════════════════════════════════
    # PANEL ALARMAS
    # ═══════════════════════════════════════════════════════
    def crear_panel_alarmas(self):
        """Crea el panel de alarmas"""
        self.card_alarmas = self.estilos.crear_card_moderna(self.root, padding=30)
        
        # Header
        frame_header = tk.Frame(self.card_alarmas, bg=self.estilos.colores['bg_card'])
        frame_header.pack(fill='x', pady=(0, 20))
        
        titulo_frame = self.estilos.crear_titulo_seccion(
            frame_header, "⏰ GESTOR DE ALARMAS", color='#00d4ff'
        )
        titulo_frame.pack(side='left', fill='x', expand=True)
        
        btn_nueva = self.estilos.crear_boton_premium(
            frame_header, "Nueva", self.agregar_alarma_dialog, variant='primary', icon='+'
        )
        btn_nueva.pack(side='right')
        
        # Lista de alarmas
        frame_lista = tk.Frame(self.card_alarmas, bg=self.estilos.colores['bg_card'])
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_lista, bootstyle="info-round")
        scrollbar.pack(side='right', fill='y')
        
        self.lista_alarmas = tk.Listbox(
            frame_lista, bg='#0a0e1a', fg='#00d4ff',
            font=("Segoe UI", 12), height=6, bd=0, highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.lista_alarmas.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.lista_alarmas.yview)
        
        # Botones de gestión
        frame_btns = tk.Frame(self.card_alarmas, bg=self.estilos.colores['bg_card'])
        frame_btns.pack(pady=10)
        
        self.btn_eliminar_alarma = self.estilos.crear_boton_premium(
            frame_btns, "Eliminar", self.eliminar_alarma, variant='danger', icon='🗑️'
        )
        self.btn_eliminar_alarma.pack(side='left', padx=5)
        
        self.actualizar_lista_alarmas()
    
    def agregar_alarma_dialog(self):
        """Muestra el diálogo para agregar alarma"""
        ventana = tk.Toplevel(self.root)
        ventana.title("⏰ Nueva Alarma")
        ventana.geometry("450x300")
        ventana.configure(bg=self.estilos.colores['bg_primary'])
        ventana.resizable(False, False)
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Centrar
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - 225
        y = (ventana.winfo_screenheight() // 2) - 150
        ventana.geometry(f"450x300+{x}+{y}")
        
        tk.Label(
            ventana, text="⏰", font=("Segoe UI", 48),
            bg=self.estilos.colores['bg_primary'], fg=self.estilos.colores['accent_cyan']
        ).pack(pady=20)
        
        tk.Label(
            ventana, text="NUEVA ALARMA", font=("Segoe UI", 18, "bold"),
            bg=self.estilos.colores['bg_primary'], fg=self.estilos.colores['text_primary']
        ).pack(pady=10)
        
        frame_inputs = tk.Frame(
            ventana, bg=self.estilos.colores['bg_card'],
            highlightthickness=2, highlightbackground=self.estilos.colores['accent_cyan']
        )
        frame_inputs.pack(pady=20, padx=50, fill='x')
        
        tk.Label(
            frame_inputs, text="Hora (HH:MM):", font=("Segoe UI", 11),
            bg=self.estilos.colores['bg_card'], fg=self.estilos.colores['text_secondary']
        ).pack(pady=(15, 5))
        
        entry_hora = ttk.Entry(
            frame_inputs, font=("Consolas", 16, "bold"),
            width=10, bootstyle="info", justify='center'
        )
        entry_hora.pack(pady=(0, 15))
        entry_hora.insert(0, "07:00")
        entry_hora.focus()
        
        def guardar():
            hora = entry_hora.get().strip()
            if ':' in hora:
                self.logic.agregar_alarma(hora, f"Alarma {hora}")
                self.actualizar_lista_alarmas()
                ventana.destroy()
                messagebox.showinfo("✓ Alarma", f"Alarma configurada para las {hora}")
            else:
                messagebox.showwarning("Error", "Formato inválido. Usa HH:MM")
        
        frame_btns = tk.Frame(ventana, bg=self.estilos.colores['bg_primary'])
        frame_btns.pack(pady=15)
        
        self.estilos.crear_boton_premium(
            frame_btns, "Guardar", guardar, variant='success', icon='✓'
        ).pack(side='left', padx=10, ipadx=15)
        
        self.estilos.crear_boton_premium(
            frame_btns, "Cancelar", ventana.destroy, variant='danger', icon='✕'
        ).pack(side='left', padx=10, ipadx=15)
        
        entry_hora.bind('<Return>', lambda e: guardar())
    
    def eliminar_alarma(self):
        """Elimina la alarma seleccionada"""
        seleccion = self.lista_alarmas.curselection()
        if seleccion:
            indice = seleccion[0]
            self.logic.eliminar_alarma(indice)
            self.actualizar_lista_alarmas()
    
    def actualizar_lista_alarmas(self):
        """Actualiza la lista de alarmas"""
        self.lista_alarmas.delete(0, 'end')
        for i, alarma in enumerate(self.logic.obtener_alarmas()):
            estado = "✓ ACTIVA" if alarma['activa'] else "✗ INACTIVA"
            self.lista_alarmas.insert('end', f"{alarma['hora']} - {estado}")
    
    # ═══════════════════════════════════════════════════════
    # CONTROLES DE NAVEGACIÓN
    # ═══════════════════════════════════════════════════════
    def toggle_cronometro(self):
        """Muestra/oculta el cronómetro"""
        self.ocultar_todos_paneles()
        if self.modo_actual != "cronometro":
            self.card_crono.pack(pady=10, padx=30, fill='both', expand=True)
            self.modo_actual = "cronometro"
            self.badge_estado.configure(text="● CRONÓMETRO", bg=self.estilos.colores['success'])
        else:
            self.modo_actual = "reloj"
            self.badge_estado.configure(text="● RELOJ", bg=self.estilos.colores['info'])
    
    def toggle_temporizador(self):
        """Muestra/oculta el temporizador"""
        self.ocultar_todos_paneles()
        if self.modo_actual != "temporizador":
            self.card_temp.pack(pady=10, padx=30, fill='both', expand=True)
            self.modo_actual = "temporizador"
            self.badge_estado.configure(text="● TEMPORIZADOR", bg=self.estilos.colores['warning'])
        else:
            self.modo_actual = "reloj"
            self.badge_estado.configure(text="● RELOJ", bg=self.estilos.colores['info'])
    
    def toggle_alarmas(self):
        """Muestra/oculta las alarmas"""
        self.ocultar_todos_paneles()
        if self.modo_actual != "alarmas":
            self.card_alarmas.pack(pady=10, padx=30, fill='both', expand=True)
            self.modo_actual = "alarmas"
            self.badge_estado.configure(text="● ALARMAS", bg=self.estilos.colores['info'])
        else:
            self.modo_actual = "reloj"
            self.badge_estado.configure(text="● RELOJ", bg=self.estilos.colores['info'])
    
    def mostrar_reloj(self):
        """Muestra solo el reloj"""
        self.ocultar_todos_paneles()
        self.modo_actual = "reloj"
        self.badge_estado.configure(text="● RELOJ ACTIVO", bg=self.estilos.colores['success'])
    
    def ocultar_todos_paneles(self):
        """Oculta todos los paneles secundarios"""
        self.card_crono.pack_forget()
        self.card_temp.pack_forget()
        self.card_alarmas.pack_forget()
    
    def crear_footer(self):
        """Crea el footer"""
        sep = self.estilos.crear_separador_elegante(self.root)
        sep.pack(fill='x', padx=40, pady=20, side='bottom')
        
        footer = tk.Frame(self.root, bg=self.estilos.colores['bg_primary'])
        footer.pack(side='bottom', pady=(0, 20))
        
        tk.Label(
            footer, text="⚡", font=("Segoe UI", 16),
            bg=self.estilos.colores['bg_primary'], fg=self.estilos.colores['accent_cyan']
        ).pack()
        
        tk.Label(
            footer, text="Reloj Profesional · Oskar Edition · 2025",
            font=("Segoe UI", 10, "bold"),
            bg=self.estilos.colores['bg_primary'], fg=self.estilos.colores['text_secondary']
        ).pack(pady=5)
        
        tk.Label(
            footer, text="Python + ttkbootstrap",
            font=("Segoe UI", 8),
            bg=self.estilos.colores['bg_primary'], fg=self.estilos.colores['text_muted']
        ).pack()