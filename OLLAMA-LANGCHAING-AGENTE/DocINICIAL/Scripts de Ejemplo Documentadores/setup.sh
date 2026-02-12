#!/bin/bash
# setup.sh - Preparación del entorno de ejecución profesional
# Este script garantiza que el entorno virtual y las dependencias del sistema existan.

set -e # Detener ejecución si algo falla

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$BASE_DIR"

echo "--- Iniciando Configuración de Entorno ---"

# 1. Crear estructura de directorios necesaria
mkdir -p temp output

# 2. Verificar JQ para el procesamiento de JSON en Bash
if ! command -v jq &> /dev/null; then
    echo "[!] JQ no encontrado. Intentando instalar..."
    sudo apt-get update && sudo apt-get install -y jq
fi

# 3. Gestión del Entorno Virtual Python
if [ ! -d "venv" ]; then
    echo "[+] Creando entorno virtual venv..."
    python3 -m venv venv
fi

# 4. Actualización de herramientas base
source venv/bin/activate
pip install --upgrade pip

echo "[OK] Entorno configurado correctamente en $BASE_DIR"
