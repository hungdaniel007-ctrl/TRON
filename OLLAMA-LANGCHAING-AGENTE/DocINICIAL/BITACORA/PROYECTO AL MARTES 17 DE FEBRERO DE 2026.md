Aquí tienes la información solicitada, estructurada en las cuatro partes requeridas, extraída del contexto actual del proyecto **OLLAMA-LANGCHAING-AGENTE**.

---

### **PARTE 1: Ubicación de Archivos Estratégicos y Documentación**

Esta sección contiene los manuales, guías, bitácoras y referencias externas necesarias para entender, operar y mantener el sistema.

**Ruta Base:** `/home/daniel/tron/programas/TRON/OLLAMA-LANGCHAING-AGENTE/`

#### **📂 Documentación del Proyecto (`DocINICIAL/`)**
*   **`DocINICIAL/ESTADO_Y_HOJA_DE_RUTA_DEL_PROYECTO.md`**
    *   **Descripción:** El documento maestro de gestión. Contiene el estado actual, lo que se ha logrado y el desglose detallado de las tareas futuras (como el "Título de Sesión Inteligente"). Es el mapa de navegación del desarrollo.
*   **`DocINICIAL/comandos_de_prueba.md`**
    *   **Descripción:** "Cheat sheet" o guía rápida operativa. Contiene todos los comandos CLI validados para ejecutar el sistema en modo interactivo y *headless* (sin cabeza), incluyendo ejemplos con streaming y cambio de agentes.
*   **`DocINICIAL/BITACORA/logros_y_errores.md`**
    *   **Descripción:** Memoria técnica de resolución de problemas. Documenta errores críticos encontrados (ej. problemas de indentación, conflictos de configuración en `load_llm`, errores 404 de Ollama) y las soluciones exactas aplicadas. Vital para no repetir errores pasados.
*   **`LEEME.md`**
    *   **Descripción:** Archivo de entrada general (Readme). Explica la visión macro del proyecto, requisitos previos e instalación básica.

#### **📂 Documentación de Referencia y Conceptos**
*   **`Sistema de Agentes Modulares con Memoria Dual y Configuración Declarativa.md`**
    *   **Descripción:** Documento fundacional que explica la teoría detrás de la arquitectura: por qué memoria dual, por qué configuración declarativa.
*   **`Arquitectura Industrial Fábrica de Agentes con Componentes Modulares.md`**
    *   **Descripción:** Explica el patrón de diseño de "Fábrica" utilizado para instanciar agentes dinámicamente.
*   **`IDEAS y apuntes para hacer un asistente local con langchaing.md`**
    *   **Descripción:** Lluvia de ideas y conceptos previos sobre la integración con LangChain.
*   **`Investigacion sobre SQL alchemy.md`**
    *   **Descripción:** Base teórica para el módulo de persistencia.
*   **`Ollama-API.md`**
    *   **Descripción:** Referencia técnica de la API de Ollama, útil para entender cómo `agente.py` se comunica nativamente con los modelos locales (bypass de LangChain para streaming robusto).

---

### **PARTE 2: Ubicación de Códigos, Configuración y Estructura del Sistema**

Detalle técnico de la infraestructura del código fuente, dónde vive cada componente y qué hace.

**Ruta Base:** `/home/daniel/tron/programas/TRON/OLLAMA-LANGCHAING-AGENTE/`

#### **🚀 Ejecución y Entrada**
*   **`run.py`**
    *   **Función:** Script agnóstico de ejecución. Detecta el sistema operativo, activa el entorno virtual (`.venv`) automáticamente y lanza el agente. Es el punto de entrada recomendado para el usuario.

#### **⚙️ Configuración (`config/`)**
*   **`config/models.yaml`**
    *   **Función:** **Biblioteca de Cerebros**. Define los modelos disponibles (DeepSeek API, Gemma Ollama), sus proveedores y parámetros técnicos base.
*   **`config/agentes.yaml`**
    *   **Función:** **Fábrica de Personalidades**. Define a los agentes (`tron-ceo`, `gema-analyst`), qué cerebro usan, su `system_prompt`, y la configuración de su memoria (tipo de DB y ruta).

#### **🧠 Núcleo del Agente (`agents/`)**
*   **`agents/agente.py`**
    *   **Función:** **El Orquestador**. Contiene la clase `AgenteInteligente`. Gestiona el ciclo de vida, la interacción con el usuario (CLI), el streaming robusto (con manejo de hilos y `requests` para Ollama), y coordina la memoria y el LLM.
