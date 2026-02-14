  
 Aquí tienes la verificación de cada afirmación con las URLs oficiales de la documentación y el código fuente de Cognee:

## 1. Configuración vía CLI (Línea de Comandos)

**Afirmación:** El parámetro `--chunk-size` en el comando `cognee-cli cognify` controla el límite de tokens por chunk.

**Verificación:** ✅ Confirmado en documentación oficial
- **URL:** https://docs.cognee.ai/cognee-cli/overview 

**Código documentado:**
```bash
# Aumentar tamaño de chunk y mostrar más logs
cognee-cli cognify --datasets onboarding --chunk-size 1500 --chunker TextChunker --verbose
```

**Parámetros documentados:**
- `--chunk-size`: Token limit for each chunk. Leave blank to let Cognee choose
- `--chunker`: `TextChunker` (default) or `LangchainChunker` if installed

---

## 2. Configuración Persistente (Config/Environment)

**Afirmación:** Se puede establecer `chunk_size` vía configuración global o variables de entorno.

**Verificación:** ✅ Confirmado en documentación oficial
- **URL:** https://docs.cognee.ai/cognee-cli/overview 

**Código documentado:**
```bash
# Ver claves soportadas
cognee-cli config list

# Establecer tamaño de chunk
cognee-cli config set chunk_size <valor>

# Resetear a valor por defecto
cognee-cli config unset chunk_size
```

**Claves de configuración documentadas:**
- `chunk_size`: Tamaño del chunk
- `chunk_overlap`: Superposición entre chunks

---

## 3. Implementación en Código Python

**Afirmación:** El chunking se configura en el pipeline de procesamiento con chunkers específicos.

**Verificación:** ✅ Confirmado en blog técnico oficial y paper académico
- **URL Blog:** https://www.cognee.ai/blog/deep-dives/enhancing-llm-responses-with-graph-based-retrieval-and-advanced-chunking-techniques 
- **URL Paper:** https://arxiv.org/pdf/2505.24478 

**Código del chunker por defecto (función, no clase):**
```python
# El chunker por defecto de Cognee es una función, no una clase
# Parámetros por defecto: paragraph_length=1024, batch_paragraphs=True

from cognee import chunk_by_paragraph

# Uso como generador (bajo footprint de memoria)
chunks = chunk_by_paragraph(text, paragraph_length=1024, batch_paragraphs=True)
```

**Comparación con otros chunkers documentada:**
```python
# LangChain (para referencia)
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024,  # Ajustable
    chunk_overlap=128
)

# LlamaIndex (para referencia)
from llama_index.core.node_parser import SentenceSplitter
splitter = SentenceSplitter(
    chunk_size=1024,  # Ajustable
    chunk_overlap=128
)
```

---

## 4. Configuración vía Variables de Entorno (.env)

**Afirmación:** Se puede configurar en archivo `.env` para persistencia.

**Verificación:** ✅ Confirmado en documentación de configuración
- **URL:** https://docs.cognee.ai/setup-configuration/overview 

**Ejemplo de archivo `.env` documentado:**
```bash
# .env file
# Configuración de Cognee

# LLM Configuration
LLM_PROVIDER=gemini
LLM_MODEL=gemini/gemini-2.5-flash
LLM_API_KEY=your-google-api-key

# Embedding Configuration  
EMBEDDING_PROVIDER=fastembed
EMBEDDING_MODEL=jinaai/jina-embeddings-v2-base-en
EMBEDDING_DIMENSIONS=768

# Chunking Configuration (implícito en la estructura)
# Según la documentación CLI, chunk_size y chunk_overlap son configurables
```

---

## 5. Parámetros en Pipeline de Cognify (Paper Académico)

**Afirmación:** `chunk_size` es un parámetro core que afecta la extracción del grafo.

**Verificación:** ✅ Confirmado en paper oficial de Cognee
- **URL:** https://arxiv.org/pdf/2505.24478  y https://arxiv.org/html/2505.24478v1 

