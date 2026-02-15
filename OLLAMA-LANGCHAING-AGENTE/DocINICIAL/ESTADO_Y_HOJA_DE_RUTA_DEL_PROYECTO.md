# Estado y Hoja de Ruta del Proyecto: Agente Modular

**Versión: 2026-02-14**

Este documento sirve como la fuente única de verdad para el estado, la arquitectura y la evolución del proyecto de agente modular. Su propósito es consolidar toda la información para mantener el rumbo y asegurar que no se pierda funcionalidad valiosa.

---

## **Parte 1: El Estado Actual (Lo que TENEMOS y funciona)**

Esta sección audita las capacidades "wow" confirmadas en nuestra arquitectura base actual (`agente.py` + `permanencia/`).

### **Capacidades del Núcleo y Arquitectura:**
1.  **Arquitectura de Agente Instanciable (POO):** El sistema se basa en la clase `AgenteInteligente`, permitiendo la creación de múltiples agentes distintos a partir de un mismo plano.
2.  **Configuración Declarativa de Agentes (`agentes.yaml`):** Cada agente se define en un archivo YAML, especificando su `id`, nombre, modelo base, y configuración de memoria.
3.  **Soporte Multi-Proveedor (`models.yaml`):** Compatible con Ollama (local) y DeepSeek (API), y fácilmente extensible a otros proveedores.
4.  **Sistema de Alias para Modelos:** Se pueden usar nombres cortos (ej: `gema`) para referirse a modelos largos (ej: `gemma-ollama`).
5.  **Módulo de Persistencia con SQLAlchemy:** La memoria del chat se almacena de forma robusta en una base de datos SQLite, con un esquema granular y desacoplado del agente (`permanencia/SqlAlchemySQLite.py`).
6.  **Persistencia Enriquecida:** La base de datos incluye un campo `metadata_json` listo para almacenar datos estructurados (nodos, relaciones) para futuros sistemas semánticos (Cognee).
7.  **Componentes Desacoplados:** La lógica está separada en "Nodos" (Agente, Permanencia, Utilidades), facilitando la refactorización y la modularidad.
8.  **Gestión de Entorno con `uv`:** Uso de `uv` para una gestión de dependencias y entornos virtuales eficiente.
9.  **Soporte para Variables de Entorno (`.env`):** Manejo seguro de claves de API.

### **Capacidades de Interacción y CLI:**
10. **Modo CLI Interactivo Profesional:** Interfaz de chat con historial persistente y manejo de comandos.
11. **Modo CLI Headless (`-sc`):** Ejecución de una sola instrucción para casos de uso automatizados, con soporte para `stream` y `system_prompt`.
12. **Streaming Real y Cancelable:** Implementación robusta que permite un streaming de texto fluido y una cancelación inmediata con `Ctrl+C` sin matar el programa.
13. **Cambio de Modelo en Caliente (`/model`):** Capacidad de cambiar el "cerebro" (LLM) del agente durante una sesión de chat interactiva.
14. **Control de Streaming en Caliente (`/stream`):** Activar o desactivar el modo streaming durante una sesión.
15. **Jerarquía de System Prompts:** El prompt de sistema se puede definir en `agentes.yaml` y ser sobreescrito desde la CLI (`-ps`, `--prompt-sistema`) para máxima flexibilidad.
16. **Gestión de Sesiones (Base):** Se ha implementado la lógica inicial para nombrar una sesión de conversación al inicio, sentando las bases para una gestión más avanzada.

---

## **Parte 2: Próximos Pasos (Lo que VIENE)**

Esta sección detalla las siguientes funcionalidades a implementar, en orden de prioridad.

### **Paso Inmediato y Detallado: Título de Sesión Inteligente**
*   **Objetivo:** Implementar la lógica completa que, si el usuario no define un título al inicio, el sistema lo sugiera de forma inteligente.
*   **Detalles de Implementación:**
    1.  Modificar la clase `AgenteInteligente` para manejar un estado de sesión (ej: `AWAITING_TITLE`, `PROBATIONARY`, `ACTIVE`).
    2.  En el modo `PROBATIONARY`, contar las interacciones (5 de usuario + 5 de asistente).
    3.  Tras la 5ª interacción, pausar el chat principal.
    4.  Crear una función `sugerir_titulo(historial)` que:
        *   Tome los últimos 5 mensajes del usuario.
        *   Instancie un LLM rápido (ej: `gemma-ollama`) con un prompt específico para generar 3 títulos cortos y descriptivos.
        *   Presente al usuario las 3 opciones + la opción de escribir un título personalizado.
    5.  Una vez el usuario elija o escriba un título, actualizar el `self.titulo_actual` y cambiar el estado a `ACTIVE`.
    6.  Continuar la conversación de forma transparente.

**Detalles de Implementación - Sub-tareas Atómicas:**
1.  **Añadir Gestión de Estados y Conteo de Interacciones:**
    *   Modificar la clase `AgenteInteligente` para incluir atributos como `self.interaccion_count` (inicializado a 0) y `self.session_state` (inicializado a "INITIAL").
    *   Ajustar `gestionar_titulo_sesion` para iniciar el estado `PROBATIONARY` si no se proporciona un título explícito.
    *   Incrementar `self.interaccion_count` en `procesar_mensaje` durante el estado `PROBATIONARY` después de cada turno (usuario + asistente).