*   **`agents/utils.py`**
    *   **Función:** **Utilidades y Sanitización**. Contiene `load_llm`. Su función crítica es fusionar y limpiar las configuraciones de `models.yaml` y `agentes.yaml` para evitar errores de parámetros no soportados por LangChain (el fix de `top_k`, `temperatura`, etc.).

#### **💾 Persistencia y Datos (`permanencia/` y `datos/`)**
*   **`permanencia/persistence_manager.py`**
    *   **Función:** **Gestor de Base de Datos**. (Anteriormente `SqlAlchemySQLite.py`). Es agnóstico a la DB. Maneja la conexión (SQLAlchemy), el esquema de la tabla `HistorialChat` y las operaciones CRUD (guardar/leer). Define los "Puertos" de entrada/salida de datos.
*   **`permanencia/db_viewer.py`**
    *   **Función:** **Visor CLI**. Herramienta para inspeccionar visualmente las conversaciones guardadas en los archivos `.db`.
*   **`permanencia/update_user_id.py`**
    *   **Función:** Script de utilidad para migraciones o correcciones masivas de datos (ej. cambiar IDs de usuario).
*   **`datos/`**
    *   **Contenido:** Carpeta donde se almacenan físicamente los archivos SQLite (`tron_memory.db`, `gema_analyst_memory.db`).

#### **🧪 Pruebas (`TESTs/`)**
*   **`TESTs/run_all_tests.py`**
    *   **Función:** Suite de pruebas automatizada. Ejecuta escenarios *headless* para validar que los agentes cargan, responden y guardan datos correctamente.
*   **`TESTs/logs/`**
    *   **Contenido:** Registros detallados de la ejecución de cada prueba para depuración.

---

### **PARTE 3: Estado Actual y Próximos Pasos (Técnico-Programático)**

**¿Dónde estamos?**
El sistema ha alcanzado una **Arquitectura v1.0 Estable**.
1.  **Modularidad:** Separación clara entre Agente, Cerebro (LLM) y Memoria.
2.  **Robustez:** Streaming funcional en Ollama y DeepSeek con cancelación (`Ctrl+C`).
3.  **Agnosticismo:** El módulo de persistencia ya no está atado solo a SQLite por nombre, y la configuración permite inyección de parámetros.
4.  **Validación:** Suite de pruebas pasando (6/6) y visor de DB funcional.

**¿Qué se va a hacer? (El Siguiente Hito)**
Implementar la **"Lógica de Título de Sesión Inteligente"**.

**¿Dónde?**
Principalmente en `agents/agente.py`, con soporte menor en `permanencia/persistence_manager.py`.

**¿Como? (Plan Técnico)**
1.  **Gestión de Estados (En `AgenteInteligente`):**
    *   Introducir variables de estado: `self.session_state` (valores: `INITIAL`, `PROBATIONARY`, `ACTIVE`) y `self.interaccion_count`.
2.  **Lógica de "Probation":**
    *   Si el usuario no da título al inicio, entrar en `PROBATIONARY`.
    *   Contar 5 interacciones (turnos usuario-agente).
3.  **Generación de Título (El "Sub-agente"):**
    *   Crear método `_sugerir_titulo_con_llm`. Usará el mismo LLM cargado (o uno ligero) para leer el historial reciente y proponer 3 títulos cortos.
4.  **Interacción de Usuario:**
    *   Pausar el chat normal. Presentar las opciones. Permitir selección o escritura manual.
5.  **Migración (En `persistence_manager.py`):**
    *   Crear método `renombrar_sesion(old_title, new_title, user_id)`.
    *   Actualizar todos los registros en la DB que tengan el título temporal al nuevo título definitivo.

---

### **PARTE 4: Filosofía, Directivas y Memoria del Proyecto**

Esta sección define el "alma" del desarrollo y las reglas inquebrantables para mantener la calidad.

#### **🧠 Filosofía: "Cápsulas Inviolables"**
*   **Principio:** Lo que ya funciona, se aísla y **no se toca**.
*   **Objetivo:** Evitar regresiones. Si algo funciona (ej. el streaming actual), se considera una "cápsula cerrada". Las nuevas funcionalidades se construyen *alrededor* o *sobre* ella, no modificando su interior a menos que sea estrictamente necesario por un bug crítico.
*   **Nucleación:** Avanzamos hacia un núcleo estable (el agente) que orquesta acciones periféricas (herramientas, MCPs). El código del agente debe volverse cada vez más simple y delegar más.

