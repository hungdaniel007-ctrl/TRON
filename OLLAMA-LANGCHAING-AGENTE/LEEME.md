# OLLAMA-LANGCHAIN-AGENTE

Proyecto de agentes de inteligencia artificial local basado en LangChain y Ollama, con soporte para múltiples proveedores de modelos y arquitectura modular extensible.

## Características Principales

- **Arquitectura de agentes modulares**: Agentes con capacidad de evolución, pudiendo actuar como agentes independientes o como subagentes según las necesidades
- **Soporte multi-proveedor**: Compatible con Ollama (local), DeepSeek (API), y extensible a otros proveedores
- **Streaming con cancelación real**: Implementación robusta de streaming que permite interrupción inmediata de la generación (especialmente crítica para Ollama)
- **Configuración flexible**: Sistema de configuración basado en YAML que permite definir múltiples modelos con alias y configuraciones específicas
- **Modo CLI interactivo y one-shot**: Interfaz de comandos versátil para uso interactivo o por lotes
- **Paradigma adaptable**: Uso del paradigma más eficaz y eficiente según el caso de uso - funcional, orientado a objetos, o mixto
- **Componentes físicos desacoplables**: Las herramientas y funcionalidades pueden incluirse o excluirse físicamente del sistema, permitiendo versiones modulares del agente

## Estructura del Proyecto

```
OLLAMA-LANGCHAING-AGENTE/
├── agents/                     # Código de los agentes
│   ├── general.py             # Agente principal general
│   └── herramientas/          # Herramientas y MCPs de los agentes
├── config/                    # Archivos de configuración
│   └── models.yaml            # Configuración de modelos y proveedores
├── DocINICIAL/                # Documentación general
│   ├── BITACORA/              # Bitácora de eventos, errores e importantes
│   └── ...                    # Otros documentos
├── OLD/                       # Scripts y versiones antiguas
├── .venv/                     # Entorno virtual gestionado con uv
├── requirements.txt           # Dependencias del proyecto
└── run.sh                     # Script de ejecución principal
```

## Configuración y Requisitos

### Requisitos Previos

- Python 3.9+
- Ollama instalado y corriendo (`ollama serve`)
- Clave API de DeepSeek (opcional, para usar proveedor DeepSeek)

### Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd OLLAMA-LANGCHAING-AGENTE
   ```

2. **Crear entorno virtual con uv**:
   ```bash
   uv venv .venv
   source .venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   ```bash
   cp .env.example .env
   # Editar .env para añadir clave API de DeepSeek si se va a usar
   ```

5. **Descargar modelos necesarios**:
   ```bash
   ollama pull gemma3:4b
   # Añadir otros modelos según configuración en models.yaml
   ```

### Configuración de Modelos

Editar `config/models.yaml` para definir los modelos disponibles:

```yaml
default_model: gemma-ollama

models:
  - id: gemma-ollama
    name: "Gemma (Ollama)"
    alias: gema
    provider: ollama
    config:
      model: "gemma3:4b"
      base_url: "http://localhost:11434"
      temperature: 0.7

  - id: deepseek-chat
    name: "DeepSeek (API)"
    alias: deepseek
    provider: deepseek
    config:
      model: "deepseek-chat"
      api_key: "ENV" # Se carga desde variable de entorno
```

## Uso

### Modo Interactivo

```bash
python agents/general.py
```

Comandos disponibles en modo chat:
- `/exit` - Salir del chat
- `/model [alias]` - Cambiar modelo activo
- `/stream` - Alternar modo streaming
- `/clear` - Limpiar historial
- `/help` - Mostrar ayuda
- `Ctrl+C` - Cancelar generación actual

### Modo One-Shot

```bash
python agents/general.py -sc -m "Mensaje de entrada" --model gemma-ollama
```

### Con Streaming

```bash
python agents/general.py --model gemma-ollama --stream
```

## Arquitectura del Agente

### Componentes Principales

1. **Agente General**: Punto de entrada principal que gestiona la lógica de interacción y selección de modelos
2. **Sistema de Configuración**: Carga dinámica de modelos y proveedores desde YAML
3. **Gestión de Streaming**: Implementación robusta que resuelve problemas de socket bloqueante con Ollama
4. **Herramientas y MCPs**: Componentes modulares que amplían la funcionalidad del agente

### Paradigma de Desarrollo

El proyecto adopta un paradigma adaptable donde se selecciona la metodología más eficaz y eficiente según el caso de uso:
- **Funcional**: Para operaciones puras y transformaciones de datos
- **Orientado a Objetos**: Para componentes con estado y comportamiento complejo
- **Modernos**: Uso de patrones actuales de programación cuando ofrecen ventajas claras
- **Mixto**: Combinación de paradigmas según las necesidades específicas

### Modularidad y Extensibilidad

El sistema está diseñado para permitir la inclusión/exclusión física de herramientas y funcionalidades:
- Las herramientas se organizan en carpetas dentro de `agents/herramientas/`
- La configuración refleja qué herramientas están disponibles
- Al vender versiones del agente, se pueden incluir/excluir componentes físicamente
- La instalación de nuevas funcionalidades es sencilla y modular

## Implementación de Streaming con Cancelación Real

Uno de los aspectos técnicamente más importantes del proyecto es la implementación de streaming que resuelve un problema conocido con Ollama y LangChain. El problema radica en que `ChatOllama.stream()` no expone un método nativo para cerrar la conexión TCP subyacente ante una señal de terminal, causando bloqueos.

La solución implementada:
1. Para Ollama: Uso de la API HTTP nativa con `requests.post` y `stream=True` para permitir cierre real de conexión con `response.close()`
2. Threading + Queue: El streaming corre en un thread separado que comunica chunks mediante `queue.Queue`
3. Cancelación real: Al recibir `Ctrl+C`, se cierra la conexión HTTP real, deteniendo la generación inmediatamente

## Documentación y Recursos

- La documentación general se encuentra en `DocINICIAL/`
- La bitácora de eventos, errores e incidentes importantes está en `DocINICIAL/BITACORA/`
- Los scripts actualizados se mantienen en `OLD/`
- La documentación de componentes específicos (cognee, redis, ollama, etc.) se consulta según sea necesario para cada caso de uso

## Contribuciones

Las contribuciones son bienvenidas. Por favor, asegúrese de seguir las convenciones de codificación del proyecto:
- Comentarios y documentación en español
- Código reusable y modular
- Seguimiento de la documentación oficial de cada componente
- Adopción del paradigma más eficaz y eficiente según el caso de uso

## Licencia

Todos los derechos reservados Elías Hung +585623825