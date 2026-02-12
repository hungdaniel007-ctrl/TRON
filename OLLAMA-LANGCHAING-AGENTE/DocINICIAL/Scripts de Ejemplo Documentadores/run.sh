#!/bin/bash
# run.sh - Punto de entrada único

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$BASE_DIR"

INPUT_MD="$1"
EXTRA_ARGS="${@:2}"

if [[ -z "$INPUT_MD" ]]; then
    echo "Uso: ./run.sh \"archivo.md\" [-Nivel N] [-Contexto N] [-SoloErrores 1]"
    exit 1
fi

chmod +x *.py *.sh
./setup.sh > /dev/null

source venv/bin/activate

echo -e "\033[1;34mStep 1: Indexando con Filtros de Bloque de Código...\033[0m"
python3 extract_titles_v5.py "$INPUT_MD"

JSON_OUT="output/extracted_titles_index_v5.json"

if [[ -f "$JSON_OUT" ]]; then
    echo -e "\033[1;34mStep 2: Verificación Guacamaya (Filtros: $EXTRA_ARGS)\033[0m"
    python3 verify_index.py "$INPUT_MD" "$JSON_OUT" $EXTRA_ARGS
else
    echo "Error en la indexación."
fi