#### **⚠️ Cuidados y Directivas (Para la IA Desarrolladora)**
1.  **Prohibición de Edición Manual:** Yo (la IA) **nunca** debo editar archivos manualmente. Debo usar herramientas (`qwen`, `edit`, `write_file`).
2.  **Uso de `qwen`:**
    *   Usar siempre `--yolo` para ejecución autónoma.
    *   **CERO Markdown en prompts de bash:** Los prompts para `qwen` deben ser cadenas planas, sin acentos, sin comillas conflictivas y sin bloques de código complejos que rompan el shell.
    *   Instrucciones atómicas y precisas.
3.  **Documentación de Errores:** Cada vez que se corrige un bug complejo, se debe añadir un comentario acumulativo al inicio del archivo afectado (como hicimos en `utils.py` y `agente.py`) explicando el error y la solución. Esto es "memoria en el código".

#### **🛡️ Prácticas de Arquitectura**
*   **Puertos:** Definir claramente las entradas y salidas de los módulos (ej. los métodos de `GestorDePersistencia` están marcados como `[PUERTO]`).
*   **Sanitización:** Nunca confiar en la configuración cruda. Siempre limpiar y validar los diccionarios de configuración antes de pasarlos a librerías externas (como aprendimos con `load_llm`).
*   **Experiencia de Usuario (CLI):** El modo *headless* debe ser puro (solo salida del modelo). El modo interactivo debe ser informativo pero limpio. La persistencia en *headless* debe ser explícita (`--session`).

#### **📝 Recordatorios de Memoria**
*   **Ollama vs DeepSeek:** Recordar que Ollama requiere manejo de socket especial (requests/threading) para cancelación, mientras que DeepSeek (API) funciona bien con el estándar de LangChain, pero requiere manejo cuidadoso de parámetros (`top_k`).
*   **Configuración:** `agentes.yaml` manda sobre `models.yaml`. La identidad es del Agente, el cerebro es del Modelo.



Entendido. Inicio el ciclo de análisis y respuesta detallada.

Esta es la **PARTE 1**, dedicada exclusivamente al **Análisis Profundo de Archivos Estratégicos y Documentación**.

---

### **PARTE 1: MAPA ESTRATÉGICO DE DOCUMENTACIÓN Y REFERENCIAS**

Este análisis desglosa la infraestructura documental del proyecto. No se trata solo de una lista de archivos, sino de la clasificación funcional de los activos de conocimiento que permiten la operación, el mantenimiento y la evolución del sistema **OLLAMA-LANGCHAING-AGENTE**.

#### **1. NÚCLEO DE GESTIÓN Y ESTRATEGIA (El "Cerebro" del Proyecto)**

Estos archivos definen el *qué*, el *cuándo* y el *por qué* del desarrollo. Son los documentos vivos que gobiernan el ciclo de vida del software.

*   **`DocINICIAL/ESTADO_Y_HOJA_DE_RUTA_DEL_PROYECTO.md`**
    *   **Clasificación:** Gestión de Proyecto / Roadmap Técnico.
    *   **Ubicación:** `/home/daniel/tron/programas/TRON/OLLAMA-LANGCHAING-AGENTE/DocINICIAL/`
    *   **Análisis Profundo:** Es el documento más crítico para la continuidad. No es estático; evoluciona con cada iteración.
        *   **Contenido Estratégico:** Define el estado actual exacto (v1.0 Estable) y desglosa granularmente las tareas futuras (como la lógica de estados `PROBATIONARY` para el título de sesión).
        *   **Uso:** Debe consultarse antes de escribir una sola línea de código nuevo para entender el contexto y las dependencias. Es la "ley" actual del desarrollo.

*   **`DocINICIAL/BITACORA/logros_y_errores.md`**
    *   **Clasificación:** Memoria Técnica / Base de Conocimiento de Errores (Knowledge Base).
    *   **Ubicación:** `/home/daniel/tron/programas/TRON/OLLAMA-LANGCHAING-AGENTE/DocINICIAL/BITACORA/`
    *   **Análisis Profundo:** Este archivo es el mecanismo de defensa contra la regresión.
        *   **Valor Táctico:** Contiene diagnósticos forenses de errores complejos (ej. el conflicto de parámetros en `load_llm` o el manejo de sockets en Ollama).
        *   **Directiva:** Antes de corregir un bug, se consulta este archivo para ver si ya fue resuelto o si la solución propuesta entra en conflicto con una solución previa. Transforma la experiencia dolorosa de depuración en activos de conocimiento reutilizables.

