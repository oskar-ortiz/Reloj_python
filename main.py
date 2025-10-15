import tkinter as tk
from interfaz import InterfazReloj
from interfaz_estilos import EstiloApp
import os

def main():
    # Crear ventana principal
    root = tk.Tk()
    root.title("⏰ Reloj Profesional - Oskar Edition")
    root.geometry("650x800")
    root.resizable(False, False)
    
    # Inicializar sistema de estilos
    estilos = EstiloApp(root, tema_inicial="darkly")
    root.configure(bg=estilos.colores['bg_primary'])
    
    # Centrar ventana en pantalla
    root.update_idletasks()
    width = 650
    height = 800
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Ruta del sonido por defecto
    sonido_por_defecto = os.path.join("sounds", "alarma.mp3")
    
    # Crear instancia de la interfaz
    interfaz = InterfazReloj(root, sound_path=sonido_por_defecto, tema_inicial="darkly")
    
    # ═══════════════════════════════════════════════════════
    # HEADER DECORATIVO
    # ═══════════════════════════════════════════════════════
    header = tk.Frame(root, bg=estilos.colores['bg_primary'])
    header.pack(fill='x', pady=(25, 10))
    
    # Logo/Título principal
    titulo_app = tk.Label(
        header,
        text="RELOJ PROFESIONAL",
        font=("Segoe UI", 16, "bold"),
        bg=estilos.colores['bg_primary'],
        fg=estilos.colores['accent_cyan']
    )
    titulo_app.pack()
    
    subtitulo_app = tk.Label(
        header,
        text="OSKAR EDITION",
        font=("Segoe UI", 10),
        bg=estilos.colores['bg_primary'],
        fg=estilos.colores['text_secondary']
    )
    subtitulo_app.pack()
    
    # Línea decorativa superior
    linea_superior = tk.Frame(header, height=2, bg=estilos.colores['accent_cyan'])
    linea_superior.pack(fill='x', padx=100, pady=15)
    
    # ═══════════════════════════════════════════════════════
    # DISPLAY PRINCIPAL - HORA
    # ═══════════════════════════════════════════════════════
    
    # Card para el reloj principal
    card_reloj = estilos.crear_card_moderna(root, padding=30)
    card_reloj.pack(pady=(10, 5), padx=40, fill='x')
    
    # Label de hora con efecto gradiente simulado
    lbl_hora = tk.Label(
        card_reloj,
        text="00:00:00",
        font=("Consolas", 68, "bold"),
        bg=estilos.colores['bg_card'],
        fg=estilos.colores['accent_cyan']
    )
    lbl_hora.pack(pady=(5, 10))
    
    # Efecto de resplandor
    estilos.aplicar_efecto_glow(lbl_hora)
    
    # ═══════════════════════════════════════════════════════
    # DISPLAY SECUNDARIO - FECHA
    # ═══════════════════════════════════════════════════════
    
    lbl_fecha = tk.Label(
        card_reloj,
        text="Cargando fecha...",
        font=("Segoe UI", 13),
        bg=estilos.colores['bg_card'],
        fg=estilos.colores['text_secondary']
    )
    lbl_fecha.pack(pady=(0, 10))
    
    # Línea decorativa inferior del card
    linea_card = tk.Frame(card_reloj, height=1, bg=estilos.colores['border'])
    linea_card.pack(fill='x', pady=(10, 0))
    
    # ═══════════════════════════════════════════════════════
    # REGISTRAR WIDGETS Y CREAR INTERFAZ COMPLETA
    # ═══════════════════════════════════════════════════════
    
    interfaz.crear_marcas_hora(lbl_hora, lbl_fecha)
    
    # ═══════════════════════════════════════════════════════
    # ANIMACIÓN DE ENTRADA (OPCIONAL)
    # ═══════════════════════════════════════════════════════
    
    def animar_entrada():
        """Pequeña animación de fade-in al iniciar"""
        try:
            root.attributes('-alpha', 0.0)
            alpha = 0.0
            
            def fade_in():
                nonlocal alpha
                if alpha < 1.0:
                    alpha += 0.05
                    root.attributes('-alpha', alpha)
                    root.after(20, fade_in)
            
            fade_in()
        except:
            # Si no soporta transparencia, mostrar directamente
            root.attributes('-alpha', 1.0)
    
    # Iniciar animación
    root.after(100, animar_entrada)
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == "__main__":
    main()