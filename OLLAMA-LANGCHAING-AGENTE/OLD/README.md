# Asistente Local con LangChain y Ollama

## Descripción
Este proyecto tiene como objetivo desarrollar un asistente local utilizando el framework LangChain, con capacidades de memoria persistente a través de SQLAlchemy y SQLite (inicialmente, con planes de migración a PostgreSQL). El asistente será impulsado por modelos de lenguaje locales ejecutados con Ollama.

## Principios Clave
*   **Agentes Reutilizables y Configurables:** Todos los agentes y sub-agentes desarrollados dentro de este proyecto están diseñados para ser modulares, fácilmente configurables y reutilizables en diferentes contextos o para distintas tareas. Esto permitirá una construcción flexible y escalable del asistente.
*   **Memoria Persistente:** La gestión de la memoria se realizará a través de una base de datos SQL (inicialmente SQLite), permitiendo que los agentes mantengan el estado y el contexto a lo largo de las interacciones.
*   **Modelos de Lenguaje Locales:** Integración con Ollama para utilizar una variedad de modelos de lenguaje grandes (LLMs) ejecutados localmente, permitiendo flexibilidad y control sobre los recursos computacionales.

## Características Principales
*   **Agente Especialista Git:** Un sub-agente dedicado a la gestión de operaciones Git, incluyendo la lectura/escritura de archivos, creación/eliminación de directorios, y otras funcionalidades de control de versiones.
*   **Intercambio Dinámico de Modelos:** Capacidad para cambiar entre diferentes modelos de Ollama durante la ejecución, lo que facilita la experimentación y optimización.

## Configuración del Entorno
1.  **Clonar el Repositorio (Si aplica):**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd OLLAMA-LANGCHAING-AGENTE
    ```
2.  **Crear y Activar Entorno Virtual con `uv`:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```
3.  **Instalar Dependencias:**
    ```bash
    uv pip install langchain sqlalchemy pysqlite3-binary ollama
    ```

## Ejecución
Para activar el entorno virtual y preparar el proyecto:
```bash
./run.sh
```
Una vez activado el entorno, podrás ejecutar los scripts de los agentes.

## Avances y Problemas
Esta sección se actualizará periódicamente para registrar el progreso del proyecto, las decisiones de diseño, los desafíos encontrados y sus soluciones.