#### **2. MANUALES OPERATIVOS Y DE EJECUCIÓN (La "Interfaz" Humana)**

Documentos diseñados para el operador del sistema (tú) y para la validación rápida de funcionalidades.

*   **`DocINICIAL/comandos_de_prueba.md`**
    *   **Clasificación:** Guía de Operaciones / Cheat Sheet de QA.
    *   **Ubicación:** `/home/daniel/tron/programas/TRON/OLLAMA-LANGCHAING-AGENTE/DocINICIAL/`
    *   **Análisis Profundo:** Es la traducción práctica del código a la acción.
        *   **Contenido:** Bloques de código listos para copiar y pegar que cubren todos los casos de uso soportados: modo interactivo, *headless*, streaming, cambio de agentes y persistencia.
        *   **Función:** Reduce la fricción cognitiva al probar. En lugar de recordar flags complejos (`--headless -m "..." --session ...`), el operador recurre a este catálogo validado.

*   **`LEEME.md`**
    *   **Clasificación:** Onboarding / Visión General.
    *   **Ubicación:** Raíz del proyecto.
    *   **Análisis Profundo:** Establece el contexto macro. Define los prerrequisitos (Ollama, Python, venv) y la instalación inicial. Es el punto de entrada para cualquier nueva instancia del proyecto.

#### **3. FUNDAMENTOS TEÓRICOS Y ARQUITECTURA (LangChain y Diseño)**

Estos documentos explican la teoría detrás del código. Son vitales para entender *por qué* el sistema está diseñado como está (Fábricas, Memoria Dual, Agnosticismo).

*   **`Sistema de Agentes Modulares con Memoria Dual y Configuración Declarativa.md`**
    *   **Clasificación:** Arquitectura de Software / Teoría de Agentes.
    *   **Ubicación:** Raíz del proyecto.
    *   **Análisis Profundo:** Justifica la separación entre la memoria de corto plazo (contexto de ventana del LLM) y la memoria de largo plazo (Persistencia SQL/Vectorial). Define el modelo mental de configuración declarativa (`yaml`) que desacopla la lógica del código de los datos de configuración.

*   **`Arquitectura Industrial Fábrica de Agentes con Componentes Modulares.md`**
    *   **Clasificación:** Patrones de Diseño.
    *   **Ubicación:** `/home/daniel/tron/programas/TRON/OLLAMA-LANGCHAING-AGENTE/DocINICIAL/`
    *   **Análisis Profundo:** Detalla el patrón "Factory" utilizado en `agente.py` para instanciar dinámicamente agentes (`Tron`, `Gemma`) basándose en planos (`agentes.yaml`). Explica cómo se ensamblan las piezas (Cerebro + Memoria + Herramientas) en tiempo de ejecución.

*   **`IDEAS y apuntes para hacer un asistente local con langchaing.md`**
    *   **Clasificación:** Investigación / Brainstorming.
    *   **Ubicación:** `/home/daniel/tron/programas/TRON/OLLAMA-LANGCHAING-AGENTE/DocINICIAL/`
    *   **Análisis Profundo:** Contiene la génesis del proyecto. Útil para revisar ideas descartadas o futuras funcionalidades potenciales que aún no están en la hoja de ruta oficial.

#### **4. REFERENCIAS TÉCNICAS ESPECÍFICAS (Componentes Críticos)**

Documentación técnica de bajo nivel sobre tecnologías clave integradas.

*   **`Investigacion sobre SQL alchemy.md`**
    *   **Clasificación:** Referencia de Persistencia / ORM.
    *   **Ubicación:** `/home/daniel/tron/programas/TRON/OLLAMA-LANGCHAING-AGENTE/DocINICIAL/`
    *   **Análisis Profundo:** Base teórica para `persistence_manager.py`. Explica el mapeo Objeto-Relacional necesario para que el sistema sea agnóstico a la base de datos (SQLite hoy, PostgreSQL mañana).

*   **`Ollama-API.md`**
    *   **Clasificación:** Referencia de API Externa.
    *   **Ubicación:** `/home/daniel/tron/programas/TRON/OLLAMA-LANGCHAING-AGENTE/DocINICIAL/`
    *   **Análisis Profundo:** Documentación crítica para entender el "bypass" de LangChain.
        *   **Relevancia:** Dado que LangChain tiene limitaciones con el streaming de Ollama (bloqueos), este documento detalla los endpoints nativos (`/api/chat`) que utilizamos en `_stream_ollama_with_cancel` para lograr un control total del socket y permitir la interrupción (`Ctrl+C`).

