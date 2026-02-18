#!/bin/bash
# run.sh
# Un script de conveniencia para ejecutar el agente a través del entorno virtual.

# Determinar la ruta raíz del proyecto (donde reside run.sh)
PROJECT_ROOT=$(dirname "$(realpath "$0")")

# Ruta al ejecutable de Python del entorno virtual
VENV_PYTHON="${PROJECT_ROOT}/.venv/bin/python"

# Ruta al script principal del agente
AGENT_SCRIPT="${PROJECT_ROOT}/agents/agente.py"

# Verificar que el entorno virtual exista
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Error: Entorno virtual '.venv' no encontrado o incompleto."
    echo "   Se esperaba encontrar el ejecutable de Python en: $VENV_PYTHON"
    echo "   Por favor, asegúrate de haber creado el entorno con 'uv venv .venv'."
    exit 1
fi

# Ejecutar el script del agente con los argumentos pasados a este script
# Nota: os.execv en run.py es más eficiente, pero este script es para flexibilidad.
# Usaremos directamente agents/agente.py para bypass el run.py
exec "$VENV_PYTHON" "$AGENT_SCRIPT" "$@"
