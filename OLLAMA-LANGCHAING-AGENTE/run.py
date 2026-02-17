#!/usr/bin/env python3
"""
# --- FILOSOFÍA DEL PROYECTO ---
# Principio de "Cápsulas Inviolables":
# Se prioriza la identificación, aislamiento y corrección de la funcionalidad rota,
# dejando intactas las partes del código que ya han demostrado ser estables y funcionales.
# Esto minimiza el riesgo de introducir nuevas regresiones y asegura un progreso robusto.
#
Script de Ejecución Agnóstico del Proyecto.

Este script es el punto de entrada profesional para el sistema de agentes.
Su diseño permite ejecutarlo desde cualquier ubicación en el sistema de archivos.

Funcionalidades Clave:
1.  **Detección de Ruta Raíz:** Determina automáticamente la ubicación del proyecto
    basándose en su propia ubicación.
2.  **Activación de Entorno Virtual:** Identifica el sistema operativo y localiza
    el ejecutable de Python correcto dentro del directorio '.venv'.
3.  **Ejecución Transparente:** Lanza el script principal del agente (`agents/agente.py`)
    y le pasa todos los argumentos de línea de comandos que este script recibió.
4.  **Portabilidad:** Al usar rutas absolutas y detección de SO, este script es
    altamente portable y puede ser enlazado simbólicamente desde /usr/local/bin
    para un acceso global (ej: `tron-agent --headless ...`).
"""
import sys
import os
import subprocess

def main():
    # 1. Determinar la ruta raíz del proyecto.
    # __file__ es la ruta a este script (run.py).
    # os.path.dirname() nos da el directorio que lo contiene.
    # os.path.abspath() lo convierte en una ruta absoluta.
    project_root = os.path.dirname(os.path.abspath(__file__))

    # 2. Determinar la ruta al ejecutable de Python del entorno virtual.
    venv_python_path = ""
    if sys.platform in ["linux", "darwin"]:
        # Para Linux y macOS
        venv_python_path = os.path.join(project_root, ".venv", "bin", "python")
    elif sys.platform == "win32":
        # Para Windows
        venv_python_path = os.path.join(project_root, ".venv", "Scripts", "python.exe")
    else:
        print(f"❌ Error: Sistema operativo '{sys.platform}' no soportado por este script.")
        sys.exit(1)

    # Verificar que el ejecutable del venv existe.
    if not os.path.exists(venv_python_path):
        print("❌ Error: Entorno virtual '.venv' no encontrado o incompleto.")
        print(f"   Se esperaba encontrar el ejecutable de Python en: {venv_python_path}")
        print("   Por favor, asegúrate de haber creado el entorno con 'uv venv .venv'.")
        sys.exit(1)

    # 3. Determinar la ruta al script del agente que queremos ejecutar.
    agent_script_path = os.path.join(project_root, "agents", "agente.py")

    if not os.path.exists(agent_script_path):
        print(f"❌ Error: Script del agente no encontrado en: {agent_script_path}")
        sys.exit(1)
        
    # 4. Preparar el comando y los argumentos.
    # El primer argumento es el ejecutable de python del venv.
    # El segundo es el script del agente.
    # El resto (sys.argv[1:]) son todos los argumentos que se pasaron a ESTE script (run.py),
    # que se los pasamos de forma transparente al script del agente.
    command = [venv_python_path, agent_script_path] + sys.argv[1:]

    # Imprimir el comando que se va a ejecutar (útil para depuración)
    # print(f"▶️  Ejecutando: {' '.join(command)}")

    # 5. Ejecutar el subproceso.
    # El proceso actual (run.py) será reemplazado por el nuevo proceso.
    # Esto significa que el manejo de señales (como Ctrl+C) será heredado
    # directamente por el script del agente, que es exactamente lo que queremos.
    try:
        # En sistemas tipo Unix, os.execv es más eficiente que subprocess.run
        # porque reemplaza el proceso actual en lugar de crear uno nuevo.
        if sys.platform in ["linux", "darwin"]:
            os.execv(command[0], command)
        else:
            # Para Windows, subprocess es más robusto.
            subprocess.run(command, check=True)
    except FileNotFoundError:
        print(f"❌ Error: No se pudo encontrar el ejecutable '{command[0]}'.")
        sys.exit(1)
    except Exception as e:
        # Esto solo se ejecutaría si hay un error al lanzar el proceso,
        # no si el proceso del agente falla.
        print(f"❌ Error al lanzar el subproceso: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
