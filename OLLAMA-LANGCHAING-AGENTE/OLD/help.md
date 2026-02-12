# Guía Interna del Proyecto

Este documento proporciona una guía rápida y consideraciones importantes para el desarrollo y mantenimiento del Asistente Local con LangChain y Ollama.

## Estructura del Proyecto
*   `.venv/`: Entorno virtual de Python gestionado por `uv`.
*   `DocINICIAL/`: Documentación relevante proporcionada para el proyecto.
*   `README.md`: Descripción general del proyecto, características y configuración.
*   `run.sh`: Script para activar el entorno virtual y ejecutar la aplicación principal.
*   `agents/`: (Futuro) Directorio para la definición de agentes y sub-agentes.
*   `core/`: (Futuro) Directorio para lógica central, como la integración de memoria y modelos.
*   `tools/`: (Futuro) Directorio para herramientas personalizadas que los agentes puedan utilizar.

## Principios de Desarrollo
*   **Modularidad:** Cada componente debe ser lo más independiente posible para facilitar la reutilización y el mantenimiento.
*   **Configurabilidad:** Priorizar la configuración externa (ej. variables de entorno, archivos de configuración) sobre el hardcoding para permitir adaptabilidad.
*   **Claridad del Código:** Escribir código limpio, legible y bien comentado (cuando sea necesario para explicar el "por qué").
*   **Pruebas:** Cada componente o característica nueva debe ir acompañada de sus respectivas pruebas unitarias o de integración.

## Convenciones de Nomenclatura
*   **Archivos Python:** `snake_case.py`
*   **Clases:** `CamelCase`
*   **Funciones y Variables:** `snake_case`

## Contribución
Para contribuir a este proyecto:
1.  Asegúrate de que tu entorno de desarrollo esté configurado siguiendo las instrucciones del `README.md`.
2.  Crea una nueva rama para tus cambios.
3.  Implementa tus características o correcciones, asegurándote de que sigan los principios de desarrollo y las convenciones de nomenclatura.
4.  Escribe o actualiza las pruebas correspondientes.
5.  Actualiza el `README.md` y este `help.md` si tus cambios impactan la documentación o la estructura del proyecto.
6.  Envía una solicitud de extracción (Pull Request) con una descripción clara de tus cambios.

## Registro de Avances
Los avances significativos y los problemas resueltos se registrarán en la sección "Avances y Problemas" del `README.md` al finalizar cada jornada o hito importante, no de manera incremental.