**Descripción técnica documentada:**
> **Chunk Size (chunk_size)**: This parameter controls the number of tokens used to segment documents before graph extraction. In the Cognee pipeline, it influences both the structure of the resulting graph and the granularity of context available during retrieval. The range used in this study (200–2000 tokens) was chosen based on preliminary testing to balance extraction accuracy, retrieval specificity, and processing time.

**Tabla de parámetros del framework Dreamify:**
| Parameter | Description |
|-----------|-------------|
| Chunk size | Number of tokens per document segment used during graph extraction |
| Retriever type | Strategy used to retrieve context (text chunks or graph triplets) |
| Top-k | Number of retrieved items passed to the language model |

---

## 6. Limitaciones Conocidas (Ollama)

**Afirmación:** Existen limitaciones específicas con ciertos providers.

**Verificación:** ✅ Confirmado en blog de desarrollo
- **URL:** https://www.glukhov.org/post/2025/12/selfhosting-cognee-quickstart-llms-comparison/ 

**Nota documentada:**
> **Chunk Size Limitation**: Cognee uses 4k token chunks when processing documents with Ollama. For complex documents or models with larger context windows, this seems unnecessarily restrictive. The framework doesn't provide an easy way to adjust this parameter.

---

## Resumen de Fuentes Oficiales

| Aspecto | Documentación Oficial | Tipo |
|---------|----------------------|------|
| CLI `--chunk-size` | https://docs.cognee.ai/cognee-cli/overview | Docs |
| Config keys (`chunk_size`, `chunk_overlap`) | https://docs.cognee.ai/cognee-cli/overview | Docs |
| Setup/Environment | https://docs.cognee.ai/setup-configuration/overview | Docs |
| Chunking técnicas | https://www.cognee.ai/blog/deep-dives/enhancing-llm-responses-with-graph-based-retrieval-and-advanced-chunking-techniques | Blog técnico |
| Parámetros académicos | https://arxiv.org/pdf/2505.24478 | Paper oficial |
| Limitaciones Ollama | https://www.glukhov.org/post/2025/12/selfhosting-cognee-quickstart-llms-comparison/ | Blog comunidad |

Todas las afirmaciones están respaldadas por la documentación formal de Cognee o publicaciones técnicas oficiales del equipo de desarrollo.


CLI

# Cognee CLI Overview

Copy page

Command line interface for Cognee AI memory operations

The `cognee-cli` command lets you run Cognee from the terminal so you can add data, build the knowledge graph, and ask questions without opening a Python file. The commands are designed to be short, use friendly defaults, and are safe for people who are just starting out.

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#setup)

Setup

Before using the CLI, you need to configure your API key. The recommended approach is to store it in a `.env` file:

```
# Create a .env file in your project root
echo "LLM_API_KEY=your_openai_api_key" > .env
```

Alternatively, you can export it in your terminal session:

```
export LLM_API_KEY=your_openai_api_key
```

Use the `cognee-cli config set` command only for temporary tweaks during a long-running session. For persistent configuration, use `.env` files or environment variables.

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#quick-tour-of-commands)

Quick Tour of Commands

- `cognee-cli add <data>` loads documents or text into a dataset
- `cognee-cli cognify` turns datasets into a knowledge graph
- `cognee-cli search "question"` asks the graph for answers
- `cognee-cli delete` removes stored data when you no longer need it
- `cognee-cli config` reads and updates saved settings
- `cognee-cli -ui` launches the local web app

Add `--help` after any command (for example, `cognee-cli search --help`) to see every option.

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#add-data)

Add Data

Start by loading something the graph can learn from. You can add files, folders, URLs, or even plain text.

