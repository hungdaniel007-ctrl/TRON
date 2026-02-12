**La arquitectura final de Tron integra orquestación avanzada, manipulación de archivos local y memoria semántica GraphRAG en una estructura modular y eficiente.**

Esta configuración permite que cada componente funcione como una pieza de un motor: Tron (el CEO) decide la estrategia, los especialistas ejecutan las tácticas y Cognee proporciona la memoria a largo plazo, todo optimizado para no exceder los 4 GB de RAM mediante el uso de modelos locales y APIs externas.

## Estructura de Directorios y Archivos

```text
tron_project/
├── .venv/                      # Entorno virtual único (Python 3.11+)
├── requirements.txt            # Dependencias del ecosistema
├── config.yaml                 # Configuración centralizada (Modelos, DB, Chunks)
├── .env                        # Credenciales (OPENROUTER_API_KEY, TAVILY_API_KEY, etc.)
├── main.py                     # Punto de entrada y ejecución de Tron
├── core/                       # Kernel del sistema
│   ├── __init__.py
│   ├── factory.py              # Fábrica dinámica de modelos (init_chat_model)
│   ├── persistence.py          # SQLAlchemy Checkpointers (Postgres/SQLite)
│   └── mcp_loader.py           # Conector universal para servidores MCP
├── agents/                     # Subgrafos encapsulados
│   ├── tron/                   # Orquestador CEO
│   │   ├── agent.py            # Grafo principal
│   │   └── prompts.py          # Instrucciones del CEO
│   ├── memory_specialist/      # Especialista en Memoria (Basado en Cognee)
│   │   ├── agent.py            # Grafo del especialista
│   │   ├── engine_ingest.py    # Lógica de ingesta táctica (Chunks dinámicos)
│   │   ├── engine_query.py     # Lógica de búsqueda (Microscopio)
│   │   └── engine_inspect.py   # Diagnóstico de grafos (Visor)
│   ├── git_specialist/         # Especialista en Git y Control de Versiones
│   │   └── agent.py
│   └── file_specialist/        # Especialista en Archivos (Claude Code style)
│       └── agent.py
├── tools/                      # Herramientas compartidas
│   ├── shell_tools.py          # Ejecución de comandos segura
│   └── file_tools.py           # FileManagementToolkit configurado
└── databases/                  # Almacenamiento persistente
    ├── tron_memory.db          # Memoria de hilos (SQLite)
    └── cognee_data/            # Almacenamiento local de Cognee (Kuzu + LanceDB)
```

## Requisitos de Entorno (`requirements.txt`)

```text
# LangChain Core
langchain>=0.3.0
langgraph>=0.2.0
langchain-community

# Proveedores de Modelos
langchain-openai        # Conecta con OpenRouter y DeepSeek
langchain-ollama        # Maneja Gemma y modelos locales

# Memoria y GraphRAG
cognee                  # El motor de memoria semántica
lancedb                 # Base de datos vectorial ligera
kuzu                    # Base de datos de grafos para 4GB RAM
fastembed               # Embeddings locales eficientes

# Utilidades y DB
sqlalchemy              # Puerto universal para SQL
aiosqlite               # Soporte asíncrono para SQLite
psycopg2-binary         # Soporte para PostgreSQL
pyyaml                  # Gestión de configuración
toolbox-langchain       # SDK para integración MCP
```

## Arquitectura de Conectividad Táctica

### 1. El Puerto Universal (Graph-as-a-Tool)
Cada agente en la carpeta `agents/` se compila como un grafo independiente. Tron los importa y los envuelve en una función decorada con `@tool`. Esto permite que el CEO llame a un subagente pasando solo un `query`, y reciba una respuesta estructurada.

### 2. Inyección Dinámica de Modelos
El archivo `core/factory.py` utiliza `init_chat_model` para que, cuando Tron detecte una tarea de análisis de archivos grandes, inyecte automáticamente el modelo DeepSeek con temperatura baja (0.1). Para charlas o tareas triviales, inyecta Gemma vía Ollama.

### 3. Memoria a Largo Plazo (Cognee Engine)
Tu código de `auditoria_ingesta.py` y `microscopio.py` se integra en `agents/memory_specialist/`. Cuando Tron recibe información nueva que debe recordar "para siempre", envía los datos al especialista de memoria, quien ajusta el `chunk_size` dinámicamente según el tipo de archivo y lo procesa en `databases/cognee_data/`.

### 4. Persistencia Agnóstica
Gracias a SQLAlchemy en `core/persistence.py`, el sistema puede usar `tron_memory.db` (SQLite) mientras trabajas en tu máquina de 4 GB. Si escalas a un servidor, solo cambias la URI en `config.yaml` a una dirección de PostgreSQL.

**Relevant docs:**

- [Subgraphs: Multi-agent systems](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)
- [init_chat_model: Unified model initialization](https://docs.langchain.com/oss/python/langchain/multi-agent/router-knowledge-base)
- [File Management Toolkit](https://docs.langchain.com/oss/python/integrations/tools/mcp_toolbox)
- [SQLDatabase: Persistence with SQLAlchemy](https://docs.langchain.com/oss/python/langchain/sql-agent)
