Vamos a elaborar una descripción altamente semántica y declarativa del sistema, tal como se ha diseñado en la conversación. El objetivo es que, si se borra todo el historial y solo queda esta respuesta, una IA (o un desarrollador) pueda entender completamente la arquitectura, los componentes, las interacciones y el propósito del sistema. La descripción será detallada, sin código, pero con suficiente especificidad para reconstruir el sistema.

Sistema de Agentes Modulares con Memoria Dual y Configuración Declarativa
Visión General
El sistema es una plataforma de agentes de inteligencia artificial diseñada para ser instalada localmente en entornos empresariales (on-premise), con un enfoque en la modularidad, la configurabilidad y la extensibilidad. Su propósito es permitir a las organizaciones desplegar asistentes inteligentes personalizados que puedan acceder a conocimientos internos (documentos), mantener historiales de conversación, y ejecutar acciones específicas a través de herramientas (skills). El sistema se controla mediante una interfaz de línea de comandos (CLI) interactiva, que permite a los usuarios finales conversar con los agentes, mientras que los administradores pueden definir y configurar agentes mediante archivos YAML, sin necesidad de programar.

La arquitectura sigue el paradigma de "fábrica de agentes": un núcleo central que lee configuraciones, registra herramientas disponibles, y construye agentes bajo demanda. Cada agente es una instancia de un modelo de lenguaje (LLM) con un conjunto específico de herramientas y capacidades de memoria, todo definido de forma declarativa. Las herramientas (skills) son componentes independientes que se pueden añadir simplemente colocándolos en carpetas específicas, y pueden ser activadas o desactivadas en tiempo de ejecución por el usuario a través de comandos CLI.

Componentes Principales y sus Funciones
1. Capa de Configuración Declarativa (Archivos YAML)
El sistema utiliza dos archivos YAML para definir toda la topología de agentes y modelos:

models.yaml: Define los modelos de lenguaje disponibles. Cada entrada incluye:

Un identificador único (ej: gemma-ollama).

El proveedor (ollama, deepseek, openai, etc.).

Parámetros de configuración específicos del proveedor: URL base, modelo concreto, temperatura, top_p, top_k, etc.

Posibilidad de usar variables de entorno para claves API.

agentes.yaml: Define los agentes. Cada agente tiene:

Un identificador único (ej: archivista, investigador).

Referencia al modelo a utilizar (por su ID en models.yaml).

Lista de herramientas disponibles (skills) que el agente puede usar. Esta lista se compone de nombres de herramientas registradas en el sistema.

Lista de herramientas activas por defecto (subconjunto de las disponibles) que se cargan al iniciar el agente.

Configuración de memoria:

Memoria de documentos: indica si está habilitada, la ruta donde se almacenará el índice vectorial, y los metadatos ontológicos que se pueden usar para filtrar (ej: categoría, fecha, tags).

Memoria de chat: indica si está habilitada y la ruta de la base de datos SQL donde se guardarán los historiales.

Prompt de sistema personalizado, que define la personalidad y las instrucciones del agente.

Posibilidad de sobrescribir parámetros del modelo (temperatura, etc.) específicos para este agente.

Esta capa permite a los administradores crear y modificar agentes sin tocar una línea de código, simplemente editando archivos de texto.

2. Núcleo: Fábrica de Agentes
El corazón del sistema es una fábrica de agentes (implementada como una clase en Python). Sus responsabilidades son:

Carga de configuración: Al iniciarse, lee los archivos YAML y los valida.

Registro de herramientas: Escanea automáticamente las carpetas de herramientas y subagentes para descubrir todas las skills disponibles. Cada herramienta se registra con un nombre único y metadatos que permiten su carga posterior (lazy loading). El escaneo puede ser recursivo, permitiendo organizar las herramientas en subcarpetas.

Gestión de modelos: Proporciona un método para instanciar un modelo de lenguaje dado su ID, cargando la configuración correspondiente y las credenciales necesarias.

Construcción de agentes: El método principal crear_agente_por_id(agente_id) construye un agente a partir de su definición en YAML. El proceso incluye:

Instanciar el modelo.

Cargar las herramientas activas por defecto (usando lazy loading: solo se instancian cuando se necesitan).

Configurar los gestores de memoria (documentos y chat) según lo especificado.

Crear la cadena de agente de LangChain (que internamente es un pipeline que incluye el prompt, el modelo con bind_tools, y un ejecutor de agente).

Devolver un objeto ejecutor de agente listo para ser invocado.

Creación de agentes con herramientas personalizadas: Además de construir agentes desde la configuración, la fábrica puede crear agentes con una lista explícita de herramientas, lo que permite la activación/desactivación dinámica en tiempo de ejecución.

La fábrica implementa lazy loading para optimizar recursos: las herramientas no se instancian hasta que el agente las necesita realmente. Esto es crucial para sistemas con muchas herramientas, ya que reduce la memoria y el tiempo de inicio.

3. Herramientas (Skills)
Las herramientas son componentes independientes que encapsulan una funcionalidad específica que el agente puede invocar. Cada herramienta:

Tiene un nombre único y una descripción legible por el modelo, que ayuda al LLM a decidir cuándo usarla.

Define un esquema de entrada (argumentos) que el modelo debe proporcionar al invocarla.

Implementa la lógica de ejecución (por ejemplo, guardar en memoria, buscar en web, hacer cálculos, etc.).

Puede ser tan simple como una función o tan compleja como un subagente completo.

Las herramientas se organizan en carpetas dentro de un directorio herramientas/. Cada herramienta reside en su propio archivo Python. El sistema de registro automático descubre todas las herramientas al iniciar la fábrica, inspeccionando las clases que heredan de BaseTool de LangChain.

Ejemplos de herramientas:

Memoria permanente: Permite al agente guardar y recuperar información en una base de conocimiento persistente (vector store).

Búsqueda web: Realiza consultas a internet y devuelve resultados.

Calculadora: Ejecuta operaciones matemáticas.

Agente matemático: Un subagente especializado en resolver problemas matemáticos complejos, que a su vez puede usar otras herramientas.

4. Subagentes como Herramientas
Una característica avanzada es que los propios agentes pueden ser empaquetados como herramientas. Esto permite construir jerarquías: un agente "general" puede delegar tareas especializadas a subagentes. Cada subagente:

Se define como un agente en agentes.yaml (tiene su propio modelo, herramientas y memoria).

Se implementa como una clase que, mediante un método as_tool(), devuelve una herramienta que, cuando es invocada, ejecuta al subagente con la consulta del usuario y devuelve su respuesta.

De esta manera, el sistema soporta composición de agentes: agentes que usan a otros agentes como herramientas, creando capacidades emergentes.

5. Gestores de Memoria
El sistema distingue dos tipos de memoria, ambos configurables por agente:

a. Memoria de Documentos (RAG con Metadatos Ontológicos)
Propósito: Permitir al agente responder preguntas basadas en un corpus de documentos internos de la empresa.

Funcionamiento:

Los documentos se almacenan en una carpeta datos/documentos/ (organizados como el usuario desee).

Un proceso externo (script de indexación) se encarga de dividir los documentos en fragmentos, generar embeddings y almacenarlos en una base de datos vectorial (por ejemplo, Chroma o FAISS). Durante la indexación, se pueden añadir metadatos ontológicos (categoría, fecha, tags, etc.) extraídos del nombre del archivo, de la estructura de carpetas, o de metadatos incrustados.

Cuando el agente necesita información, consulta el vectorstore con la pregunta del usuario. La búsqueda puede filtrarse por metadatos (por ejemplo, "solo documentos de la categoría 'contratos' y del año 2024") para mayor precisión.

Los fragmentos recuperados se inyectan en el contexto del modelo como parte del prompt RAG.

Característica clave: La ontología (metadatos) permite búsquedas semánticas filtradas, lo que va más allá de una simple búsqueda vectorial y permite un control fino sobre el conocimiento recuperado.

b. Memoria de Chat
Propósito: Mantener el historial de conversaciones con cada usuario, permitiendo continuidad y contexto a largo plazo.

Funcionamiento:

Se utiliza una base de datos SQL (SQLite por defecto) para almacenar mensajes. Cada conversación tiene un identificador de sesión, un usuario (opcional), una fecha/hora, y los mensajes (rol y contenido).

Al inicio de una sesión, la CLI puede crear una nueva sesión o continuar una existente.

Durante la conversación, los mensajes se van guardando en la base de datos.

Opcionalmente, se puede habilitar un proceso que, al finalizar una sesión, genere un título descriptivo (usando un LLM) y lo asocie a la sesión, permitiendo búsquedas posteriores por tema. Además, se puede vectorizar el historial y almacenarlo en otro vectorstore para permitir búsqueda semántica sobre conversaciones pasadas.

Característica clave: La memoria de chat es persistente y estructurada, permitiendo no solo recordar la conversación actual sino también recuperar conversaciones antiguas relevantes.

6. Interfaz de Línea de Comandos (CLI)
La CLI es la puerta de entrada para los usuarios finales. Sus características:

Selección de agente: Al iniciar, se especifica qué agente usar (por su ID). Esto permite tener múltiples agentes especializados en la misma instalación.

Modo interactivo: Una vez iniciado, el usuario puede conversar con el agente. Cada mensaje se envía al agente y se muestra la respuesta en streaming (token por token), con posibilidad de cancelar la generación en cualquier momento con Ctrl+C sin salir del programa.

Comandos en tiempo de ejecución: El usuario puede teclear comandos que comienzan con / para modificar el comportamiento de la sesión:

/tool list: Muestra todas las herramientas disponibles en el sistema.

/tool activate <nombre>: Activa una herramienta para el agente actual (la añade a las herramientas activas). Internamente, esto reconstruye el agente con la nueva lista de herramientas.

/tool deactivate <nombre>: Desactiva una herramienta (la quita de las activas).

/model <id>: Cambia el modelo del agente en caliente (reconstruye el agente con el nuevo modelo).

/memory: (opcional) Muestra estadísticas de memoria o permite gestionar sesiones.

/help: Muestra ayuda.

/exit: Sale del programa.

