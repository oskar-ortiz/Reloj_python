
# Reloj Python - Proyecto para VSCode

Proyecto completo que contiene un reloj con interfaz gráfica usando **Tkinter** (incluido en Python).
Características:
- Modo analógico y digital (botón para alternar).
- Alarma (establece hora y minuto, muestra alerta cuando llega la hora).
- Cronómetro (start / stop / reset).
- Temas: claro y oscuro.
- Diseño pensado para ser profesional y fácil de modificar.

## Requisitos
- Python 3.8+ (Tkinter incluido en la instalación estándar).
- No requiere librerías externas.

## Ejecutar
1. Extrae el contenido y abre la carpeta en VSCode.
2. Ejecuta `python main.py` desde la terminal (asegúrate que el intérprete de Python esté configurado en VSCode).

## Estructura del proyecto
- `main.py` - punto de entrada.
- `interfaz.py` - contiene la interfaz Tkinter y toda la lógica de interacción.
- `reloj.py` - utilidades y cálculos del reloj.
- `utils/colores.py` - definiciones de colores y temas.

## Notas
- El proyecto está hecho para ser editable: agrégale funcionalidades o cambia estilos desde `utils/colores.py` o `interfaz.py`.
