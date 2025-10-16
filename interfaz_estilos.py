"""
Sistema de estilos mejorado para el reloj analógico profesional
Incluye temas claro y oscuro
"""

class ColoresOscuro:
    """Tema Oscuro Profesional"""
    # Fondos
    bg_primary = '#0a0e1a'
    bg_secondary = '#1a1f3a'
    bg_card = '#1e2439'
    bg_reloj = '#0f1419'
    bg_panel = '#141824'
    
    # Acentos
    accent_primary = '#00d4ff'
    accent_secondary = '#b794f6'
    accent_success = '#10b981'
    accent_warning = '#f59e0b'
    accent_danger = '#ef4444'
    
    # Textos
    text_primary = '#ffffff'
    text_secondary = '#a0aec0'
    text_muted = '#6b7280'
    
    # Bordes
    border = '#374151'
    border_glow = '#00d4ff'
    border_light = '#4b5563'
    
    # Manecillas del reloj
    manecilla_hora = '#ffffff'
    manecilla_minuto = '#00d4ff'
    manecilla_segundo = '#ef4444'
    
    # Botones
    btn_primary = '#00d4ff'
    btn_success = '#10b981'
    btn_warning = '#f59e0b'
    btn_danger = '#ef4444'
    btn_secondary = '#6b7280'


class ColoresClaro:
    """Tema Claro Profesional"""
    # Fondos
    bg_primary = '#f8fafc'
    bg_secondary = '#e2e8f0'
    bg_card = '#ffffff'
    bg_reloj = '#f1f5f9'
    bg_panel = '#e5e7eb'
    
    # Acentos
    accent_primary = '#0284c7'
    accent_secondary = '#7c3aed'
    accent_success = '#059669'
    accent_warning = '#d97706'
    accent_danger = '#dc2626'
    
    # Textos
    text_primary = '#0f172a'
    text_secondary = '#475569'
    text_muted = '#94a3b8'
    
    # Bordes
    border = '#cbd5e1'
    border_glow = '#0284c7'
    border_light = '#e2e8f0'
    
    # Manecillas del reloj
    manecilla_hora = '#0f172a'
    manecilla_minuto = '#0284c7'
    manecilla_segundo = '#dc2626'
    
    # Botones
    btn_primary = '#0284c7'
    btn_success = '#059669'
    btn_warning = '#d97706'
    btn_danger = '#dc2626'
    btn_secondary = '#64748b'


class Fuentes:
    """Fuentes del sistema"""
    # Principales
    titulo = ('Segoe UI', 20, 'bold')
    subtitulo = ('Segoe UI', 12)
    titulo_modal = ('Segoe UI', 16, 'bold')
    
    # Displays
    hora_digital = ('Consolas', 42, 'bold')
    hora_digital_pequeña = ('Consolas', 24, 'bold')
    fecha = ('Segoe UI', 14)
    cronometro = ('Consolas', 36, 'bold')
    temporizador = ('Consolas', 48, 'bold')
    
    # Controles
    boton = ('Segoe UI', 11, 'bold')
    boton_pequeño = ('Segoe UI', 10, 'bold')
    label = ('Segoe UI', 11)
    label_pequeño = ('Segoe UI', 9)
    
    # Otros
    footer = ('Segoe UI', 9)
    listbox = ('Segoe UI', 11)


def obtener_colores(tema_oscuro=True):
    """Retorna el esquema de colores según el tema"""
    return ColoresOscuro() if tema_oscuro else ColoresClaro()