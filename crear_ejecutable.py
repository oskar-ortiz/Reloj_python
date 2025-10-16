"""
Script para crear ejecutable del Reloj Analógico Pro
Incluye TODAS las dependencias necesarias
"""

import os
import subprocess
import sys

print("=" * 60)
print("     CREADOR DE EJECUTABLE - RELOJ ANALÓGICO PRO")
print("=" * 60)
print()

# Verificar que main.py existe
if not os.path.exists("main.py"):
    print("✗ ERROR: No se encuentra el archivo main.py")
    print("Asegúrate de estar en la carpeta correcta del proyecto")
    input("\nPresiona ENTER para salir...")
    sys.exit(1)

# Instalar dependencias necesarias
print("Instalando dependencias necesarias...")
dependencias = ['pytz', 'pyinstaller']

for dep in dependencias:
    try:
        __import__(dep.replace('-', '_'))
        print(f"✓ {dep} ya está instalado")
    except ImportError:
        print(f"Instalando {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        print(f"✓ {dep} instalado")

print()
print("Creando ejecutable...")
print("Esto puede tardar 2-3 minutos... ⏳")
print("(No cierres esta ventana)\n")

# Comando completo con todas las dependencias
comando = [
    sys.executable,
    "-m",
    "PyInstaller",
    "--name=RelojAnalogicoProOskar",
    "--onefile",
    "--windowed",
    "--noconsole",
    "--clean",
    # Incluir módulos ocultos que PyInstaller no detecta automáticamente
    "--hidden-import=pytz",
    "--hidden-import=datetime",
    "--hidden-import=time",
    "--hidden-import=math",
    "--hidden-import=tkinter",
    "--hidden-import=tkinter.ttk",
    "--hidden-import=tkinter.messagebox",
    "main.py"
]

# Ejecutar PyInstaller
try:
    print("Ejecutando PyInstaller...")
    print("-" * 60)
    
    resultado = subprocess.run(
        comando, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Mostrar salida
    if resultado.stdout:
        print(resultado.stdout)
    
    if resultado.returncode == 0:
        print("\n" + "=" * 60)
        print("✓✓✓ EJECUTABLE CREADO EXITOSAMENTE ✓✓✓")
        print("=" * 60)
        print()
        
        exe_path = os.path.join("dist", "RelojAnalogicoProOskar.exe")
        
        if os.path.exists(exe_path):
            tamaño_mb = os.path.getsize(exe_path) / (1024*1024)
            print(f"📁 Ubicación: {os.path.abspath('dist')}")
            print(f"📦 Archivo: RelojAnalogicoProOskar.exe")
            print(f"💾 Tamaño: {tamaño_mb:.1f} MB")
            print()
            print("🎉 ¡Ejecutable listo para usar!")
            print("🚀 Incluye TODAS las dependencias (pytz, tkinter, etc.)")
            print("💡 No necesita Python instalado")
            print()
            
            # Preguntar si abrir carpeta
            print("¿Abrir carpeta 'dist'? (s/n): ", end="")
            try:
                respuesta = input().lower()
                if respuesta == 's' or respuesta == 'si':
                    os.startfile("dist")
            except:
                pass
        else:
            print("⚠️ El ejecutable debería estar en la carpeta 'dist'")
            print(f"   Busca: {os.path.abspath('dist')}")
    else:
        print("\n" + "=" * 60)
        print("✗ ERROR AL CREAR EL EJECUTABLE")
        print("=" * 60)
        print("\nDetalles del error:")
        if resultado.stderr:
            print(resultado.stderr)
        print()
        print("Posibles soluciones:")
        print("1. Verifica que todos los archivos .py estén en la carpeta")
        print("2. Instala manualmente: pip install pytz")
        print("3. Cierra cualquier antivirus temporalmente")
        
except FileNotFoundError:
    print("\n✗ No se pudo ejecutar PyInstaller")
    print("Intenta instalar manualmente:")
    print(f"   {sys.executable} -m pip install pyinstaller")
except KeyboardInterrupt:
    print("\n\n⚠️ Proceso cancelado por el usuario")
except Exception as e:
    print(f"\n✗ Error inesperado: {e}")
    print(f"Tipo de error: {type(e).__name__}")

print()
input("Presiona ENTER para salir...")