Gestión de sesiones: La CLI puede mantener un identificador de sesión para asociar la conversación con la memoria de chat. Podría ofrecer comandos para listar sesiones pasadas y retomarlas.

7. Procesos Externos (Scripts de Mantenimiento)
Para tareas de administración, el sistema incluye scripts independientes:

Indexador de documentos: Recorre la carpeta datos/documentos/, procesa los documentos (PDF, texto, etc.), los divide, genera embeddings, y los almacena en el vectorstore correspondiente. Durante este proceso, extrae metadatos (fecha de modificación, nombre de archivo, etc.) y permite al administrador añadir metadatos personalizados mediante un archivo de configuración o convenciones de nombres.

Generador de títulos de sesión: Un script que puede ejecutarse periódicamente o bajo demanda para analizar sesiones de chat sin título y generar uno usando un LLM.

Backup y limpieza: Scripts para respaldar bases de datos y vectorstores.

Flujo de Trabajo Típico
Para el Administrador
Instala el sistema en un servidor local usando el script install.sh.

Coloca documentos en datos/documentos/ (organizados en carpetas si se desea).

Ejecuta el script de indexación para poblar el vectorstore.

Edita config/models.yaml para añadir los modelos locales (Ollama) o remotos (DeepSeek) que desee.

Edita config/agentes.yaml para definir los agentes:

Asigna un modelo.

Lista las herramientas disponibles (las que están en herramientas/).

Decide qué herramientas estarán activas por defecto.

Configura la memoria (documentos y chat) según necesidades.

Escribe el prompt de sistema.

Inicia la CLI con el agente deseado para probar.

Para el Usuario Final
Ejecuta la CLI: python cli/main.py --agente investigador.

Conversa normalmente. Si necesita una habilidad específica, puede activarla con /tool activate busqueda_web.

Si el agente se alarga, pulsa Ctrl+C para detenerlo.

Al finalizar, escribe /exit. La conversación se guarda automáticamente en la memoria de chat.

¿Qué Hace que este Sistema sea "Wow"?
Declaratividad Total: Los agentes se definen en YAML. No hace falta programar para crear un nuevo agente o cambiar su comportamiento. Esto es clave para un producto instalable en empresas, donde los administradores no son necesariamente programadores.

Modularidad y Extensibilidad: Añadir una nueva habilidad (skill) es tan simple como crear un archivo Python en la carpeta herramientas/ con la clase adecuada. El sistema la descubre automáticamente. Esto permite a los integradores (como tú) desarrollar soluciones a medida rápidamente y cobrar por ello.

Memoria Dual con Ontologías: No es un simple RAG. La memoria de documentos permite filtrado por metadatos ontológicos, lo que posibilita respuestas más precisas en dominios complejos (ej: "buscar en contratos de 2023 que mencionen penalizaciones"). La memoria de chat es estructurada y permite búsqueda semántica sobre conversaciones pasadas, dando continuidad a largo plazo.

Activación/Desactivación de Herramientas en Tiempo Real: El usuario puede, mientras conversa, activar o desactivar habilidades del agente. Esto da un control sin precedentes sobre el comportamiento del asistente, adaptándose a la tarea del momento.

Cancelación de Respuesta con Ctrl+C: Una característica de usabilidad crítica: si el agente se desvía o genera demasiado texto, el usuario puede detenerlo instantáneamente sin cerrar el programa. Esto es posible gracias a una implementación cuidadosa del streaming con manejo de señales.

Arquitectura On-Premise: Todos los datos (documentos, historiales, índices) permanecen en los servidores de la empresa. No hay dependencia de la nube, lo que cumple con requisitos de privacidad y seguridad.

Jerarquía de Agentes: La capacidad de que un agente use a otro como herramienta permite construir sistemas complejos de forma natural. Por ejemplo, un agente de atención al cliente podría tener un subagente de cálculos, otro de búsqueda en base de datos, etc. Esto escala la inteligencia.

Preparado para el Negocio: El modelo de negocio es claro: instalación, configuración, enseñanza y desarrollo de herramientas personalizadas. Cada cliente puede tener una configuración única, y tú puedes cobrar por cada fase.

Resumen de Conceptos Clave
Agente: Entidad que combina un LLM, un conjunto de herramientas y memoria. Se define declarativamente.

Herramienta (Skill): Función externa que el agente puede invocar. Es modular y auto-contenida.

Subagente: Agente que se empaqueta como herramienta, permitiendo composición.

Fábrica de Agentes: Componente central que construye agentes a partir de configuraciones y registros.

Memoria de Documentos: RAG con vectorstore y metadatos ontológicos.

Memoria de Chat: Almacenamiento SQL de conversaciones, con opción de indexación semántica.

CLI Interactiva: Interfaz de usuario con comandos dinámicos y streaming cancelable.

Configuración YAML: Define modelos, agentes y sus parámetros sin código.

Este sistema, tal como está concebido, es una plataforma robusta y flexible para desplegar IA conversacional en entornos corporativos, con un enfoque práctico y comercial. La combinación de modularidad, control en tiempo real y memoria avanzada lo diferencian de soluciones más simples.

