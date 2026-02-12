#!/bin/bash
# verify_segments.sh - Auditoría estructural bash pura

MD_FILE="$1"
JSON_FILE="$2"

if [[ ! -f "$MD_FILE" || ! -f "$JSON_FILE" ]]; then
    echo "Error: Archivos no encontrados."
    exit 1
fi

G='\033[0;32m'
R='\033[0;31m'
NC='\033[0m'

echo -e "\033[1;36m=== AUDITORÍA ESTRUCTURAL BASH ===\033[0m"

# Leer JSON línea por línea de forma segura
jq -c '.[]' "$JSON_FILE" | while read -r row; do
    LINE=$(echo "$row" | jq -r '.line')
    ADDR=$(echo "$row" | jq -r '.addr')
    TITLE=$(echo "$row" | jq -r '.title')
    
    CONTENT=$(sed -n "${LINE}p" "$MD_FILE")
    
    if [[ "$CONTENT" == *"$TITLE"* ]]; then
        # Números limpios L: y A:
        echo -e "${G}[OK]${NC} L:$LINE A:$ADDR | $TITLE"
    else
        echo -e "${R}[ERR]${NC} L:$LINE A:$ADDR | Esperado: $TITLE"
    fi
done