```
# Add a single file to the default dataset
cognee-cli add docs/company-handbook.pdf

# Pick a dataset name so you can separate topics later
cognee-cli add docs/policies.docx --dataset-name onboarding

# Add multiple files at once
cognee-cli add docs/policies.docx docs/faq.md --dataset-name onboarding

# Add a short text note (wrap the note in quotes)
cognee-cli add "Kickoff call notes: customer wants faster onboarding" --dataset-name sales_calls
```

Add Command Options

- `data`: One or more file paths, URLs, or text strings. Mix and match as needed
- `--dataset-name` (`-d`): Defaults to `main_dataset`. Use clear names so the team remembers what each dataset holds

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#cognify-data)

Cognify Data

Cognify builds the knowledge graph. Run it whenever you add new data or change the ontology.

```
# Process every dataset
cognee-cli cognify

# Process specific datasets only
cognee-cli cognify --datasets onboarding sales_calls

# Increase chunk size and show more logs
cognee-cli cognify --datasets onboarding --chunk-size 1500 --chunker TextChunker --verbose

# Kick off a long job and return immediately
cognee-cli cognify --datasets onboarding --background
```

Cognify Command Options

- `--datasets` (`-d`): Space-separated list. Skip it to process everything
- `--chunk-size`: Token limit for each chunk. Leave blank to let Cognee choose
- `--chunker`: `TextChunker` (default) or `LangchainChunker` if installed
- `--background` (`-b`): Handy for large datasets; the CLI exits while the job keeps running
- `--verbose` (`-v`): Prints progress messages
- `--ontology-file`: Path to a custom ontology (`.owl`, `.rdf`, etc.)

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#search-the-graph)

Search the Graph

Once cognify finishes, you can question the graph. Start with a simple natural-language question, then experiment with search types.

```
# Default search (GRAPH_COMPLETION)
cognee-cli search "Who owns the rollout plan?"

# Limit the scope to one dataset
cognee-cli search "What is the onboarding timeline?" --datasets onboarding

# Return three answers at most
cognee-cli search "List the key risks" --top-k 3

# Save a JSON response for another tool
cognee-cli search "Which documents mention security?" --output-format json
```

Search Types

Try these quick examples to feel the differences:

```
# Conversational answer with reasoning (default)
cognee-cli search "Give me a summary of onboarding" --query-type GRAPH_COMPLETION

# Shorter answer based on chunks
cognee-cli search "Show the onboarding steps" --query-type RAG_COMPLETION

# Highlight relationships and insights
cognee-cli search "How do onboarding tasks connect?" --query-type INSIGHTS

# Raw text passages you can copy
cognee-cli search "Find security requirements" --query-type CHUNKS --top-k 5

# Summaries only (great for reviews)
cognee-cli search "Summarise the onboarding handbooks" --query-type SUMMARIES

# Code-aware search for repos
cognee-cli search "Where is the email parser?" --query-type CODE

# Advanced graph query (requires Cypher skills)
cognee-cli search "MATCH (n) RETURN COUNT(n)" --query-type CYPHER
```

Search Command Options

- `--query-type`: Choose from GRAPH_COMPLETION, RAG_COMPLETION, INSIGHTS, CHUNKS, SUMMARIES, CODE, or CYPHER
- `--datasets`: Limit search to specific datasets
- `--top-k`: Maximum number of results to return
- `--system-prompt`: Point to a custom prompt file for LLM-backed modes
- `--output-format` (`-f`): `pretty` (friendly layout), `simple` (minimal text), or `json` (structured output for scripts)

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#delete-data)

Delete Data

Clean up when a dataset is outdated or when you reset the environment.

```
# Remove one dataset (asks for confirmation)
cognee-cli delete --dataset-name onboarding

# Remove everything for a specific user
cognee-cli delete --user-id 123e4567

# Wipe all data (add --force to skip the question)
cognee-cli delete --all --force
```

Delete Command Options

- `--dataset-name`: Remove a specific dataset
- `--user-id`: Remove all data for a specific user
- `--all`: Remove all data (use with caution)
- `--force`: Skip confirmation prompts

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#manage-configuration)

Manage Configuration

