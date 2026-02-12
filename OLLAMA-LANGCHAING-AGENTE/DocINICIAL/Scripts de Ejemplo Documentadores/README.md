# TRON Markdown Indexer & Auditor v6

Sistema de grado industrial para la generación de índices jerárquicos a partir de archivos Markdown y validación cruzada mediante herramientas de sistema (Bash/Sed/JQ).

## Características
- **Resiliencia**: Crea automáticamente carpetas de logs y resultados.
- **Precisión**: Maneja headers vacíos y bloques de código.
- **Auditoría**: Script Bash independiente que valida la posición exacta de cada título.
- **Logging**: Nivel DEBUG detallado con trazabilidad de errores.

## Requisitos
- Python 3.10+
- Linux (Ubuntu/Debian recomendado)
- `jq` (el sistema intentará instalarlo automáticamente)

## Uso
Simplemente ejecuta el script maestro:
```bash
./run.sh