---

**Fin de la PARTE 1.**
Espero tus instrucciones para proceder con la **PARTE 2** (Ubicación de códigos y documentos de configuración detallados).

Esta es la **PARTE 2**, dedicada al **Análisis Técnico de la Infraestructura de Código y Configuración**.

Aquí desglosamos la anatomía del sistema, explicando no solo dónde están los archivos, sino su función arquitectónica, sus dependencias y por qué están diseñados de esta manera.

---

### **PARTE 2: INFRAESTRUCTURA DE CÓDIGO Y CONFIGURACIÓN**

**Ruta Raíz del Proyecto:** `/home/daniel/tron/programas/TRON/OLLAMA-LANGCHAING-AGENTE/`

#### **1. CAPA DE EJECUCIÓN Y ENTORNO (El Puente con el SO)**

Estos archivos son los encargados de preparar el terreno para que el código Python se ejecute correctamente, independientemente de desde dónde se llame.

*   **`run.py`**
    *   **Ubicación:** Raíz.
    *   **Rol:** **Lanzador Agnóstico / Bootstrap**.
    *   **Análisis Técnico:** Este script no contiene lógica de IA. Su única función es la **introspección del entorno**.
        *   Detecta el sistema operativo (Linux/Windows).
        *   Calcula la ruta absoluta del proyecto.
        *   Localiza el intérprete de Python dentro del entorno virtual (`.venv`).
        *   Reemplaza el proceso actual (`os.execv`) con el proceso del agente, pasando todos los argumentos CLI transparentemente.
    *   **Por qué es vital:** Permite ejecutar `./run.py` desde cualquier carpeta del sistema sin tener que activar manualmente el entorno virtual (`source .venv/bin/activate`).

*   **`.env`** (y `.env.example`)
    *   **Ubicación:** Raíz.
    *   **Rol:** **Gestión de Secretos**.
    *   **Análisis Técnico:** Almacena variables sensibles como `DEEPSEEK_API_KEY`. `agente.py` carga esto al inicio usando `python-dotenv`. Nunca se sube al control de versiones (git).

#### **2. CAPA DE CONFIGURACIÓN DECLARATIVA (El ADN del Sistema)**

Aquí se define el comportamiento y las capacidades del sistema sin tocar código. Sigue el patrón de "Inyección de Dependencias" basada en configuración.

*   **`config/models.yaml`**
    *   **Ubicación:** `config/`
    *   **Rol:** **Biblioteca de Hardware/Cerebros**.
    *   **Análisis Técnico:** Define los proveedores técnicos.
        *   Mapea un ID interno (`gemma-ollama-local`) a una configuración técnica específica (`provider: ollama`, `model: gemma3:4b`, `base_url`).
        *   Es la capa de abstracción que permite cambiar de `gemma:7b` a `gemma3:4b` tocando solo una línea aquí, sin editar el código Python.

*   **`config/agentes.yaml`**
    *   **Ubicación:** `config/`
    *   **Rol:** **Fábrica de Personalidades**.
    *   **Análisis Técnico:** Define las instancias lógicas de los agentes.
        *   **Herencia:** Un agente (`tron-ceo`) selecciona un cerebro base de `models.yaml`.
        *   **Sobreescritura:** Puede redefinir parámetros (ej. `temperatura`) específicos para esa personalidad.
        *   **Memoria:** Define qué tipo de persistencia usar (`sqlite`) y dónde guardar el archivo (`datos/tron_memory.db`).
        *   **Identidad:** Contiene el `system_prompt` que define quién es el agente.

#### **3. CAPA DE LÓGICA CORE (El Orquestador)**

El cerebro programático del sistema. Aquí reside la lógica de negocio, el manejo de flujo y la integración de componentes.

*   **`agents/agente.py`**
    *   **Ubicación:** `agents/`
    *   **Rol:** **Orquestador Principal / Controlador**.
    *   **Análisis Técnico:** Es el archivo más complejo y central.
        *   **Clase `AgenteInteligente`:** Encapsula el estado de una sesión (memoria, modelo actual, configuración).
        *   **Gestión de Streaming Híbrida:** Implementa lógica condicional para usar el streaming estándar de LangChain (para DeepSeek) o un **bypass nativo con `requests` y `threading`** para Ollama (para solucionar el bloqueo de sockets y permitir `Ctrl+C`).
        *   **CLI Loop:** Maneja el bucle interactivo de entrada/salida y los comandos en tiempo de ejecución (`/model`, `/stream`).
        *   **Persistencia:** Decide cuándo y qué guardar en la base de datos a través del `GestorDePersistencia`.

