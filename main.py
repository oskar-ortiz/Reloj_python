"""
main.py
Arranca la aplicación Reloj Analógico Pro (modo oscuro neon).
"""
from interfaz import RelojAnalogicoPro
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = RelojAnalogicoPro(root)
    root.mainloop()
