# interfaz_estilos.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk

class EstiloApp:
    def __init__(self, root, tema_inicial="darkly"):
        """Inicializa el sistema de estilos profesional"""
        self.root = root
        self.style = ttk.Style(theme=tema_inicial)
        
        # Colores profesionales personalizados MEJORADOS
        self.colores = {
            'bg_primary': '#0a0e1a',          # Fondo principal más oscuro
            'bg_secondary': '#1a1f3a',        # Fondo secundario
            'bg_card': '#1e2439',             # Cards con contraste
            'bg_card_hover': '#252b45',       # Hover en cards
            'accent_cyan': '#00d4ff',         # Cian brillante
            'accent_purple': '#b794f6',       # Morado suave
            'accent_gradient': '#7b2cbf',     # Morado oscuro
            'text_primary': '#ffffff',        # Texto principal
            'text_secondary': '#a0aec0',      # Texto secundario
            'text_muted': '#6b7280',          # Texto apagado (CORREGIDO)
            'text_disabled': '#4a5568',       # Texto deshabilitado
            'success': '#10b981',             # Verde éxito
            'warning': '#f59e0b',             # Naranja advertencia
            'danger': '#ef4444',              # Rojo peligro
            'info': '#3b82f6',                # Azul información
            'border': '#374151',              # Bordes sutiles
            'border_focus': '#00d4ff',        # Borde en foco
            'shadow': 'rgba(0, 0, 0, 0.5)'    # Sombras
        }
        
        self._actualizar_colores()
        self.root.configure(bg=self.colores['bg_primary'])

    def _actualizar_colores(self):
        """Actualiza los colores base del tema actual"""
        colors = self.style.colors
        self.bg = self.colores['bg_primary']
        self.fg = self.colores['text_primary']
        self.primary = colors.primary
        self.secondary = colors.secondary
        self.success = colors.success
        self.warning = colors.warning
        self.danger = colors.danger

    def aplicar_tema(self, tema):
        """Cambia el tema visual y actualiza colores"""
        try:
            self.style.theme_use(tema)
            self._actualizar_colores()
            self.root.configure(bg=self.bg)
        except Exception as e:
            print(f"⚠️ Error aplicando tema: {e}")

    def crear_card_moderna(self, parent, padding=25):
        """Crea un card moderno con efecto glassmorphism mejorado"""
        card = ttk.Frame(parent, padding=padding, bootstyle="dark")
        card.configure(relief="flat")
        
        # Agregar borde sutil para efecto premium
        card.configure(
            borderwidth=1,
            relief="solid"
        )
        
        return card

    def crear_boton_premium(self, parent, texto, comando=None, variant='primary', icon=''):
        """Crea un botón premium con efectos hover mejorados"""
        texto_completo = f"{icon} {texto}" if icon else texto
        
        # Mapeo de variantes a estilos de ttkbootstrap
        estilos = {
            'primary': 'info',
            'success': 'success',
            'danger': 'danger',
            'secondary': 'secondary',
            'dark': 'dark',
            'warning': 'warning'
        }
        
        estilo_base = estilos.get(variant, 'info')
        
        btn = ttk.Button(
            parent,
            text=texto_completo,
            bootstyle=f"{estilo_base}",
            command=comando,
            cursor='hand2',
            width=15  # Ancho uniforme para todos los botones
        )
        
        # Efectos hover mejorados con animación
        def on_enter(e):
            btn.configure(bootstyle=f"{estilo_base}-outline")
        
        def on_leave(e):
            btn.configure(bootstyle=f"{estilo_base}")
        
        # Efecto de clic
        def on_press(e):
            btn.configure(bootstyle=f"{estilo_base}")
        
        def on_release(e):
            btn.configure(bootstyle=f"{estilo_base}-outline")
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<ButtonPress-1>", on_press)
        btn.bind("<ButtonRelease-1>", on_release)
        
        return btn

    def crear_separador_elegante(self, parent, color='#374151', height=2):
        """Crea un separador horizontal elegante con gradiente simulado"""
        # Frame contenedor para el separador
        container = tk.Frame(parent, bg=self.colores['bg_primary'], height=height+2)
        
        # Línea principal
        line = tk.Frame(container, height=height, bg=color)
        line.pack(fill='x')
        
        return container

    def crear_separador_con_texto(self, parent, texto):
        """Crea un separador con texto en el centro"""
        frame = tk.Frame(parent, bg=self.colores['bg_primary'])
        
        # Línea izquierda
        line_left = tk.Frame(frame, height=1, bg=self.colores['border'])
        line_left.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Texto
        label = tk.Label(
            frame,
            text=texto,
            font=("Segoe UI", 9, "bold"),
            bg=self.colores['bg_primary'],
            fg=self.colores['text_muted']
        )
        label.pack(side='left')
        
        # Línea derecha
        line_right = tk.Frame(frame, height=1, bg=self.colores['border'])
        line_right.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        return frame

    def crear_titulo_seccion(self, parent, texto, color='#00d4ff'):
        """Crea un título de sección con estilo mejorado"""
        # Frame contenedor
        frame = tk.Frame(parent, bg=self.colores['bg_card'])
        
        # Barra de color decorativa
        barra = tk.Frame(frame, width=4, bg=color)
        barra.pack(side='left', fill='y', padx=(0, 10))
        
        # Label del título
        label = tk.Label(
            frame,
            text=texto,
            font=("Segoe UI", 12, "bold"),
            bg=self.colores['bg_card'],
            fg=color,
            anchor="w"
        )
        label.pack(side='left', fill='x', expand=True)
        
        return frame

    def crear_label_premium(self, parent, texto, size=12, bold=False, color=None):
        """Crea un label con estilo premium"""
        peso = "bold" if bold else "normal"
        color_final = color or self.colores['text_secondary']
        
        label = tk.Label(
            parent,
            text=texto,
            font=("Segoe UI", size, peso),
            bg=self.colores['bg_primary'],
            fg=color_final
        )
        return label

    def crear_badge(self, parent, texto, tipo='success'):
        """Crea un badge de estado con diseño mejorado"""
        colores_badge = {
            'success': (self.colores['success'], '#ffffff'),
            'warning': (self.colores['warning'], '#1a1f2e'),
            'danger': (self.colores['danger'], '#ffffff'),
            'info': (self.colores['accent_cyan'], '#1a1f2e'),
            'secondary': (self.colores['text_secondary'], '#1a1f2e')
        }
        
        bg, fg = colores_badge.get(tipo, colores_badge['info'])
        
        badge = tk.Label(
            parent,
            text=texto,
            font=("Segoe UI", 9, "bold"),
            bg=bg,
            fg=fg,
            padx=12,
            pady=4,
            relief='flat'
        )
        
        # Bordes redondeados simulados con padding
        badge.configure(
            highlightthickness=0,
            borderwidth=0
        )
        
        return badge

    def crear_boton_icono(self, parent, icono, comando=None, tooltip=None):
        """Crea un botón circular solo con ícono"""
        btn = tk.Button(
            parent,
            text=icono,
            font=("Segoe UI", 16),
            bg=self.colores['bg_card'],
            fg=self.colores['accent_cyan'],
            activebackground=self.colores['bg_card_hover'],
            activeforeground=self.colores['accent_cyan'],
            relief='flat',
            cursor='hand2',
            width=3,
            height=1,
            command=comando
        )
        
        # Efectos hover
        def on_enter(e):
            btn.configure(bg=self.colores['bg_card_hover'])
        
        def on_leave(e):
            btn.configure(bg=self.colores['bg_card'])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn

    def aplicar_efecto_glow(self, widget):
        """Aplica un efecto de resplandor a un widget"""
        widget.configure(
            highlightthickness=2,
            highlightbackground=self.colores['accent_cyan'],
            highlightcolor=self.colores['accent_cyan']
        )
    
    def aplicar_efecto_glow_purple(self, widget):
        """Aplica un efecto de resplandor morado a un widget"""
        widget.configure(
            highlightthickness=2,
            highlightbackground=self.colores['accent_purple'],
            highlightcolor=self.colores['accent_purple']
        )
    
    def crear_tooltip(self, widget, texto):
        """Crea un tooltip para cualquier widget"""
        tooltip = None
        
        def mostrar_tooltip(event):
            nonlocal tooltip
            x = event.x_root + 10
            y = event.y_root + 10
            
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(
                tooltip,
                text=texto,
                background=self.colores['bg_card'],
                foreground=self.colores['text_primary'],
                relief='solid',
                borderwidth=1,
                font=("Segoe UI", 9),
                padx=8,
                pady=4
            )
            label.pack()
        
        def ocultar_tooltip(event):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None
        
        widget.bind("<Enter>", mostrar_tooltip)
        widget.bind("<Leave>", ocultar_tooltip)
    
    def animar_widget(self, widget, propiedad, valor_inicial, valor_final, duracion=300):
        """Anima una propiedad de un widget (simulado)"""
        # Nota: tkinter tiene limitaciones para animaciones suaves
        # Esta es una versión simplificada
        pasos = 10
        incremento = (valor_final - valor_inicial) / pasos
        delay = duracion // pasos
        
        def animar_paso(paso):
            if paso <= pasos:
                valor = valor_inicial + (incremento * paso)
                # Aplicar el cambio según la propiedad
                # (Simplificado, solo como ejemplo)
                widget.after(delay, lambda: animar_paso(paso + 1))
        
        animar_paso(0)