*   **`agents/utils.py`**
    *   **Ubicación:** `agents/`
    *   **Rol:** **Sanitización y Carga de Modelos**.
    *   **Análisis Técnico:** Resuelve el problema de impedancia entre nuestra configuración y las librerías externas.
        *   **Función `load_llm`:** Es una fábrica que instancia objetos `ChatOllama` o `ChatDeepSeek`.
        *   **Sanitización Crítica:** Su tarea más importante es **limpiar y mapear** los diccionarios de configuración. Elimina claves internas (`modelo_base_id`) y renombra claves en español (`temperatura` -> `temperature`) antes de pasarlas a LangChain para evitar errores de `TypeError`.

#### **4. CAPA DE PERSISTENCIA Y DATOS (La Memoria)**

Módulos encargados de que la información sobreviva al reinicio del proceso. Diseñado para ser agnóstico al motor de base de datos.

*   **`permanencia/persistence_manager.py`**
    *   **Ubicación:** `permanencia/`
    *   **Rol:** **Gestor de Base de Datos (ORM)**.
    *   **Análisis Técnico:** Abstrae las operaciones SQL.
        *   Usa **SQLAlchemy** para definir el esquema (`HistorialChat`).
        *   Expone "Puertos" claros (`guardar_mensaje`, `obtener_historial_reciente`) que el agente consume.
        *   Está diseñado para recibir `db_type` y `db_config`, permitiendo cambiar de SQLite a PostgreSQL en el futuro sin tocar el código del agente.

*   **`permanencia/db_viewer.py`**
    *   **Ubicación:** `permanencia/`
    *   **Rol:** **Herramienta de Inspección**.
    *   **Análisis Técnico:** Un script CLI independiente que se conecta a los archivos `.db` (solo lectura) para listar sesiones y leer mensajes. Útil para depuración y auditoría humana.

*   **`datos/`** (Directorio)
    *   **Ubicación:** `datos/`
    *   **Rol:** **Almacenamiento Físico**.
    *   **Contenido:** Archivos `.db` de SQLite (ej. `tron_memory.db`). Separar los datos del código es una práctica fundamental para la limpieza y el backup.

#### **5. CAPA DE CALIDAD Y PRUEBAS (QA)**

Infraestructura para asegurar que los cambios no rompan la funcionalidad existente.

*   **`TESTs/run_all_tests.py`**
    *   **Ubicación:** `TESTs/`
    *   **Rol:** **Suite de Pruebas Automatizada**.
    *   **Análisis Técnico:** Script que orquesta ejecuciones del sistema en modo *headless*.
        *   Define casos de prueba (DeepSeek simple, Gemma streaming, persistencia, etc.).
        *   Ejecuta `run.py` como subproceso con `timeout` de seguridad.
        *   Valida la salida usando expresiones regulares (Regex) para confirmar que el modelo correcto se cargó y respondió.

*   **`TESTs/logs/`** (Directorio)
    *   **Ubicación:** `TESTs/`
    *   **Rol:** **Evidencia de Ejecución**.
    *   **Contenido:** Archivos `.log` con la salida estándar (`stdout`) y de error (`stderr`) de cada prueba. Fundamental para el análisis forense cuando una prueba falla.

---

**Fin de la PARTE 2.**
Espero tus instrucciones para proceder con la **PARTE 3** (Estado actual, qué se va a hacer, dónde y cómo - Técnico/Programático).

Esta es la **PARTE 3**, dedicada al **Estado Técnico Actual y la Hoja de Ruta Programática**.

Aquí definimos con precisión de ingeniero dónde estamos parados y el plan de ejecución detallado para la siguiente fase, desglosando el *qué*, el *dónde* y el *cómo*.

---

### **PARTE 3: ESTADO TÉCNICO Y EJECUCIÓN PROGRAMÁTICA**

#### **1. ESTADO ACTUAL DEL SISTEMA (Snapshot v1.0)**

El sistema ha alcanzado una madurez arquitectónica funcional. Ya no es un script monolítico, sino un sistema modular orquestado.

