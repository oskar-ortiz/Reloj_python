"""
interfaz.py
Interfaz con ttkbootstrap. Reloj analógico oscuro + neon en Canvas.
Incluye panel lateral con: alarmas, cronómetro, temporizador, zonas y config básico.
"""
import tkinter as tk
from tkinter import messagebox
import math
import time
import threading

# ttkbootstrap
try:
    import ttkbootstrap as tb
    from ttkbootstrap.constants import *
    TB = True
except Exception:
    # Fallback: usar tkinter.ttk (menos estilizado)
    import tkinter.ttk as tb
    from tkinter.ttk import *
    TB = False

from reloj_logica import LogicaRelojPro
import pytz
from datetime import datetime

class RelojAnalogicoPro:
    def __init__(self, root):
        self.root = root
        # aplicar estilo
        if TB:
            self.style = tb.Style(theme="darkly")  # tema oscuro
        else:
            self.style = None
        self.root.title("⏰ Reloj Analógico Pro - Oskar Edition")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)

        # colores neon / oscuro (puedes ajustarlos)
        self.colores = {
            "bg": "#0b0f14",
            "card": "#0f1620",
            "neon": "#39f0ff",      # cyan neon
            "accent": "#7b61ff",    # magenta accent
            "muted": "#8a97a8",
            "tick": "#2c3e50",
            "warning": "#ffb86b"
        }

        # lógica (pasamos callback para alarm trigger)
        self.logic = LogicaRelojPro(on_alarm_callback=self._on_alarm_trigger)

        # parámetros canvas reloj
        self.canvas_size = 540
        self.center = self.canvas_size // 2
        self.radius = int(self.canvas_size * 0.42)

        # IDs para actualizar manecillas
        self._ids = {"hora": None, "min": None, "seg": None, "centro": None, "ticks": []}

        # GUI layout
        self._crear_layout()
        # dibujar cara y manecillas iniciales
        self._dibujar_cara()
        self._crear_manecillas()
        # iniciar animación
        self._ultima = 0.0
        self.animar_reloj()

        # iniciar actualizadores de cronómetro/temporizador en UI
        self.actualizar_ui_crono()
        self.actualizar_ui_temp()

    # ---------------- Layout principal ----------------
    def _crear_layout(self):
        # root background
        self.root.configure(bg=self.colores["bg"])
        # grid: 0 = izquierda (reloj), 1 = derecha (panel)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)

        # Frame izquierdo (reloj)
        left = tk.Frame(self.root, bg=self.colores["bg"])
        left.grid(row=0, column=0, sticky='nsew', padx=16, pady=16)
        left.grid_rowconfigure(0, weight=0)
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        header = tk.Frame(left, bg=self.colores["bg"])
        header.grid(row=0, column=0, sticky='ew', pady=(8,4))
        tk.Label(header, text="RELOJ ANALÓGICO PRO", font=("Segoe UI", 18, "bold"), fg=self.colores["neon"], bg=self.colores["bg"]).pack()
        tk.Label(header, text="OSKAR EDITION · 2025", font=("Segoe UI", 10), fg=self.colores["muted"], bg=self.colores["bg"]).pack()

        # canvas card
        card = tk.Frame(left, bg=self.colores["card"], bd=0, relief='flat')
        card.grid(row=1, column=0, sticky='n', pady=8)
        self.canvas = tk.Canvas(card, width=self.canvas_size, height=self.canvas_size, bg=self.colores["card"], highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)

        # digital time + date
        foot = tk.Frame(left, bg=self.colores["bg"])
        foot.grid(row=2, column=0, sticky='ew', pady=(4,10))
        self.lbl_digital = tk.Label(foot, text="00:00:00", font=("Consolas", 24), fg=self.colores["neon"], bg=self.colores["bg"])
        self.lbl_digital.pack()
        self.lbl_fecha = tk.Label(foot, text="", font=("Segoe UI", 11), fg=self.colores["muted"], bg=self.colores["bg"])
        self.lbl_fecha.pack()

        # Frame derecho (panel)
        right = tk.Frame(self.root, bg=self.colores["card"], width=380)
        right.grid(row=0, column=1, sticky='nsew', padx=(0,16), pady=16)
        right.grid_rowconfigure(5, weight=1)

        # Panel header
        tk.Label(right, text="PANEL DE CONTROL", font=("Segoe UI", 14, "bold"), fg=self.colores["accent"], bg=self.colores["card"]).pack(pady=(14,8))
        tk.Frame(right, bg=self.colores["bg"], height=2).pack(fill='x', padx=12, pady=6)

        # NAV botones
        nav = tk.Frame(right, bg=self.colores["card"])
        nav.pack(pady=8, padx=12, fill='x')
        btns = [
            ("Alarmas", self.mostrar_panel_alarmas),
            ("Cronómetro", self.mostrar_panel_cronometro),
            ("Temporizador", self.mostrar_panel_temporizador),
            ("Zonas", self.mostrar_panel_zonas),
            ("Config", self.mostrar_panel_config)
        ]
        for i, (label, cmd) in enumerate(btns):
            b = tk.Button(nav, text=label, command=cmd, bg=self.colores["bg"], fg=self.colores["neon"],
                          relief='flat', padx=8, pady=6, cursor='hand2')
            b.grid(row=i, column=0, sticky='ew', pady=4)

        # contenedor de subpaneles
        self.subpanel = tk.Frame(right, bg=self.colores["card"])
        self.subpanel.pack(fill='both', expand=True, padx=12, pady=12)

        # iniciamos mostrando alarmas
        self.mostrar_panel_alarmas()

    # ---------------- Reloj analógico/carátula ----------------
    def _dibujar_cara(self):
        c = self.canvas
        c.delete("cara")
        center = self.center
        r = self.radius

        # Outer glow (simulado con varios círculos)
        for i, alpha in enumerate([18, 12, 6]):
            offset = 18 + i*6
            c.create_oval(center - r - offset, center - r - offset, center + r + offset, center + r + offset,
                          fill=self.colores["bg"], outline="", tags="cara")

        # Face
        c.create_oval(center - r, center - r, center + r, center + r,
                      fill=self.colores["card"], outline=self.colores["neon"], width=3, tags="cara")

        # ticks horas (más visibles) y minutos (sutiles)
        for id_ in self._ids.get("ticks", []):
            try:
                self.canvas.delete(id_)
            except:
                pass
        self._ids["ticks"].clear()

        for m in range(60):
            angle = math.radians(m * 6)
            cos = math.cos(angle)
            sin = math.sin(angle)
            if m % 5 == 0:
                x1 = center + (r - 10) * sin
                y1 = center - (r - 10) * cos
                x2 = center + (r - 30) * sin
                y2 = center - (r - 30) * cos
                idtick = c.create_line(x1, y1, x2, y2, width=4, fill=self.colores["neon"], capstyle='round', tags="cara")
                self._ids["ticks"].append(idtick)
                # números
                num = 12 if m == 0 else m // 5
                tx = center + (r - 70) * sin
                ty = center - (r - 70) * cos
                c.create_text(tx, ty, text=str(num), font=("Segoe UI", 12), fill=self.colores["muted"], tags="cara")
            else:
                x1 = center + (r - 14) * sin
                y1 = center - (r - 14) * cos
                x2 = center + (r - 22) * sin
                y2 = center - (r - 22) * cos
                idtick = c.create_line(x1, y1, x2, y2, width=1, fill=self.colores["tick"], tags="cara")
                self._ids["ticks"].append(idtick)

        # centro
        centro = c.create_oval(center - 6, center - 6, center + 6, center + 6, fill=self.colores["neon"], outline="", tags="cara")
        self._ids["centro"] = centro

    def _crear_manecillas(self):
        c = self.canvas
        center = self.center
        # si existen borrarlas primero
        for key in ("hora","min","seg"):
            if self._ids.get(key):
                try:
                    c.delete(self._ids[key])
                except:
                    pass
        # crear manecillas
        hora_line = c.create_line(center, center, center, center - int(self.radius * 0.5),
                                  width=8, capstyle='round', fill=self.colores["accent"])
        min_line = c.create_line(center, center, center, center - int(self.radius * 0.75),
                                 width=5, capstyle='round', fill=self.colores["neon"])
        seg_line = c.create_line(center, center, center, center - int(self.radius * 0.9),
                                 width=2, capstyle='round', fill=self.colores["warning"])

        self._ids["hora"] = hora_line
        self._ids["min"] = min_line
        self._ids["seg"] = seg_line

    def _actualizar_manecillas(self, h, m, s_float):
        c = self.canvas
        center = self.center
        r = self.radius

        # angulos: convertir a radianes; 0 arriba
        ang_seg = math.radians(s_float * 6)  # 360/60
        ang_min = math.radians(m * 6 + s_float * 0.1)
        ang_hor = math.radians((h % 12) * 30 + m * 0.5)

        def coords(angle, length_ratio):
            x = center + (r * length_ratio) * math.sin(angle)
            y = center - (r * length_ratio) * math.cos(angle)
            return (center, center, x, y)

        try:
            c.coords(self._ids["hora"], *coords(ang_hor, 0.5))
            c.coords(self._ids["min"], *coords(ang_min, 0.75))
            c.coords(self._ids["seg"], *coords(ang_seg, 0.9))
        except Exception:
            # si algo falla, recrear manecillas
            self._crear_manecillas()

    # ---------------- Loop animación ----------------
    def animar_reloj(self):
        ahora = time.time()
        # limitar ~30 FPS
        if ahora - self._ultima < 1/30:
            self.root.after(10, self.animar_reloj)
            return
        self._ultima = ahora

        dt = datetime.now()
        horas = dt.hour
        minutos = dt.minute
        segundos = dt.second + dt.microsecond / 1_000_000.0

        # actualizar manecillas y etiquetas
        self._actualizar_manecillas(horas, minutos, segundos)
        self.lbl_digital.config(text=dt.strftime("%H:%M:%S"))
        self.lbl_fecha.config(text=dt.strftime("%A, %d %B %Y"))

        self.root.after(33, self.animar_reloj)

    # ----------------- PANEL: ALARMAS -----------------
    def mostrar_panel_alarmas(self):
        self._limpiar_subpanel()
        frame = tk.Frame(self.subpanel, bg=self.colores["card"])
        frame.pack(fill='both', expand=True)

        # lista
        tk.Label(frame, text="Alarmas programadas", bg=self.colores["card"], fg=self.colores["neon"], font=("Segoe UI", 12, "bold")).pack(pady=(8,4))
        list_frame = tk.Frame(frame, bg=self.colores["card"])
        list_frame.pack(fill='x', padx=8)

        self.lb_alarmas = tk.Listbox(list_frame, bg=self.colores["bg"], fg=self.colores["neon"], bd=0, height=6)
        self.lb_alarmas.pack(side='left', fill='both', expand=True, padx=(0,4), pady=6)
        scrollbar = tk.Scrollbar(list_frame, command=self.lb_alarmas.yview)
        scrollbar.pack(side='right', fill='y')
        self.lb_alarmas.config(yscrollcommand=scrollbar.set)

        self._refrescar_lista_alarmas()

        # formulario
        form = tk.Frame(frame, bg=self.colores["card"])
        form.pack(padx=8, pady=8, fill='x')
        tk.Label(form, text="Hora (HH):", bg=self.colores["card"], fg=self.colores["muted"]).grid(row=0,column=0, sticky='e')
        self.ent_hora = tk.Entry(form, width=5)
        self.ent_hora.grid(row=0,column=1, padx=6)
        tk.Label(form, text="Minuto (MM):", bg=self.colores["card"], fg=self.colores["muted"]).grid(row=0,column=2, sticky='e')
        self.ent_min = tk.Entry(form, width=5)
        self.ent_min.grid(row=0,column=3, padx=6)
        tk.Label(form, text="Nombre:", bg=self.colores["card"], fg=self.colores["muted"]).grid(row=1,column=0, sticky='e')
        self.ent_name = tk.Entry(form, width=20)
        self.ent_name.grid(row=1,column=1, columnspan=3, pady=6, sticky='w')

        chk_frame = tk.Frame(form, bg=self.colores["card"])
        chk_frame.grid(row=2, column=0, columnspan=4, pady=(4,0))
        self.var_repetir = tk.BooleanVar(value=False)
        tk.Checkbutton(chk_frame, text="Repetir diariamente", variable=self.var_repetir, bg=self.colores["card"], fg=self.colores["muted"], selectcolor=self.colores["card"]).pack(anchor='w')

        btns = tk.Frame(frame, bg=self.colores["card"])
        btns.pack(pady=6)
        tk.Button(btns, text="Agregar", command=self._ui_agregar_alarma, bg=self.colores["neon"], fg="#001", padx=10).pack(side='left', padx=6)
        tk.Button(btns, text="Eliminar seleccionada", command=self._ui_eliminar_alarma, bg=self.colores["accent"], fg="#fff").pack(side='left', padx=6)

    def _refrescar_lista_alarmas(self):
        try:
            self.lb_alarmas.delete(0, tk.END)
        except Exception:
            pass
        for a in self.logic.obtener_alarmas():
            estado = "✓" if a.get("activa", False) else "✗"
            rep = "🔁" if a.get("repetir", False) else ""
            texto = f"{estado} {a['hora']:02}:{a['minuto']:02} - {a['nombre']} {rep}"
            self.lb_alarmas.insert(tk.END, texto)

    def _ui_agregar_alarma(self):
        try:
            h = int(self.ent_hora.get())
            m = int(self.ent_min.get())
            name = self.ent_name.get().strip() or "Alarma"
            rep = self.var_repetir.get()
            self.logic.agregar_alarma(h, m, name, rep)
            messagebox.showinfo("Alarma", f"Alarma agregada: {name} {h:02}:{m:02}")
            self._refrescar_lista_alarmas()
        except ValueError:
            messagebox.showerror("Error", "Introduce hora y minuto válidos (números).")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _ui_eliminar_alarma(self):
        sel = self.lb_alarmas.curselection()
        if sel:
            self.logic.eliminar_alarma(sel[0])
            self._refrescar_lista_alarmas()
        else:
            messagebox.showwarning("Selecciona", "Selecciona una alarma primero")

    # --------------- PANEL: CRONOMETRO ----------------
    def mostrar_panel_cronometro(self):
        self._limpiar_subpanel()
        frame = tk.Frame(self.subpanel, bg=self.colores["card"])
        frame.pack(fill='both', expand=True)
        tk.Label(frame, text="Cronómetro", bg=self.colores["card"], fg=self.colores["neon"], font=("Segoe UI", 12,"bold")).pack(pady=6)
        self.lbl_crono_ui = tk.Label(frame, text="00:00:00.00", font=("Consolas", 16), bg=self.colores["card"], fg=self.colores["muted"])
        self.lbl_crono_ui.pack(pady=8)

        btns = tk.Frame(frame, bg=self.colores["card"])
        btns.pack()
        tk.Button(btns, text="Iniciar", command=self._crono_iniciar, bg=self.colores["neon"]).grid(row=0,column=0,padx=6)
        tk.Button(btns, text="Pausar", command=self._crono_pausar, bg=self.colores["accent"]).grid(row=0,column=1,padx=6)
        tk.Button(btns, text="Vuelta", command=self._crono_vuelta, bg=self.colores["warning"]).grid(row=0,column=2,padx=6)
        tk.Button(btns, text="Reset", command=self._crono_reset, bg=self.colores["bg"], fg=self.colores["neon"]).grid(row=0,column=3,padx=6)

        tk.Label(frame, text="Vueltas:", bg=self.colores["card"], fg=self.colores["muted"]).pack(pady=(12,0))
        self.lb_vueltas = tk.Listbox(frame, height=6, bg=self.colores["bg"], fg=self.colores["neon"])
        self.lb_vueltas.pack(fill='both', padx=8, pady=6)

    def _crono_iniciar(self):
        self.logic.crono_start()
    def _crono_pausar(self):
        self.logic.crono_pause()
    def _crono_vuelta(self):
        v = self.logic.crono_vuelta()
        if v:
            self.lb_vueltas.insert(tk.END, v)
    def _crono_reset(self):
        self.logic.crono_reset()
        try:
            self.lb_vueltas.delete(0, tk.END)
        except:
            pass

    def actualizar_ui_crono(self):
        try:
            if self.logic.cronometro_corriendo or self.logic.cronometro_iniciado:
                t = self.logic.obtener_tiempo_cronometro()
                if hasattr(self, 'lbl_crono_ui'):
                    self.lbl_crono_ui.config(text=t)
        except Exception:
            pass
        self.root.after(100, self.actualizar_ui_crono)

    # --------------- PANEL: TEMPORIZADOR ----------------
    def mostrar_panel_temporizador(self):
        self._limpiar_subpanel()
        frame = tk.Frame(self.subpanel, bg=self.colores["card"])
        frame.pack(fill='both', expand=True)
        tk.Label(frame, text="Temporizador (s)", bg=self.colores["card"], fg=self.colores["neon"], font=("Segoe UI", 12,"bold")).pack(pady=6)
        self.ent_temp = tk.Entry(frame, width=12)
        self.ent_temp.pack(pady=6)
        tk.Button(frame, text="Iniciar", command=self._ui_iniciar_temporizador, bg=self.colores["neon"]).pack(pady=4)
        tk.Button(frame, text="Detener", command=self.logic.detener_temporizador, bg=self.colores["accent"]).pack(pady=4)
        self.lbl_temp_ui = tk.Label(frame, text="00:00:00", bg=self.colores["card"], fg=self.colores["muted"])
        self.lbl_temp_ui.pack(pady=8)

    def _ui_iniciar_temporizador(self):
        try:
            s = int(self.ent_temp.get())
            self.logic.iniciar_temporizador(s)
            messagebox.showinfo("Temporizador", f"Temporizador iniciado por {s} segundos")
        except ValueError:
            messagebox.showerror("Error", "Introduce segundos válidos (número entero)")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_ui_temp(self):
        try:
            if hasattr(self, 'lbl_temp_ui'):
                self.lbl_temp_ui.config(text=self.logic.obtener_tiempo_temporizador())
        except Exception:
            pass
        self.root.after(500, self.actualizar_ui_temp)

    # --------------- PANEL: ZONAS ----------------
    def mostrar_panel_zonas(self):
        self._limpiar_subpanel()
        frame = tk.Frame(self.subpanel, bg=self.colores["card"])
        frame.pack(fill='both', expand=True)
        tk.Label(frame, text="Zonas Horarias", bg=self.colores["card"], fg=self.colores["neon"], font=("Segoe UI", 12,"bold")).pack(pady=6)

        zonas = ["America/Bogota","America/Mexico_City","Europe/London","Asia/Tokyo","Australia/Sydney"]
        self.var_zona = tk.StringVar(value=zonas[0])
        tk.OptionMenu(frame, self.var_zona, *zonas).pack(pady=6)
        self.lbl_zona_hora = tk.Label(frame, text="", bg=self.colores["card"], fg=self.colores["muted"])
        self.lbl_zona_hora.pack(pady=6)
        self._actualizar_zona()
    
    def _actualizar_zona(self):
        try:
            tzname = self.var_zona.get()
            tz = pytz.timezone(tzname)
            ahora = datetime.now(tz)
            self.lbl_zona_hora.config(text=ahora.strftime("%Y-%m-%d %H:%M:%S"))
        except Exception:
            self.lbl_zona_hora.config(text="Error zona")
        self.root.after(1000, self._actualizar_zona)

    # --------------- PANEL: CONFIG ----------------
    def mostrar_panel_config(self):
        self._limpiar_subpanel()
        frame = tk.Frame(self.subpanel, bg=self.colores["card"])
        frame.pack(fill='both', expand=True)
        tk.Label(frame, text="Configuración", bg=self.colores["card"], fg=self.colores["neon"], font=("Segoe UI", 12,"bold")).pack(pady=6)
        tk.Label(frame, text="Tema: Oscuro (neon)", bg=self.colores["card"], fg=self.colores["muted"]).pack(pady=4)
        tk.Label(frame, text="Sonido de alarma: integrado (sistema)", bg=self.colores["card"], fg=self.colores["muted"]).pack(pady=4)

    # ----------------- UTILS -------------------
    def _limpiar_subpanel(self):
        for w in self.subpanel.winfo_children():
            w.destroy()

    # ----------------- ALARM TRIGGER CALLBACK (UI) -------------------
    def _on_alarm_trigger(self, alarma):
        # alarma: dict con keys 'nombre', 'hora', 'minuto' (puede venir desde temporizador con hora None)
        nombre = alarma.get("nombre", "Alarma")
        # llamar a UI en hilo principal
        def _show():
            try:
                messagebox.showinfo("Alarma", f"🔔 {nombre}")
                # intentar sonido: winsound en Windows, si no usar bell()
                try:
                    import winsound
                    winsound.Beep(1000, 700)
                except Exception:
                    try:
                        self.root.bell()
                    except:
                        pass
            except Exception:
                pass
        # ejecutar en main thread
        self.root.after(10, _show)

    # ----------------- cerrar (cleanup) -------------------
    def close(self):
        try:
            self.logic.stop()
        except:
            pass

# Fin interfaz.py