2.  **Implementar LLM para Sugerencia de Títulos:**
    *   Crear un LLM secundario (ej. `gema-ollama`) dentro del agente (o reutilizar el existente si es adecuado) para generar sugerencias de títulos a partir del historial.
    *   Crear un nuevo método `_sugerir_titulo_con_llm(historial_mensajes)` que use este LLM.
    *   Este método debe tomar los últimos N mensajes de la conversación y generar 3 títulos cortos y descriptivos.
3.  **Integrar Lógica de Sugerencia en `procesar_mensaje`:**
    *   Si `self.session_state == "PROBATIONARY"` y `self.interaccion_count >= X` (ej. 5 interacciones):
        *   Pausar la conversación (dejar de procesar entrada de usuario normal).
        *   Llamar a `_sugerir_titulo_con_llm`.
        *   Presentar las opciones al usuario y entrar en el estado `AWAITING_TITLE_SELECTION`.
4.  **Manejar Selección de Título por el Usuario:**
    *   Añadir lógica en `iniciar_modo_interactivo` (o un nuevo método de manejo de comandos) para capturar la elección del usuario (una de las sugerencias, o un título personalizado).
    *   Actualizar `self.titulo_actual` con el título elegido.
    *   Cambiar `self.session_state = "ACTIVE"`.
5.  **Migrar Títulos en la Base de Datos:**
    *   Implementar una función en `GestorDePersistencia` (o un nuevo método en `AgenteInteligente`) que, una vez seleccionado el título definitivo, actualice los registros de la base de datos de la sesión temporal (`sesion_temporal_...`) al nuevo `titulo_actual`.

### **Siguientes Pasos en la Hoja de Ruta:**
1.  **Integrar Editor `micro` para System Prompts:**
    *   **Objetivo:** Implementar el comando `/prompt-sistema` en modo interactivo.
    *   **Lógica:** Al ejecutarlo, se deberá abrir el editor `micro` con el `system_prompt` actual. Al cerrar el editor, el agente leerá el contenido del archivo temporal y actualizará su `system_prompt` en memoria para el resto de la sesión.

2.  **Desarrollo del Primer Sistema de Herramientas (Tools):**
    *   **Objetivo:** Dotar al agente de la capacidad de ejecutar acciones más allá de generar texto.
    *   **Fase 1: Herramienta Simple:** Crear una carpeta `agents/herramientas/sistema/` y dentro un archivo `comandos_shell.py` con una herramienta simple que use `subprocess` para ejecutar comandos básicos del sistema (ej: `ls -l`, `date`).
    *   **Fase 2: Conexión con el Agente:** Modificar `agente.py` para que pueda "vincular" (`bind_tools`) las herramientas a su LLM y manejar las respuestas del modelo que sean `ToolCall` en lugar de texto.

---

## **Parte 3: Visión a Largo Plazo (El Futuro del Proyecto)**

Esta es una categorización de la lista de deseos más amplia para mantener el enfoque.

### **Memoria y Conocimiento:**
*   **Memoria Dual:** Implementar una memoria de documentos (Vectorstore) separada de la memoria de chat (SQL).
*   **Indexación Automática:** Crear un proceso para vigilar un directorio de documentos y convertirlos en vectores automáticamente.
*   **Metadatos Ontológicos:** Usar el campo `metadata_json` para que un LLM extraiga entidades y relaciones de las conversaciones y las guarde, creando un grafo de conocimiento.
*   **Búsqueda Semántica en Historial:** Permitir buscar conversaciones pasadas por el significado de lo que se habló, no solo por palabras clave.

### **Agentes y Herramientas:**
*   **Herramientas Auto-Registrables:** Mecanismo para que el agente descubra y cargue herramientas automáticamente solo con ponerlas en una carpeta.
*   **Lazy Loading:** Cargar herramientas solo cuando se necesiten para optimizar el uso de memoria.
*   **Subagentes como Herramientas:** Empaquetar un agente completo como una herramienta que otro agente pueda invocar para tareas complejas.

### **Interfaz y Experiencia de Usuario (CLI):**
*   **Gestión Avanzada de Sesiones:** Comandos para listar, borrar y cambiar entre sesiones de chat (`/session list`, `/session switch [titulo]`).
*   **Panel de Administración (Futuro Lejano):** Una interfaz web o TUI (Text-based User Interface) para gestionar agentes, ver logs y monitorizar el rendimiento.

### **Robustez y Producción:**
*   **Sistema de Pruebas Automatizadas:** Crear tests (unitarios y de integración) para validar que los cambios no rompen funcionalidades existentes.
*   **Sistema de Backup y Restauración:** Scripts para hacer copias de seguridad de la base de datos de memoria y el vectorstore.
*   **Auditoría y Logs Detallados:** Mejorar el sistema de logging para un seguimiento más granular.