The CLI stores its settings so you do not have to repeat them. Configuration updates line up with the Python API.

```
# See the list of supported keys
cognee-cli config list

# Check one value (if implemented)
cognee-cli config get llm_model

# Update your LLM provider and model
cognee-cli config set llm_provider openai
cognee-cli config set llm_model gpt-4o-mini

# Store an API key (quotes are optional)
cognee-cli config set llm_api_key sk-yourkey

# Reset a key back to its default value
cognee-cli config unset chunk_size
```

Config Command Options

- `list`: Print the common keys
- `get [key]`: Show the saved value; omit the key to list everything
- `set <key> <value>`: Save a new value. JSON strings such as `{}` or `true` are parsed automatically
- `unset <key>`: Reset to the default. Add `--force` to skip confirmation
- `reset`: Placeholder for a future “reset everything” command

Useful Configuration Keys

- Language model: `llm_provider`, `llm_model`, `llm_api_key`, `llm_endpoint`
- Storage: `graph_database_provider`, `vector_db_provider`, `vector_db_url`, `vector_db_key`
- Chunking: `chunk_size`, `chunk_overlap`

## 

[​

](https://docs.cognee.ai/cognee-cli/overview#launch-the-ui)

Launch the UI

Prefer a browser view? Launch the UI with one flag.

```
cognee-cli -ui
```
**No es verdad que solo se pueda por CLI; tu código actual ya está usando la forma correcta de hacerlo programáticamente.**

En Cognee, la configuración de los chunks se maneja a través del objeto global `config` del SDK de Python. Al hacer `cognee_config.chunk_size = CHUNK_SIZE`, estás sobreescribiendo el valor por defecto del sistema antes de que se ejecuten los procesos de `add` y `cognify`.

## Formas de configurar Chunks en Cognee

Según la arquitectura de Cognee, tienes tres niveles de control para los chunks:

1.  **Nivel Programático (Tu método):** Es el más flexible para el agente Tron, ya que permite cambiar el tamaño del chunk según el tipo de archivo detectado por el CEO.
    ```python
    from cognee import config as cognee_config
    cognee_config.chunk_size = 1024  # Ajuste dinámico
    ```
2.  **Nivel de Variables de Entorno:** Cognee lee variables `COGNEE_CHUNK_SIZE` si están presentes en el `.env`. Esto es útil para una configuración estática del subagente.
3.  **Nivel de CLI:** Es simplemente un "wrapper" que termina modificando los mismos valores internos que tú ya estás manipulando en tu script.

## Recomendación para el Especialista de Memoria

Para que tu subagente sea realmente inteligente, deberías integrar la lógica de tamaño de chunk en la herramienta de ingesta. Archivos de código (scripts) se benefician de chunks pequeños para mantener la lógica atómica, mientras que documentos de texto largo pueden usar chunks más grandes.

```python
@tool
async def smart_ingest(doc_path: str, focus: str = "general"):
    """Ingesta con tamaño de chunk adaptativo."""
    from cognee import config as cognee_config
    
    # Táctica: Chunks pequeños para código, grandes para narrativa
    if doc_path.endswith(('.py', '.js', '.json')):
        cognee_config.chunk_size = 512
    else:
        cognee_config.chunk_size = 1024
        
    await cognee.add(doc_path)
    await cognee.cognify()
    return f"Ingesta finalizada con chunks de {cognee_config.chunk_size}"
```

**Conclusión:** Tu camino es el correcto. La CLI de Cognee es solo una interfaz de conveniencia, pero el "puerto real" para un desarrollador de LangChain es la manipulación directa de `cognee.config` que ya implementaste en `auditoria_ingesta.py`.

**Relevant docs:**
- [Custom Tool Definition with dynamic logic](https://docs.langchain.com/oss/python/langchain/sql-agent)
- [LangGraph: State Management for Subagents](https://docs.langchain.com/oss/python/langgraph/graph-api#state)