*   **Estabilidad del Core:** El archivo `agents/agente.py` actúa como un orquestador estable. Ya no contiene lógica dura de conexión a bases de datos (delegada a `persistence_manager.py`) ni lógica sucia de configuración (delegada a `utils.py`).
*   **Validación de Entradas:** La capa de `utils.py` sanitiza activamente los diccionarios de configuración, resolviendo el conflicto de impedancia entre nuestros YAMLs (español/interno) y las librerías externas (LangChain/Ollama).
*   **Manejo de Procesos:** El streaming de Ollama corre en hilos separados con control de sockets nativo (`requests`), permitiendo interrupciones limpias (`Ctrl+C`) sin corromper el estado del agente.
*   **Persistencia:** La base de datos es accesible, consultable (vía `db_viewer.py`) y el código está preparado para cambiar de motor (SQLite -> Postgres) mediante configuración.

**Conclusión del Estado:** Tenemos una base sólida ("Cápsula Inviolable"). Ahora podemos construir *funcionalidad de negocio* compleja sobre ella sin miedo a romper la comunicación básica.

---

#### **2. EL SIGUIENTE OBJETIVO: TÍTULO DE SESIÓN INTELIGENTE**

**El Problema:** Actualmente, la experiencia de usuario (UX) se interrumpe al inicio pidiendo un título manual, o usa un título temporal feo (`sesion_temporal_...`).
**La Solución:** Implementar un flujo de "Probation" (Prueba) donde el sistema espera a tener contexto suficiente para auto-proponer un título semántico.

---

#### **3. PLAN DE EJECUCIÓN TÉCNICA (El "Cómo" y "Dónde")**

La implementación se realizará en 4 fases lógicas, tocando archivos específicos mediante "cirugía de precisión".

##### **FASE A: Máquina de Estados (En `agents/agente.py`)**
*   **Objetivo:** Que el agente sepa en qué fase de la conversación está.
*   **Cambio Programático:**
    *   En `AgenteInteligente.__init__`, inicializar:
        ```python
        self.session_state = "INITIAL" # Valores: INITIAL, PROBATIONARY, ACTIVE
        self.interaction_count = 0
        self.umbral_titulo = 5 # Configurable
        ```
    *   Modificar `gestionar_titulo_sesion`: Si el usuario da Enter (vacío), establecer `self.session_state = "PROBATIONARY"` y devolver un ID temporal.

##### **FASE B: El Sub-Agente Generador (En `agents/agente.py`)**
*   **Objetivo:** Capacidad de resumir el historial en un título corto.
*   **Cambio Programático:**
    *   Crear método privado `_generar_sugerencias_titulo(self)`.
    *   **Lógica:**
        1.  Extraer los últimos N mensajes de la memoria.
        2.  Construir un prompt específico: *"Analiza esta conversación y genera 3 títulos cortos (máx 5 palabras) en formato JSON..."*.
        3.  Invocar `self.llm.invoke()` (sin streaming) para obtener las sugerencias.
        4.  Manejar errores (si el LLM falla, degradar a título por fecha).

##### **FASE C: Interceptor de Flujo (En `agents/agente.py` -> `procesar_mensaje`)**
*   **Objetivo:** Detectar cuándo disparar la sugerencia sin bloquear el mensaje actual.
*   **Cambio Programático:**
    *   Al final de `procesar_mensaje`, incrementar `self.interaction_count`.
    *   **Condición de Disparo:**
        ```python
        if self.session_state == "PROBATIONARY" and self.interaction_count >= self.umbral_titulo:
            self._activar_flujo_seleccion_titulo()
        ```

##### **FASE D: Migración de Datos (En `permanencia/persistence_manager.py`)**
*   **Objetivo:** Renombrar la sesión retroactivamente en la base de datos.
*   **Cambio Programático:**
    *   Crear nuevo método (Puerto): `renombrar_sesion(old_title, new_title, user_id)`.
    *   **SQL:** Ejecutar un `UPDATE historial_conversaciones SET titulo_conversacion = :new WHERE titulo_conversacion = :old AND usuario_id = :user`.
    *   Esto asegura que los 5 mensajes previos no se pierdan ni queden huérfanos bajo el ID temporal.

---

**Fin de la PARTE 3.**
Espero tus instrucciones para proceder con la **PARTE 4** (Filosofía, comportamiento, directivas y memoria).

Esta es la **PARTE 4**, la última y quizás la más importante. Aquí definimos el **"Alma" y la "Psicología" del Proyecto**.

Esta sección no trata sobre código, sino sobre **cómo pensamos y actuamos** para escribir ese código. Son las reglas de enfrentamiento, la memoria institucional y los hábitos de seguridad que garantizan que el sistema no colapse bajo su propio peso.

---

### **PARTE 4: FILOSOFÍA, DIRECTIVAS Y MEMORIA TÁCTICA**

#### **1. FILOSOFÍA CENTRAL: "CÁPSULAS INVIOLABLES"**

*   **El Principio:** El código que ha sido probado y validado (como el streaming actual o la carga de modelos) se convierte en una **Cápsula Inviolable**.
*   **La Regla:** No se "toquetea" el interior de una cápsula para añadir nuevas funcionalidades. Se construye **alrededor** de ella.
*   **Nucleación de Acciones:** El objetivo final es que el `agente.py` (el núcleo) sea cada vez más pequeño y estable, actuando solo como un despachador que delega la complejidad a herramientas periféricas (MCPs, módulos de persistencia, visores).
*   **Mentalidad:** "Si funciona, está sellado. Si necesito algo nuevo, creo un puerto nuevo, no rompo la pared."

#### **2. DIRECTIVAS OPERATIVAS (Para la IA Desarrolladora)**

Estas son las reglas de seguridad innegociables para evitar errores humanos/IA recurrentes.

*   **PROHIBICIÓN DE EDICIÓN MANUAL:** Yo (la IA) tengo prohibido intentar editar archivos "a mano" o asumir que puedo aplicar parches complejos en un solo paso. **Debo usar herramientas**.
*   **PROTOCOLO DE USO DE `QWEN`:**
    *   **Modo YOLO:** Siempre usar `--yolo` para ejecución autónoma.
    *   **CERO MARKDOWN EN BASH:** Los prompts enviados a `qwen` vía terminal deben ser **texto plano**.
        *   ❌ No usar backticks (\`\`\`).
        *   ❌ No usar comillas simples anidadas sin escapar.
        *   ✅ Usar estrategias de generación: "Crea un archivo con este contenido..." en lugar de intentar pasar el código como string en el prompt.
    *   **Atomicidad:** Si una tarea es compleja, divídela. No le pidas a `qwen` que refactorice todo el sistema en un solo prompt. Pídele que arregle una función, luego otra.

#### **3. PRÁCTICAS DE INGENIERÍA Y "HÁBITOS"**

*   **Sanitización Paranoica:** Nunca confiar en que un diccionario de configuración (`yaml`) tiene las claves correctas para una librería externa. Siempre filtrar, limpiar y mapear parámetros (como hicimos con `top_k` y `temperatura` en `utils.py`) antes de inyectarlos.
*   **Documentación Semántica (El "Por Qué"):**
    *   No comentar *qué* hace el código (eso se ve). Comentar *por qué* existe y *qué error previene*.
    *   Usar encabezados de **"HISTORIAL DE ERRORES Y SOLUCIONES"** al inicio de archivos críticos. Esto actúa como memoria a largo plazo para cualquier desarrollador futuro.
*   **Definición de Puertos:** Marcar explícitamente las funciones que sirven de interfaz con el mundo exterior (ej. `[PUERTO] guardar_mensaje`). Esto define la frontera de la "Cápsula".

#### **4. MEMORIA TÁCTICA Y RECORDATORIOS (Lecciones Aprendidas)**

Esta es la "bitácora de guerra" de los errores que no debemos repetir.

*   **El "Socket Hang" de Ollama:** LangChain nativo no maneja bien la interrupción (`Ctrl+C`) con Ollama. **Solución:** Siempre usar el bypass con `requests` y `threading` para Ollama.
*   **Identidad vs. Cerebro:** Un Agente (`Tron`) tiene una identidad fija. Su Modelo (`DeepSeek`) es intercambiable. Nunca confundir el nombre del agente con el nombre del modelo en los logs.
*   **Configuración Jerárquica:** `agentes.yaml` (específico) siempre sobreescribe a `models.yaml` (genérico).
*   **Experiencia CLI:**
    *   Modo *Headless* = Silencio absoluto. Solo habla el LLM.
    *   Persistencia en *Headless* = Solo si se pide explícitamente (`--session`).
*   **Entorno:** Los errores `404` en Ollama suelen ser porque el modelo no está descargado (`ollama pull`), no porque el código esté mal. Verificar el entorno antes de depurar el código.

---

**Fin del ciclo de análisis.**
