## 🔗 El Paradigma de Funciones Encadenadas (`|`) en LangChain

Vamos a visualizar las cadenas con flechas para que veas el flujo de datos. Este es el corazón de LangChain.

### 📊 Ejemplos Visuales de Cadenas (Pipelines)

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.1")

# ------------------- EJEMPLO 1: CADENA BÁSICA -------------------
# FLUJO: prompt → llm → parser
# DATOS: "tema" → prompt_template → {mensaje_formateado} → llm → {respuesta_AI} → parser → {string}

prompt = ChatPromptTemplate.from_template("Cuéntame un chiste sobre {tema}")
cadena_chiste = prompt | llm | StrOutputParser()

resultado = cadena_chiste.invoke({"tema": "programadores"})
# resultado = "string" (solo el texto del chiste)

# ------------------- EJEMPLO 2: RAG CON RETRIEVER -------------------
# FLUJO: pregunta → retriever → format_docs → prompt → llm → parser
# DATOS: "pregunta" → retriever → {docs} → format_docs → {contexto_string} → prompt → {mensaje} → llm → {respuesta} → parser → {string}

from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough

vectorstore = FAISS.from_texts(["LangChain es genial"], embedding=...)  # simplificado
retriever = vectorstore.as_retriever()

def format_docs(docs):
    return "\n".join(doc.page_content for doc in docs)

prompt_rag = ChatPromptTemplate.from_template("Contexto: {context}\nPregunta: {question}")

cadena_rag = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt_rag
    | llm
    | StrOutputParser()
)

resultado = cadena_rag.invoke("¿Qué es LangChain?")
# resultado = "LangChain es genial"

# ------------------- EJEMPLO 3: BRANCHING (CONDICIONAL) -------------------
# FLUJO: entrada → clasificador → (rama A o rama B) → respuesta

from langchain_core.runnables import RunnableBranch

# Clasificador: decide qué hacer
clasificador = prompt_clasificador | llm | StrOutputParser()

# Ramas
rama_chiste = prompt_chiste | llm | StrOutputParser()
rama_serio = prompt_serio | llm | StrOutputParser()

cadena_branch = (
    RunnablePassthrough.assign(categoria=clasificador)
    | RunnableBranch(
        (lambda x: x["categoria"] == "chiste", rama_chiste),
        (lambda x: x["categoria"] == "serio", rama_serio),
        rama_serio  # default
    )
)

# ------------------- EJEMPLO 4: AGENTE CON TOOL CALLING -------------------
# FLUJO COMPLEJO: input → agente (piensa) → (tool call o respuesta final) → loop

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool

@tool
def suma(x: int, y: int) -> int:
    """Suma dos números."""
    return x + y

herramientas = [suma]

# El agente ES una cadena: prompt | llm.bind_tools(herramientas) | parser_agente
agente = create_tool_calling_agent(llm, herramientas, prompt_agente)
ejecutor = AgentExecutor(agent=agente, tools=herramientas)

# El ejecutor maneja el loop automáticamente
resultado = ejecutor.invoke({"input": "suma 2 y 3"})
# resultado: el agente decide llamar suma(2,3) y luego responde "5"
```

## 🏗️ Arquitectura Industrial: "Fábrica de Agentes" con Componentes Modulares

Para diseñar un sistema donde puedas activar/desactivar herramientas y componentes desde otras carpetas, necesitas un patrón de **inyección de dependencias** o **fábrica de agentes**. Aquí te muestro una estructura industrial:

### 📁 Estructura de Carpetas
```
proyecto/
├── agentes/
│   ├── base/
│   │   ├── agente_base.py        # La cadena base
│   │   └── factory.py             # Fábrica de agentes
│   ├── herramientas/
│   │   ├── memoria/
│   │   │   └── memoria_permanente.py
│   │   ├── busqueda/
│   │   │   └── buscar_web.py
│   │   └── registro_herramientas.py  # Registro central
│   └── subagentes/
│       ├── agente_especialista1.py
│       └── agente_especialista2.py
├── config/
│   └── models.yaml
└── main.py
```

### 🏭 Código Industrial: Fábrica de Agentes

```python
# agentes/base/factory.py
import importlib
from typing import Dict, List, Any
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import BaseTool
from langchain_core.language_models import BaseLanguageModel

class AgentFactory:
    """Fábrica que construye agentes con herramientas inyectadas."""
    
    def __init__(self, llm: BaseLanguageModel):
        self.llm = llm
        self._herramientas_registradas = {}
        self._subagentes_registrados = {}
        
    def registrar_herramienta(self, nombre: str, ruta_modulo: str, clase_herramienta: str):
        """Registra una herramienta para poder activarla después."""
        self._herramientas_registradas[nombre] = {
            'ruta': ruta_modulo,
            'clase': clase_herramienta,
            'instancia': None  # Lazy loading
        }
    
    def registrar_subagente(self, nombre: str, ruta_modulo: str, clase_agente: str):
        """Registra un subagente como posible herramienta."""
        self._subagentes_registrados[nombre] = {
            'ruta': ruta_modulo,
            'clase': clase_agente,
            'instancia': None
        }
    
    def _cargar_herramienta(self, nombre: str) -> BaseTool:
        """Carga una herramienta bajo demanda (lazy loading)."""
        registro = self._herramientas_registradas.get(nombre)
        if not registro:
            raise ValueError(f"Herramienta {nombre} no registrada")
        
        if not registro['instancia']:
            # Importación dinámica
            modulo = importlib.import_module(registro['ruta'])
            clase = getattr(modulo, registro['clase'])
            registro['instancia'] = clase()
        
        return registro['instancia']
    
    def _cargar_subagente_como_herramienta(self, nombre: str) -> BaseTool:
        """Convierte un subagente en una herramienta."""
        registro = self._subagentes_registrados.get(nombre)
        if not registro:
            raise ValueError(f"Subagente {nombre} no registrado")
        
        if not registro['instancia']:
            modulo = importlib.import_module(registro['ruta'])
            clase = getattr(modulo, registro['clase'])
            # El subagente se instancia con su propia fábrica
            subagente = clase(llm=self.llm, factory=self)
            registro['instancia'] = subagente.as_tool()  # Método especial
        
        return registro['instancia']
    
    def crear_agente(self, 
                      nombre_agente: str,
                      herramientas_activas: List[str],
                      prompt_personalizado: ChatPromptTemplate = None,
                      incluir_subagentes: bool = False) -> AgentExecutor:
        """
        Crea un agente con un subconjunto activo de herramientas.
        
        Args:
            herramientas_activas: Lista de nombres de herramientas a incluir
            incluir_subagentes: Si True, incluye subagentes como herramientas
        """
        herramientas = []
        
        # Activar herramientas seleccionadas
        for nombre in herramientas_activas:
            herramienta = self._cargar_herramienta(nombre)
            herramientas.append(herramienta)
        
        # Activar subagentes si se pide
        if incluir_subagentes:
            for nombre in self._subagentes_registrados.keys():
                herramienta = self._cargar_subagente_como_herramienta(nombre)
                herramientas.append(herramienta)
        
        # Crear agente con las herramientas activas
        prompt = prompt_personalizado or self._prompt_base()
        agente = create_tool_calling_agent(self.llm, herramientas, prompt)
        
        return AgentExecutor(
            agent=agente,
            tools=herramientas,
            handle_parsing_errors=True,
            max_iterations=10  # Evita loops infinitos
        )
    
    def _prompt_base(self) -> ChatPromptTemplate:
        """Prompt base para agentes."""
        return ChatPromptTemplate.from_messages([
            ("system", "Eres un asistente útil con acceso a herramientas."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
```

### 🧰 Herramientas Ejemplo
```python
# agentes/herramientas/memoria/memoria_permanente.py
from langchain_core.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field

class MemoriaInput(BaseModel):
    dato: str = Field(description="Dato a guardar en memoria")

class GestionMemoriaPermanente(BaseTool):
    name: str = "gestion_memoria_permanente"
    description: str = "Guarda información importante en memoria a largo plazo"
    args_schema: Type[BaseModel] = MemoriaInput
    
    def _run(self, dato: str) -> str:
        # Lógica real de guardado
        print(f"🔵 GUARDANDO: {dato}")
        return f"Memorizado: {dato}"
    
    async def _arun(self, dato: str) -> str:
        return self._run(dato)
```

### 🤖 Subagente como Herramienta
```python
# agentes/subagentes/agente_especialista1.py
from langchain.agents import AgentExecutor
from langchain_core.tools import BaseTool, tool
from agentes.base.factory import AgentFactory

class AgenteMatematico:
    def __init__(self, llm, factory: AgentFactory):
        self.llm = llm
        self.factory = factory
        
        # Este subagente tiene sus PROPIAS herramientas
        self.ejecutor = factory.crear_agente(
            nombre_agente="matematico",
            herramientas_activas=["calculadora", "conversor_unidades"]
        )
    
    def as_tool(self) -> BaseTool:
        """Convierte este agente en una herramienta."""
        
        @tool(name="agente_matematico", 
              description="Úsalo para problemas matemáticos complejos")
        def tool_func(consulta: str) -> str:
            """Recibe una consulta matemática y devuelve resultado."""
            resultado = self.ejecutor.invoke({"input": consulta})
            return resultado['output']
        
        return tool_func
```

### 🎮 Uso Principal
```python
# main.py
from agentes.base.factory import AgentFactory
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# 1. Inicializar fábrica
llm = ChatOllama(model="llama3.1")
fabrica = AgentFactory(llm)

# 2. Registrar herramientas (desde diferentes carpetas)
fabrica.registrar_herramienta(
    nombre="memoria",
    ruta="agentes.herramientas.memoria.memoria_permanente",
    clase_herramienta="GestionMemoriaPermanente"
)

fabrica.registrar_herramienta(
    nombre="busqueda",
    ruta="agentes.herramientas.busqueda.buscar_web",
    clase_herramienta="BuscarWeb"
)

# 3. Registrar subagentes
fabrica.registrar_subagente(
    nombre="matematico",
    ruta="agentes.subagentes.agente_especialista1",
    clase_agente="AgenteMatematico"
)

# 4. Crear diferentes configuraciones de agentes
agente_memoria = fabrica.crear_agente(
    nombre_agente="memorizador",
    herramientas_activas=["memoria"],
    prompt_personalizado=ChatPromptTemplate.from_messages([
        ("system", "Eres un archivista. Guarda todo lo que te pidan."),
        ("human", "{input}")
    ])
)

agente_general = fabrica.crear_agente(
    nombre_agente="general",
    herramientas_activas=["memoria", "busqueda"],
    incluir_subagentes=True  # Incluye al agente matemático
)

# 5. Usar los agentes
resultado = agente_memoria.invoke({
    "input": "Recuerda que el proyecto usa LangChain 0.3"
})
print(resultado['output'])

resultado = agente_general.invoke({
    "input": "Resuelve 234 * 567 y guarda el resultado"
})
print(resultado['output'])
```

## 🔄 Mecanismos de Activación/Desactivación

1. **Lazy Loading**: Las herramientas se cargan SOLO cuando se activan en un agente. No se cargan todas al inicio.
2. **Inyección en Fábrica**: Cada agente recibe SOLO las herramientas que necesita en ese momento.
3. **Subagentes como Herramientas**: Los subagentes se convierten en herramientas mediante `as_tool()`, permitiendo:
   - **Patrón 1: Agente que se usa a sí mismo** (recursividad) → Cuidado con loops
   - **Patrón 2: Agente que usa otros agentes** → El agente general delega al matemático

## 📐 Diagrama de Flujo Completo
```
[CONFIG]                          [EJECUCIÓN]
models.yaml ─────────────────┐
                            ▼
[FÁBRICA] =====================|=======================
Llama3.1 + herramientas registradas
         │
         ├── activar("memoria") → AgenteA: [memoria]
         │                           │
         │                           └── invoke() → usa memoria
         │
         ├── activar("busqueda") → AgenteB: [busqueda]
         │                           │
         │                           └── invoke() → busca web
         │
         └── activar(["memoria", "busqueda"], 
                      incluir_subagentes=True) 
                                  → AgenteC: [memoria, busqueda, 
                                             agente_matematico_como_tool]
                                      │
                                      └── invoke() → "resuelve 2+2" 
                                          → delega a subagente_matemático
```

Este diseño industrial te permite:
- ✅ Activar/desactivar herramientas sin tocar código
- ✅ Subagentes que son herramientas para otros agentes
- ✅ Importación dinámica (no cargas todo en memoria)
- ✅ Cada agente es una cadena específica con sus herramientas
- ✅ Escalable: añadir nuevas herramientas = registrar y ya


ok repite tu respuesta de la fabrica es muy buena, pero organiza y explica de manera que sea evidente donde y como funcionan las cosas es decir creo que hay un objeto llamado agente pero no se donde está, creo que en algún momento se activan y desactivan las herramientas pero no se donde, y deberías desactivarse en tiempo de ejecución y activarse,  y skills, también, en alguna parte en una carpeta o varias ordenadas con sus herramientas posibles es decir una herramienta puede estar en la carpeta




skill o en la de herramientas pero dentro de una carpeta herramientas siempre, una o varias skills lo importante es que necesito poder visualizar bien donde están los codigos conectores debes incluso resaltar con flechas y hacer comentarios en mayusculas que unen las herramientas con los agentes como se levantan los agentes , etc la parte de carpetas y de codigo no logro sincronizarla en mimente y decir ha bieno esto esta aqui y hace esto y se une a esto con esto y cuando esto se llama o el agente se instancia entonces se activa la cadena tal que representa el agente y esta aqui y entonces de acuerdo al tipo de agente se levanta la sikill de esta forma con este "conector" que esta la sikll aqui y pues así...


Vamos a estructurar la respuesta para que sea ultra clara: primero la organización de carpetas, luego el flujo de ejecución con anotaciones, y finalmente los conectores. Usaré comentarios en mayúsculas y flechas para visualizar.

## 🗂️ Organización de Carpetas (VISUALIZACIÓN FÍSICA)

text

proyecto/
│
├── 📁 agentes/                          # ← TODOS LOS AGENTES VIVEN AQUÍ
│   │
│   ├── 📁 base/                          # ← FÁBRICA Y AGENTE BASE
│   │   ├── 🧩 agente_base.py              # → Define la CADENA BASE del agente
│   │   └── 🏭 factory.py                   # → FÁBRICA: CONSTRUYE AGENTES + ACTIVA HERRAMIENTAS
│   │
│   ├── 📁 herramientas/                   # ← TODAS LAS HERRAMIENTAS (SKILLS) VIVEN AQUÍ
│   │   ├── 📁 memoria/                     # → Skill específica
│   │   │   └── 🛠️ memoria_permanente.py    # → Código de la herramienta
│   │   ├── 📁 busqueda/                     # → Otra skill
│   │   │   └── 🛠️ buscar_web.py
│   │   └── 📋 registro_herramientas.py       # → REGISTRO CENTRAL (lista de skills disponibles)
│   │
│   └── 📁 subagentes/                      # ← SUBAGENTES (que son también herramientas)
│       ├── 🧠 agente_matematico.py          # → Define un agente como herramienta
│       └── 🧠 agente_traductor.py
│
├── 📁 config/                            # ← CONFIGURACIÓN GLOBAL
│   └── ⚙️ models.yaml                      # → Modelos disponibles (Ollama, DeepSeek...)
│
└── 🚀 main.py                             # ← PUNTO DE ENTRADA: levanta fábrica y crea agentes

## 🔍 FLUJO DE ACTIVACIÓN/DESACTIVACIÓN EN TIEMPO DE EJECUCIÓN

### 1️⃣ **Registro de herramientas** (ocurre al inicio, en `main.py`)

python

# main.py

from agentes.base.factory import AgentFactory
from langchain_ollama import ChatOllama

# 1. Crear la fábrica (UNA SOLA VEZ)

llm = ChatOllama(model="llama3.1")
fabrica = AgentFactory(llm)   # ← EL CORAZÓN: AQUÍ SE GESTIONAN TODAS LAS HERRAMIENTAS

# 2. REGISTRAR HERRAMIENTAS (decirle a la fábrica qué skills existen y dónde encontrarlas)

fabrica.registrar_herramienta(
    nombre="memoria",                        # ← NOMBRE PARA REFERENCIA
    ruta="agentes.herramientas.memoria.memoria_permanente",  # ← RUTA FÍSICA (carpeta/archivo)
    clase_herramienta="GestionMemoriaPermanente"             # ← CLASE DENTRO DE ESE ARCHIVO
)
fabrica.registrar_herramienta(
    nombre="busqueda",
    ruta="agentes.herramientas.busqueda.buscar_web",
    clase_herramienta="BuscarWeb"
)

# 3. REGISTRAR SUBAGENTES (también como posibles herramientas)

fabrica.registrar_subagente(
    nombre="matematico",
    ruta="agentes.subagentes.agente_matematico",
    clase_agente="AgenteMatematico"
)

### 2️⃣ **Activación en tiempo de ejecución** (cuando creamos un agente específico)

python

# main.py (continuación)

# 4. CREAR UN AGENTE CON UN CONJUNTO DE HERRAMIENTAS ACTIVAS

agente_memoria = fabrica.crear_agente(
    nombre_agente="memorizador",                    # ← SOLO PARA IDENTIFICAR
    herramientas_activas=["memoria"],                 # ← HERRAMIENTAS ACTIVAS AHORA (solo esta)
    # ... prompt opcional
)

# 5. USAR EL AGENTE

resultado = agente_memoria.invoke({
    "input": "Recuerda que el proyecto usa LangChain 0.3"
})

# → EN ESTE MOMENTO, EL AGENTE SOLO PUEDE USAR "memoria"

# 6. EN OTRO MOMENTO, CREAMOS OTRO AGENTE CON OTRAS HERRAMIENTAS

agente_general = fabrica.crear_agente(
    nombre_agente="general",
    herramientas_activas=["memoria", "busqueda"],     # ← ACTIVAS: memoria Y búsqueda
    incluir_subagentes=True                            # ← ACTIVA TAMBIÉN SUBAGENTES
)

# 7. AHORA ESTE AGENTE PUEDE USAR memoria, búsqueda Y el subagente matemático

resultado2 = agente_general.invoke({
    "input": "Resuelve 234*567 y guarda el resultado"
})

### 🔄 ¿DÓNDE ESTÁ EL OBJETO "AGENTE"?

- El **objeto agente** se crea **DENTRO DE LA FÁBRICA**, en el método `crear_agente()`.

- Vive en la variable que asignamos (`agente_memoria`, `agente_general`).

- Es un `AgentExecutor` de LangChain, que contiene:

  - El LLM (modelo)

  - Las herramientas activas (solo las que le pasamos)

  - El prompt

  - La lógica de ejecución (loop agente-herramientas)

### 🔧 ¿DÓNDE SE ACTIVAN/DESACTIVAN LAS HERRAMIENTAS?

- La **activación** ocurre **en el momento de crear el agente** (`fabrica.crear_agente`). Allí se seleccionan las herramientas que se incluirán.

- La **desactivación** no es dinámica sobre un agente ya creado (un agente ya tiene fijas sus herramientas). Para "desactivar" una herramienta en tiempo de ejecución, tendrías que:

  - Crear un nuevo agente con diferentes herramientas, o

  - Usar un mecanismo más avanzado (como routing) donde un agente principal decida no usar ciertas herramientas según el contexto.

Pero si lo que quieres es **cambiar las herramientas de un mismo agente mientras ejecuta**, eso no es posible directamente: el agente es una cadena fija. Lo que sí puedes hacer es tener un **agente orquestador** que decida qué subagente/herramienta usar en cada paso.

## 🔌 CONECTORES: CÓMO SE UNEN LAS PIEZAS (código con anotaciones)

### 🧩 **`agentes/base/agente_base.py`** (la cadena base)

python

# =====================================================

# CADENA BASE: Define cómo se construye un agente

# =====================================================

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
def crear_agente_base(llm, herramientas, prompt=None):
    """
    FÁBRICA INTERNA: Toma un LLM y una lista de herramientas (YA INSTANCIADAS)
    y devuelve un AGENTE EJECUTOR.

    ← ENTRADA: herramientas YA CARGADAS (objetos instanciados)
    → SALIDA: AgentExecutor listo para usar
    """
    if prompt is None:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un asistente útil."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])

    # ↓↓↓ AQUÍ SE UNE EL LLM CON LAS HERRAMIENTAS (bind_tools)
    agente = create_tool_calling_agent(llm, herramientas, prompt)

    # ↓↓↓ EJECUTOR: envuelve el agente y maneja el loop
    ejecutor = AgentExecutor(agent=agente, tools=herramientas)
    return ejecutor

### 🏭 **`agentes/base/factory.py`** (la fábrica)

python

# =====================================================

# FÁBRICA: Registro y creación bajo demanda

# =====================================================

import importlib
from .agente_base import crear_agente_base  # ← IMPORTA LA CADENA BASE
class AgentFactory:
    def __init__(self, llm):
        self.llm = llm
        self.registro_herramientas = {}   # ← DICCIONARIO: nombre -> metadatos
        self.registro_subagentes = {}      # ← DICCIONARIO: nombre -> metadatos

    def registrar_herramienta(self, nombre, ruta, clase_herramienta):
        """GUARDA LA REFERENCIA, pero NO CARGA LA HERRAMIENTA (lazy loading)."""
        self.registro_herramientas[nombre] = {
            'ruta': ruta,
            'clase': clase_herramienta,
            'instancia': None  # ← AÚN NO CARGADA
        }

    def _cargar_herramienta(self, nombre):
        """CARGA LA HERRAMIENTA SÓLO CUANDO SE NECESITA."""
        meta = self.registro_herramientas[nombre]
        if meta['instancia'] is None:
            # ↓↓↓ IMPORTACIÓN DINÁMICA: localiza el archivo físico
            modulo = importlib.import_module(meta['ruta'])
            clase = getattr(modulo, meta['clase'])
            meta['instancia'] = clase()  # ← INSTANCIA CREADA AQUÍ
        return meta['instancia']

    def crear_agente(self, herramientas_activas, incluir_subagentes=False):
        """CONSTRUYE UN AGENTE CON LAS HERRAMIENTAS ACTIVAS."""
        herramientas = []

        # ACTIVAR herramientas seleccionadas
        for nombre in herramientas_activas:
            if nombre in self.registro_herramientas:
                herramienta = self._cargar_herramienta(nombre)  # ← CARGA BAJO DEMANDA
                herramientas.append(herramienta)

        # ACTIVAR subagentes si se pide
        if incluir_subagentes:
            for nombre in self.registro_subagentes:
                # Cada subagente tiene un método .as_tool() que lo convierte en herramienta
                subagente_tool = self._cargar_subagente_como_herramienta(nombre)
                herramientas.append(subagente_tool)

        # ↓↓↓ PASA LAS HERRAMIENTAS YA INSTANCIADAS a la cadena base
        return crear_agente_base(self.llm, herramientas)

### 🛠️ **`agentes/herramientas/memoria/memoria_permanente.py`**

python

# =====================================================

# HERRAMIENTA INDIVIDUAL (SKILL)

# =====================================================

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
class MemoriaInput(BaseModel):
    dato: str = Field(description="Dato a guardar")
class GestionMemoriaPermanente(BaseTool):
    name = "gestion_memoria_permanente"
    description = "Guarda información importante en memoria a largo plazo"
    args_schema = MemoriaInput

    def _run(self, dato: str) -> str:
        # LÓGICA REAL DE LA HERRAMIENTA
        print(f"💾 Guardando: {dato}")
        return f"Memorizado: {dato}"

### 🧠 **`agentes/subagentes/agente_matematico.py`**

python

# =====================================================

# SUBAGENTE: ES UN AGENTE QUE SE CONVIERTE EN HERRAMIENTA

# =====================================================

from langchain.tools import tool
class AgenteMatematico:
    def __init__(self, llm, factory):
        self.llm = llm
        self.factory = factory
        # ESTE SUBAGENTE USA SUS PROPIAS HERRAMIENTAS (ej: calculadora)
        self.ejecutor = factory.crear_agente(
            herramientas_activas=["calculadora"]  # ← Otra herramienta registrada
        )

    def as_tool(self):
        """CONVIERTE ESTE SUBAGENTE EN UNA HERRAMIENTA PARA OTROS AGENTES."""
        @tool(name="agente_matematico", description="Resuelve problemas matemáticos")
        def tool_func(consulta: str) -> str:
            # CUANDO OTRO AGENTE LLAME A ESTA TOOL, SE EJECUTA EL SUBAGENTE
            resultado = self.ejecutor.invoke({"input": consulta})
            return resultado['output']
        return tool_func

## 🎯 RESUMEN VISUAL DE CONEXIONES

text

[main.py]
   │
   ├── 1. Crea fábrica:  fabrica = AgentFactory(llm)
   │
   ├── 2. REGISTRA herramientas (solo nombres y rutas):
   │      fabrica.registrar_herramienta("memoria", "ruta/a/memoria.py", "GestionMemoriaPermanente")
   │      fabrica.registrar_herramienta("busqueda", ...)
   │      fabrica.registrar_subagente("matematico", ...)
   │
   └── 3. CREA AGENTES bajo demanda:
          agenteA = fabrica.crear_agente(herramientas_activas=["memoria"])
                          │
                          └── [DENTRO DE crear_agente]
                               ├── Para cada herramienta activa:
                               │    └── _cargar_herramienta("memoria")
                               │         → importlib.import_module("ruta/a/memoria.py")
                               │         → instancia = GestionMemoriaPermanente()
                               │         ← herramienta instanciada
                               │
                               ├── (si incluye subagentes) igual para subagentes
                               │
                               └── llama a crear_agente_base(llm, [herramientas instanciadas])
                                    → create_tool_calling_agent → AgentExecutor
                                    ← retorna el agente listo
   agenteA.invoke(...)   → EL AGENTE USA SOLO LAS HERRAMIENTAS QUE SE LE PASARON

### 🔄 ¿CÓMO SE DESACTIVAN EN TIEMPO DE EJECUCIÓN?

- Si quieres que un mismo agente "desactive" una herramienta mientras conversa, necesitas un **agente orquestador** que tenga la lógica para no invocarla. Por ejemplo:

  - El agente recibe un mensaje, y basado en el contenido decide si usa la herramienta o no. Pero la herramienta sigue estando disponible (puede usarla si quiere).

- Si quieres **cambiar el conjunto de herramientas** para una nueva conversación, creas un nuevo agente con diferente lista de `herramientas_activas`. Eso es desactivar/activar en tiempo de ejecución desde la perspectiva del programa: puedes tener múltiples agentes con diferentes skills.

## 📦 EJEMPLO DE USO EN CONSOLA (simulación)

bash

$ python main.py
Registrando herramientas...

- memoria
- busqueda
- subagente: matematico
  Creando agente memorizador (solo memoria)...
  Agente listo. Escribe tu mensaje:
  Tú: Recuerda que mi color favorito es azul
  💾 Guardando: mi color favorito es azul
  Agente: OK, he memorizado que tu color favorito es azul.
  Creando agente general (memoria + búsqueda + subagente matemático)...
  Agente listo.
  Tú: Resuelve 123 * 456 y guarda el resultado

  # El agente usa primero el subagente matemático para calcular, luego memoria para guardar

---

## Parte 1: Arquitectura General del Sistema (Confirmación y Detalle)

Tu visión es correcta y se alinea con un **producto instalable on-premise** (no SaaS) donde tú generas valor en la instalación, configuración, enseñanza y soluciones a medida. La arquitectura debe ser **declarativa** (YAML) para que los administradores puedan definir agentes sin tocar código, y **modular** para que puedas añadir herramientas (skills) fácilmente.

### Componentes Clave de la Arquitectura

1.  **Capa de Configuración (Declarativa)** :
    *   `models.yaml`: Define los modelos disponibles (proveedor, nombre, parámetros por defecto como temperatura, top_p, etc.). Ejemplo:
        ```yaml
        models:
          - id: gemma-ollama
            provider: ollama
            config:
              model: "gemma3:4b"
              base_url: "http://localhost:11434"
              temperature: 0.7
          - id: deepseek-pro
            provider: deepseek
            config:
              model: "deepseek-chat"
              api_key: "ENV"  # Se toma de variable de entorno
        ```
    *   `agentes.yaml`: Define los agentes. Cada agente tiene:
        *   `id`: Identificador único.
        *   `modelo`: Referencia a un modelo de `models.yaml`.
        *   `herramientas`: Lista de herramientas (skills) que puede usar. Aquí se define qué herramientas están **disponibles** para ese agente.
        *   `herramientas_activas_por_defecto`: (opcional) Subconjunto de las disponibles que se activan al inicio.
        *   `memoria`: Configuración de memoria (documentos, chat).
        *   `prompt`: Prompt de sistema personalizado.
        *   `parámetros`: (opcional) Sobrescribe los del modelo.

2.  **Capa de Núcleo (Core)** :
    *   **Fábrica de Agentes (`AgentFactory`)**: Es el cerebro. Lee los YAML, registra las herramientas (escaneando carpetas o con registro manual), y construye agentes bajo demanda. Implementa **lazy loading**: las herramientas solo se instancian cuando se necesitan.
    *   **Agente Base**: La cadena fundamental de LangChain (`create_tool_calling_agent` + `AgentExecutor`).
    *   **Gestores de Memoria**:
        *   `DocumentMemory`: Maneja RAG sobre documentos. Usa un vectorstore (Chroma, FAISS) con embeddings. Los documentos se indexan con **metadatos ontológicos** (etiquetas, categorías, fecha) para permitir filtrado. Esto es clave para tu idea de "puntos de conocimiento con metadatos ontológicos".
        *   `ChatMemory`: Almacena historiales de conversación en una base de datos SQL (por usuario, sesión, fecha). Puede incluir un campo `titulo` para la sesión, que podría ser generado por un LLM al final de la misma (o al principio, configurable). Adicionalmente, puede tener una opción para vectorizar los mensajes y permitir búsqueda semántica sobre conversaciones pasadas.

3.  **Capa de Herramientas (Skills)** :
    *   Cada herramienta es una clase Python que hereda de `BaseTool` de LangChain.
    *   Se organizan en carpetas dentro de `herramientas/` (ej: `herramientas/memoria/`, `herramientas/busqueda/`).
    *   El **registro** puede ser automático (escaneando el directorio) o manual (en un `__init__.py` que exporte un diccionario). Para un producto instalable, el registro automático es más amigable para el usuario final (solo coloca la herramienta en la carpeta y ya).

4.  **Capa de Interfaz (CLI)** :
    *   Un punto de entrada (`cli.py`) que:
        *   Acepta parámetros como `--agente` para seleccionar el agente inicial.
        *   Proporciona comandos en tiempo de ejecución:
            *   `/tool list` - Lista herramientas disponibles.
            *   `/tool activate <nombre>` - Activa una herramienta.
            *   `/tool deactivate <nombre>` - Desactiva una herramienta.
            *   `/model <id>` - Cambia de modelo (recargando el agente).
            *   `/memory` - Ver/gestión de memoria (quizá).
            *   `/exit`
        *   Implementa el streaming con cancelación por Ctrl+C (como ya logramos).

### Flujo de Activación/Desactivación en Tiempo de Ejecución

*   **Activación inicial**: Al crear un agente con `factory.crear_agente_por_id("investigador")`, se cargan las herramientas listadas en `herramientas_activas_por_defecto` (o todas las disponibles si no se especifica).
*   **Cambio dinámico**: En la CLI, el comando `/tool activate X` hace lo siguiente:
    1.  Añade `X` al conjunto de herramientas activas del agente actual.
    2.  **Reconstruye el agente** (o crea uno nuevo) con la nueva lista de herramientas activas. Esto es necesario porque en LangChain el binding de herramientas al agente es estático. La reconstrucción es rápida gracias al lazy loading: las herramientas ya registradas se instancian solo si es necesario.
    3.  El nuevo agente reemplaza al anterior en la sesión.
*   **Desactivación**: similar, quitando la herramienta del conjunto y reconstruyendo.

Este enfoque es simple y efectivo para un producto instalable. No requiere un sistema complejo de agentes dinámicos en caliente.

---

## Parte 2: Ejemplos de Código (Conectando las Piezas)

Voy a mostrarte cómo se conectan físicamente los archivos, con comentarios en mayúsculas para que veas el flujo.

### Estructura de Carpetas (Refinada)

```
proyecto/
├── config/
│   ├── models.yaml                 # ← DEFINE MODELOS DISPONIBLES
│   └── agentes.yaml                 # ← DEFINE AGENTES (QUÉ HERRAMIENTAS Y MEMORIA USAN)
│
├── core/
│   ├── factory.py                    # ← FÁBRICA: LEE CONFIG, REGISTRA HERRAMIENTAS, CONSTRUYE AGENTES
│   ├── base_agent.py                 # ← CADENA BASE DEL AGENTE (create_tool_calling_agent)
│   └── memory/
│       ├── document_memory.py         # ← GESTOR DE MEMORIA DE DOCUMENTOS (RAG + METADATOS)
│       └── chat_memory.py             # ← GESTOR DE MEMORIA DE CHAT (SQL + OPCIONAL VECTORES)
│
├── herramientas/                      # ← TODAS LAS SKILLS VIVEN AQUÍ
│   ├── __init__.py                     # ← REGISTRO DE HERRAMIENTAS (AUTOMÁTICO O MANUAL)
│   ├── memoria/
│   │   └── permanente.py               # ← HERRAMIENTA CONCRETA
│   ├── busqueda/
│   │   └── web.py
│   └── calculadora/
│       └── calc.py
│
├── subagentes/                         # ← SUBAGENTES (QUE SON TAMBIÉN HERRAMIENTAS)
│   ├── matematico.py
│   └── traductor.py
│
├── cli/
│   └── main.py                          # ← PUNTO DE ENTRADA CLI
│
├── datos/
│   ├── documentos/                      # ← DOCUMENTOS PARA INDEXAR (EL USUARIO LOS PONE AQUÍ)
│   ├── vectorstore/                      # ← ÍNDICES VECTORIALES (SE GENERAN)
│   └── chat_history.db                   # ← BASE DE DATOS SQL DE HISTORIALES
│
├── scripts/
│   └── indexar_documentos.py             # ← SCRIPT PARA INDEXAR DOCUMENTOS (FUERA DE LA CLI)
│
├── requirements.txt
└── install.sh
```

### Ejemplo de `config/agentes.yaml`

```yaml
# config/agentes.yaml
agentes:
  - id: archivista
    modelo: gemma-ollama
    herramientas_disponibles:
      - memoria_permanente
      - calculadora        # Aunque tenga calculadora, no la activa por defecto
    herramientas_activas_por_defecto:
      - memoria_permanente
    memoria:
      documentos:
        enabled: true
        path: "datos/vectorstore/archivista"  # Ruta al índice
        filtros: ["categoria", "fecha"]       # Metadatos que se pueden filtrar
      chat:
        enabled: true
        db_path: "datos/chat_history.db"
    prompt: "Eres un archivista. Guarda todo lo que te pidan y responde basado en lo que recuerdas."
    temperatura: 0.3

  - id: investigador
    modelo: deepseek-pro
    herramientas_disponibles:
      - memoria_permanente
      - busqueda_web
      - agente_matematico   # Subagente como herramienta
    herramientas_activas_por_defecto:
      - memoria_permanente
      - busqueda_web
    memoria:
      documentos:
        enabled: true
        path: "datos/vectorstore/investigador"
      chat:
        enabled: true
    prompt: "Eres un investigador. Usa la memoria y la búsqueda web para responder."
    top_p: 0.9
```

### Código de la Fábrica (`core/factory.py`) con Anotaciones de Conexión

```python
# ============================================================
# core/factory.py
# FÁBRICA: LEE CONFIGURACIÓN, REGISTRA HERRAMIENTAS Y CONSTRUYE AGENTES
# ============================================================
import yaml
import importlib
import os
from typing import Dict, List, Optional
from langchain.agents import AgentExecutor
from langchain_ollama import ChatOllama
from langchain_deepseek import ChatDeepSeek

# Importaciones de nuestros módulos
from .base_agent import crear_agente_base
from .memory.document_memory import DocumentMemory
from .memory.chat_memory import ChatMemory

class AgentFactory:
    def __init__(self, config_dir: str = "config"):
        # 1. CARGAR CONFIGURACIÓN DESDE YAML
        with open(os.path.join(config_dir, "models.yaml")) as f:
            self.models_config = {m['id']: m for m in yaml.safe_load(f)['models']}
        with open(os.path.join(config_dir, "agentes.yaml")) as f:
            self.agentes_config = {a['id']: a for a in yaml.safe_load(f)['agentes']}

        # 2. REGISTRO DE HERRAMIENTAS (SKILLS)
        #    AQUÍ SE ESCANEAN LAS CARPETAS DE HERRAMIENTAS Y SUBAGENTES
        self.herramientas_registradas = self._escanear_herramientas()
        self.subagentes_registrados = self._escanear_subagentes()

        # 3. CACHÉ PARA INSTANCIAS DE HERRAMIENTAS (LAZY LOADING)
        self._instancias_herramientas = {}
        self._instancias_subagentes = {}

    def _escanear_herramientas(self) -> Dict[str, Dict]:
        """Escanea la carpeta 'herramientas' y registra las herramientas encontradas.
        ← ENTRADA: Archivos Python en herramientas/**/*.py
        → SALIDA: Diccionario {nombre_herramienta: {'ruta': 'modulo.ruta', 'clase': 'NombreClase'}}
        """
        herramientas = {}
        base_path = "herramientas"
        # Lógica de escaneo (simplificada)
        # Por cada archivo .py que contenga una clase que herede de BaseTool,
        # se añade al registro.
        # EJEMPLO: Si encuentra herramientas/memoria/permanente.py con clase MemoriaPermanente,
        # registra: 'memoria_permanente' -> {'ruta': 'herramientas.memoria.permanente', 'clase': 'MemoriaPermanente'}
        return herramientas

    def _escanear_subagentes(self) -> Dict[str, Dict]:
        """Similar, pero para subagentes."""
        pass

    def _cargar_herramienta(self, nombre: str):
        """CARGA UNA HERRAMIENTA BAJO DEMANDA (LAZY LOADING).
        ← ENTRADA: nombre de la herramienta
        → SALIDA: instancia de la herramienta (objeto BaseTool)
        """
        if nombre not in self._instancias_herramientas:
            registro = self.herramientas_registradas[nombre]
            modulo = importlib.import_module(registro['ruta'])
            clase = getattr(modulo, registro['clase'])
            self._instancias_herramientas[nombre] = clase()
        return self._instancias_herramientas[nombre]

    def _cargar_subagente_como_herramienta(self, nombre: str):
        """CARGA UN SUBAGENTE Y LO CONVIERTE EN HERRAMIENTA.
        ← ENTRADA: nombre del subagente
        → SALIDA: herramienta (funcióntool) que ejecuta al subagente
        """
        if nombre not in self._instancias_subagentes:
            registro = self.subagentes_registrados[nombre]
            modulo = importlib.import_module(registro['ruta'])
            clase = getattr(modulo, registro['clase'])
            # El subagente necesita la fábrica para poder crear sus propios agentes
            subagente = clase(llm_provider=self._cargar_modelo, factory=self)
            self._instancias_subagentes[nombre] = subagente.as_tool()
        return self._instancias_subagentes[nombre]

    def _cargar_modelo(self, modelo_id: str):
        """CARGA UN MODELO SEGÚN SU CONFIGURACIÓN.
        ← ENTRADA: id del modelo (ej: 'gemma-ollama')
        → SALIDA: instancia de ChatOllama o ChatDeepSeek
        """
        config = self.models_config[modelo_id]
        if config['provider'] == 'ollama':
            return ChatOllama(**config['config'])
        elif config['provider'] == 'deepseek':
            # La API key se toma de variable de entorno
            return ChatDeepSeek(**config['config'])
        # ... otros proveedores

    def _configurar_memoria(self, memoria_config: dict):
        """CONFIGURA LOS GESTORES DE MEMORIA SEGÚN LO DEFINIDO EN agentes.yaml.
        ← ENTRADA: sección 'memoria' de la config del agente
        → SALIDA: tupla (doc_memory, chat_memory) o None si no están habilitadas
        """
        doc_memory = None
        chat_memory = None
        if memoria_config.get('documentos', {}).get('enabled'):
            doc_memory = DocumentMemory(
                persist_directory=memoria_config['documentos']['path'],
                embedding_model=...  # Podría venir de config
            )
        if memoria_config.get('chat', {}).get('enabled'):
            chat_memory = ChatMemory(
                db_path=memoria_config['chat'].get('db_path', 'datos/chat_history.db')
            )
        return doc_memory, chat_memory

    def crear_agente_por_id(self, agente_id: str) -> AgentExecutor:
        """MÉTODO PRINCIPAL: CONSTRUYE UN AGENTE SEGÚN SU ID.
        ← ENTRADA: id del agente (ej: 'investigador')
        → SALIDA: AgentExecutor listo para usar
        """
        # 1. OBTENER CONFIGURACIÓN DEL AGENTE
        config = self.agentes_config[agente_id]

        # 2. CARGAR MODELO
        llm = self._cargar_modelo(config['modelo'])

        # 3. CARGAR HERRAMIENTAS ACTIVAS POR DEFECTO
        herramientas_activas = []
        for nombre_herramienta in config.get('herramientas_activas_por_defecto', []):
            if nombre_herramienta in self.herramientas_registradas:
                herramienta = self._cargar_herramienta(nombre_herramienta)
                herramientas_activas.append(herramienta)
            elif nombre_herramienta in self.subagentes_registrados:
                herramienta = self._cargar_subagente_como_herramienta(nombre_herramienta)
                herramientas_activas.append(herramienta)

        # 4. CONFIGURAR MEMORIA
        doc_memory, chat_memory = self._configurar_memoria(config.get('memoria', {}))

        # 5. CONSTRUIR AGENTE BASE (LLM + HERRAMIENTAS)
        #    AQUÍ SE USA LA CADENA BASE DE LANGCHAIN
        agente = crear_agente_base(
            llm=llm,
            herramientas=herramientas_activas,
            prompt=config.get('prompt'),
            temperature=config.get('temperatura')  # Podría sobrescribir
        )

        # 6. (OPCIONAL) AÑADIR MEMORIA AL EJECUTOR
        #    La memoria de chat se puede añadir como callback o como parte del estado.
        #    Por ahora, la dejamos para que la CLI la use.
        agente.memoria_docs = doc_memory
        agente.memoria_chat = chat_memory

        return agente
```

### Ejemplo de Herramienta (`herramientas/memoria/permanente.py`)

```python
# ============================================================
# herramientas/memoria/permanente.py
# HERRAMIENTA: MEMORIA PERMANENTE (SKILL)
# ============================================================
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class MemoriaInput(BaseModel):
    accion: str = Field(description="'guardar' o 'recuperar'")
    dato: str = Field(description="El dato a guardar o la consulta a recuperar")

class MemoriaPermanente(BaseTool):
    name = "memoria_permanente"
    description = "Guarda o recupera información importante de la memoria a largo plazo."
    args_schema: Type[BaseModel] = MemoriaInput

    def _run(self, accion: str, dato: str) -> str:
        # AQUÍ SE CONECTARÍA CON EL SISTEMA DE MEMORIA REAL
        # (ej: una base de datos vectorial)
        if accion == "guardar":
            # Llamar a doc_memory.add_documents(...)
            return f"Guardado: {dato}"
        elif accion == "recuperar":
            # Llamar a doc_memory.search(...)
            return f"Resultado de búsqueda para '{dato}'"
        else:
            return "Acción no válida"
```

### Ejemplo de Subagente (`subagentes/matematico.py`)

```python
# ============================================================
# subagentes/matematico.py
# SUBAGENTE: SE COMPORTA COMO HERRAMIENTA PARA OTROS AGENTES
# ============================================================
from langchain.tools import tool
from core.factory import AgentFactory  # para type hints

class AgenteMatematico:
    def __init__(self, llm_provider, factory: AgentFactory):
        self.factory = factory
        # ESTE SUBAGENTE USA SUS PROPIAS HERRAMIENTAS
        self.ejecutor = factory.crear_agente_por_id("matematico_interno")
        # Nota: "matematico_interno" sería otro agente definido en agentes.yaml,
        # con herramientas como calculadora, etc.

    def as_tool(self):
        @tool(name="agente_matematico", description="Resuelve problemas matemáticos complejos.")
        def tool_func(consulta: str) -> str:
            resultado = self.ejecutor.invoke({"input": consulta})
            return resultado['output']
        return tool_func
```

### CLI con Comandos de Activación/Desactivación (`cli/main.py`)

```python
# ============================================================
# cli/main.py
# PUNTO DE ENTRADA: CLI INTERACTIVA
# ============================================================
import argparse
import sys
sys.path.append("..")  # Para poder importar core

from core.factory import AgentFactory

class ChatCLI:
    def __init__(self, factory: AgentFactory, agente_id: str):
        self.factory = factory
        self.agente_id = agente_id
        self.agente = factory.crear_agente_por_id(agente_id)
        # Guardamos las herramientas activas para poder modificarlas
        self.herramientas_activas = set(
            factory.agentes_config[agente_id].get('herramientas_activas_por_defecto', [])
        )
        self.session_id = None  # Para memoria de chat

    def _reconstruir_agente(self):
        """Reconstruye el agente con las herramientas activas actuales."""
        # Modificamos la configuración temporalmente
        config = self.factory.agentes_config[self.agente_id].copy()
        config['herramientas_activas_por_defecto'] = list(self.herramientas_activas)
        # Creamos un nuevo agente
        self.agente = self.factory.crear_agente_por_id(self.agente_id)  # Usa la config original, necesitamos un método más flexible
        # Para simplificar, añadimos un método en factory que permita crear con herramientas custom
        # Pero en este ejemplo, asumimos que factory puede crear con lista explícita

    def run(self):
        print(f"--- Modo Chat Interactivo ---")
        print(f"Agente: {self.agente_id}")
        print(f"Herramientas activas: {', '.join(self.herramientas_activas)}")
        print("Comandos: /tool list | /tool activate <nombre> | /tool deactivate <nombre> | /exit")

        while True:
            try:
                user_input = input("\nTú: ").strip()
            except KeyboardInterrupt:
                print("\n(Interrumpido)")
                continue

            if not user_input:
                continue

            # Procesar comandos
            if user_input.startswith('/'):
                partes = user_input.split()
                cmd = partes[0].lower()

                if cmd == '/exit':
                    break
                elif cmd == '/tool' and len(partes) >= 2:
                    subcmd = partes[1]
                    if subcmd == 'list':
                        print("Herramientas disponibles:", list(self.factory.herramientas_registradas.keys()))
                    elif subcmd == 'activate' and len(partes) == 3:
                        nombre = partes[2]
                        if nombre in self.factory.herramientas_registradas or nombre in self.factory.subagentes_registrados:
                            self.herramientas_activas.add(nombre)
                            self._reconstruir_agente()
                            print(f"Herramienta '{nombre}' activada.")
                        else:
                            print(f"Herramienta '{nombre}' no encontrada.")
                    elif subcmd == 'deactivate' and len(partes) == 3:
                        nombre = partes[2]
                        if nombre in self.herramientas_activas:
                            self.herramientas_activas.discard(nombre)
                            self._reconstruir_agente()
                            print(f"Herramienta '{nombre}' desactivada.")
                        else:
                            print(f"Herramienta '{nombre}' no está activa.")
                else:
                    print("Comando no reconocido.")
                continue

            # Invocar al agente
            respuesta = self.agente.invoke({"input": user_input})
            print(f"Agente: {respuesta['output']}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--agente', required=True, help='ID del agente a usar')
    args = parser.parse_args()

    factory = AgentFactory(config_dir="../config")
    cli = ChatCLI(factory, args.agente)
    cli.run()

if __name__ == "__main__":
    main()
```

---

## Parte 3: Consideraciones y Próximos Pasos

### Activación/Desactivación en Tiempo de Ejecución
*   **Mecanismo**: Reconstruir el agente con la nueva lista de herramientas es simple y efectivo. La fábrica debe permitir crear un agente con una lista explícita de herramientas, no solo basada en la configuración YAML. Podemos añadir un método `crear_agente_con_herramientas(agente_id, herramientas_activas)`.
*   **Rendimiento**: La reconstrucción es rápida porque:
    *   El modelo ya está cargado (se reutiliza la instancia).
    *   Las herramientas se cargan lazy, así que si ya estaban instanciadas, se reutilizan.
    *   La creación del `AgentExecutor` es ligera.

### Memoria Dual
*   **Memoria de documentos**: Integra con Chroma o FAISS. Los metadatos ontológicos se pueden añadir al indexar los documentos (ej: categoría, tags, fecha). Luego, en la búsqueda, se pueden usar filtros. Para ontologías más complejas, podrías usar una base de datos de grafos (como Neo4j) o Cognee, pero eso es un paso más avanzado.
*   **Memoria de chat**: SQLite es suficiente. Para la vectorización de historiales, puedes tener un proceso asíncrono que tome los mensajes y los indexe en otro vectorstore. O puedes integrarlo en el flujo: al guardar un mensaje, también se guarda su embedding en una tabla aparte.

### Instalación en Empresas
*   **Script de instalación** (`install.sh`):
    1.  Crear entorno virtual.
    2.  Instalar dependencias (`pip install -r requirements.txt`).
    3.  Crear carpetas `datos/documentos`, `datos/vectorstore`, etc.
    4.  Copiar archivos de configuración de ejemplo (`models.yaml.example` a `models.yaml`).
    5.  Dar instrucciones para editar YAML y colocar documentos.
*   **Indexación de documentos**: Un script separado (`scripts/indexar_documentos.py`) que recorra `datos/documentos`, los divida, genere embeddings y los guarde en `datos/vectorstore/...` con metadatos.

### Siguientes Pasos Concretos (Te recomiendo este orden)

1.  **Definir los YAML finales** (models.yaml, agentes.yaml) con la estructura que te he mostrado.
2.  **Implementar el escaneo automático de herramientas** en `factory.py`. Puedes usar `pkgutil` o `os.walk` para encontrar clases que hereden de `BaseTool`.
3.  **Completar la fábrica** con los métodos de carga de modelos y construcción de agentes.
4.  **Implementar la CLI** con los comandos de activación/desactivación.
5.  **Añadir la memoria de chat** (SQLite) y probar que el historial se guarda por sesión.
6.  **Añadir la memoria de documentos** con un script de indexación aparte.
7.  **Empaquetar** con install.sh y probar en una máquina limpia.

### Reflexión Final
Tu visión de un producto instalable con configuración YAML, herramientas modulares y memoria dual es sólida y sigue el principio del "gato que cace ratones" (simple pero funcional). La arquitectura que hemos detallado te permite:

*   **Ganar instalando**: Cada cliente requiere configuración inicial (YAML, indexación de sus documentos).
*   **Ganar configurando**: Puedes ajustar agentes según necesidades específicas.
*   **Ganar enseñando**: Ofrecer formación sobre cómo crear nuevas herramientas o ajustar prompts.
*   **Ganar creando soluciones**: Desarrollar herramientas personalizadas para problemas puntuales.


**Sí — puedes tener agentes modulares que activen/desactiven herramientas y guardar la memoria de chat en SQLite por usuario/sesión/fecha/título; a continuación te explico, paso a paso, dónde está cada pieza, cómo se conectan y te doy código claro listo para copiar (fácil de adaptar).**

La solución que propongo usa: 1) una FÁBRICA de agentes que registra y carga herramientas (lazy loading), 2) herramientas/skills organizadas en carpetas, 3) subagentes convertidos en herramientas cuando hace falta, y 4) memoria de chat persistente en SQLite (por usuario, sesión, fecha, título). Abajo verás la estructura de carpetas, el flujo (con flechas y comentarios MAYÚSCULAS), y ejemplos de código concretos: fábrica, herramienta, subagente y la memoria SQLite con SQLAlchemy.

```text
RELEVANTE: enlaces de referencia (doc oficial LangChain que usé):
- [Ollama integration](https://docs.langchain.com/oss/python/integrations/providers/ollama)
- [Build a SQL agent](https://docs.langchain.com/oss/python/langchain/sql-agent)
- [SQLite provider](https://docs.langchain.com/oss/python/integrations/providers/sqlite)
- [Long-term memory](https://docs.langchain.com/oss/python/langchain/long-term-memory)
- [LangGraph persistence / checkpointers](https://docs.langchain.com/oss/python/langgraph/persistence)
```

## 1) Estructura de carpetas (CLARA y visual)
Luego de esto sabrás exactamente "dónde está el objeto agente", "dónde están las herramientas", "dónde está la memoria" y cómo se activan/desactivan.

```
proyecto/
├─ config/
│  ├─ models.yaml            # modelos (ej: ollama gemma3)
│  └─ agentes.yaml           # definición declarativa de agentes y herramientas por agente
├─ core/
│  ├─ factory.py            # FÁBRICA: registra, lazy-load, crea agentes
│  ├─ base_agent.py         # función que une LLM + herramientas -> AgentExecutor
│  └─ memory_sql.py         # helper para SQLite con SQLAlchemy (chat history)
├─ herramientas/            # AQUÍ viven todas las skills (una o muchas por carpeta)
│  ├─ memoria/
│  │  └─ permanente.py      # skill: guarda/lee en vectorstore o DB
│  ├─ busqueda/
│  │  └─ buscar_web.py
│  └─ __init__.py           # opcional: registro estático o helper de descubrimiento
├─ subagentes/
│  └─ matematico.py         # ejemplo: subagente convertido en tool
├─ datos/
│  └─ chat_history.db       # SQLite (puede generarse automáticamente)
├─ cli/
│  └─ main.py               # CLI que crea la fábrica y ejecuta agentes
└─ requirements.txt
```

## 2) Resumen del flujo (FLECHAS + COMENTARIOS EN MAYÚSCULAS)
- main.py → crea instancia AgentFactory (AQUÍ SE GUARDA EL OBJETO FÁBRICA)
- AgentFactory.registrar_herramienta(...) → registra nombre → ruta de módulo → clase (NO INSTANCIA AÚN)
- Al crear un agente: AgentFactory.crear_agente(...) → LA FÁBRICA:
  - carga modelo (ej. ChatOllama)
  - carga herramientas activas (lazy: importlib + instancia)
  - construye agente con base_agent.crear_agente_base(llm, herramientas)
  - devuelve AgentExecutor (este es EL OBJETO AGENTE que usarás: .invoke / .ainvoke)
- Cuando deseas activar/desactivar una tool en tiempo real:
  - actualizas la lista de herramientas activas y RECONSTRUYES el agente (rápido si el LLM se reutiliza)
- Memoria chat (SQLite): core/memory_sql.py gestiona guardar mensajes con campos:
  - user_id, session_id, session_title, timestamp, role, content, metadata

(EN MAYÚSCULAS: EL "OBJETO AGENTE" ESTÁ DENTRO DE LA FÁBRICA CUANDO LLAMAS crear_agente; las tools están en herramientas/; la memoria en datos/chat_history.db)

---

## 3) Código mínimo y limpio — copia/pega y adapta

1) core/base_agent.py — Une LLM + tools → AgentExecutor
```python
# core/base_agent.py
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

def crear_agente_base(llm, herramientas, prompt_system: str | None = None):
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_system or "Eres un asistente útil con acceso a herramientas."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    agente = create_tool_calling_agent(llm, herramientas, prompt)
    ejecutor = AgentExecutor(agent=agente, tools=herramientas)
    return ejecutor
```

2) core/memory_sql.py — SQLite con SQLAlchemy para chat history (por user/session/title)
```python
# core/memory_sql.py
from datetime import datetime
from sqlalchemy import (
    create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
)
from sqlalchemy.orm import sessionmaker

class ChatSQLMemory:
    def __init__(self, db_path: str = "datos/chat_history.db"):
        self.db_uri = f"sqlite:///{db_path}"
        self.engine = create_engine(self.db_uri, connect_args={"check_same_thread": False})
        self.metadata = MetaData()
        self.table = Table(
            "chat_history", self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("user_id", String, nullable=False),         # USUARIO
            Column("session_id", String, nullable=False),      # SESIÓN
            Column("session_title", String, nullable=True),    # TÍTULO
            Column("role", String, nullable=False),            # 'user'|'assistant'|'tool'
            Column("content", Text, nullable=False),
            Column("created_at", DateTime, default=datetime.utcnow),
        )
        self.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_message(self, user_id: str, session_id: str, role: str, content: str, session_title: str | None = None):
        s = self.Session()
        s.execute(self.table.insert().values(
            user_id=user_id, session_id=session_id, role=role, content=content,
            session_title=session_title, created_at=datetime.utcnow()
        ))
        s.commit()
        s.close()

    def get_messages(self, user_id: str, session_id: str, limit: int = 100):
        s = self.Session()
        q = s.query(self.table).filter_by(user_id=user_id, session_id=session_id).order_by(self.table.c.created_at)
        rows = q.limit(limit).all()
        s.close()
        return rows

    def list_sessions(self, user_id: str):
        s = self.Session()
        rows = s.query(self.table.c.session_id, self.table.c.session_title).filter_by(user_id=user_id).distinct().all()
        s.close()
        return rows
```

3) herramientas/memoria/permanente.py — ejemplo de tool (BaseTool)
```python
# herramientas/memoria/permanente.py
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class MemoriaInput(BaseModel):
    accion: str = Field(description="guardar|recuperar")
    texto: str = Field(description="contenido o query")

class MemoriaPermanente(BaseTool):
    name = "memoria_permanente"
    description = "Guarda o recupera texto en la memoria persistente (vectorstore o DB)."
    args_schema: Type[BaseModel] = MemoriaInput

    def __init__(self, memory_store=None):
        super().__init__()
        self.memory_store = memory_store  # opcional: inyectar doc memory

    def _run(self, accion: str, texto: str) -> str:
        if accion == "guardar":
            # Ejemplo simple: delegar a memory_store si existe
            if self.memory_store:
                self.memory_store.add(texto)
                return "Guardado en memoria."
            return f"Guardado: {texto}"
        elif accion == "recuperar":
            if self.memory_store:
                return self.memory_store.search(texto)
            return f"Resultado búsqueda (simulado) para: {texto}"
        else:
            return "Acción inválida. Usa 'guardar' o 'recuperar'."

    async def _arun(self, accion: str, texto: str) -> str:
        return self._run(accion, texto)
```

4) subagentes/matematico.py — ejemplo de subagente convertido en tool
```python
# subagentes/matematico.py
from langchain.tools import tool
from typing import Any

class AgenteMatematico:
    def __init__(self, factory=None):
        self.factory = factory
        # podría crear su propio executor interno si quisiera

    def as_tool(self):
        @tool(name="agente_matematico", description="Resuelve cálculos matemáticos complejos")
        def tool_func(expr: str) -> str:
            # implementación mínima: eval seguro (mejor: usar parser aritmético real)
            try:
                # NO usar eval en producción sin sanitizar
                result = eval(expr, {"__builtins__": {}})
                return str(result)
            except Exception as e:
                return f"Error en cálculo: {e}"
        return tool_func
```

5) core/factory.py — fábrica que registra y crea agentes (lazy load)
```python
# core/factory.py
import importlib
from typing import Dict, Any, List
from langchain_ollama import ChatOllama
from .base_agent import crear_agente_base
from .memory_sql import ChatSQLMemory

class AgentFactory:
    def __init__(self, model_config: Dict[str, Any]):
        # model_config: dict con key -> proveedor/config
        self.model_config = model_config
        self.herramientas_reg = {}      # name -> {'ruta','clase'}
        self.subagentes_reg = {}
        self.instancias = {}            # cache instancias
        self.chat_memory = ChatSQLMemory()  # único gestor SQLite (puede ser por agente/tenant)

    def registrar_herramienta(self, nombre: str, ruta_modulo: str, clase: str):
        self.herramientas_reg[nombre] = {"ruta": ruta_modulo, "clase": clase}

    def registrar_subagente(self, nombre: str, ruta_modulo: str, clase: str):
        self.subagentes_reg[nombre] = {"ruta": ruta_modulo, "clase": clase}

    def _cargar_herramienta(self, nombre: str):
        meta = self.herramientas_reg[nombre]
        if nombre not in self.instancias:
            modulo = importlib.import_module(meta["ruta"])
            cls = getattr(modulo, meta["clase"])
            self.instancias[nombre] = cls()  # instanciar
        return self.instancias[nombre]

    def _cargar_subagente_como_tool(self, nombre: str):
        meta = self.subagentes_reg[nombre]
        if nombre not in self.instancias:
            modulo = importlib.import_module(meta["ruta"])
            cls = getattr(modulo, meta["clase"])
            inst = cls(factory=self)  # pasar fábrica si necesita crear agentes internos
            self.instancias[nombre] = inst.as_tool()
        return self.instancias[nombre]

    def _cargar_modelo(self, model_id: str):
        cfg = self.model_config[model_id]
        if cfg["provider"] == "ollama":
            return ChatOllama(**cfg["config"])
        raise RuntimeError("Proveedor no soportado en ejemplo")

    def crear_agente(self, model_id: str, herramientas_activas: List[str], prompt_system: str = None):
        llm = self._cargar_modelo(model_id)
        herramientas = []
        for h in herramientas_activas:
            if h in self.herramientas_reg:
                herramientas.append(self._cargar_herramienta(h))
            elif h in self.subagentes_reg:
                herramientas.append(self._cargar_subagente_como_tool(h))
            else:
                raise KeyError(f"Herramienta {h} no registrada")
        agente = crear_agente_base(llm, herramientas, prompt_system)
        # anexamos memoria a agente para uso en code si lo necesita:
        agente.chat_memory = self.chat_memory
        return agente
```

6) cli/main.py — ejemplo de uso y activar/desactivar tools en ejecución (reconstrucción)
```python
# cli/main.py
from core.factory import AgentFactory

def main():
    # configuración de modelos (ejemplo mínimo)
    models = {
        "gemma-ollama": {"provider": "ollama", "config": {"model": "gemma3:4b", "base_url": "http://localhost:11434"}}
    }
    factory = AgentFactory(models)
    # registrar herramientas (rutas Python importables)
    factory.registrar_herramienta("memoria_permanente", "herramientas.memoria.permanente", "MemoriaPermanente")
    factory.registrar_subagente("matematico", "subagentes.matematico", "AgenteMatematico")

    # crear agente inicial con herramientas activas
    agente = factory.crear_agente("gemma-ollama", ["memoria_permanente"])

    # ejemplo simple: invocar agente y guardar chat en SQLite
    user_id = "user_1"
    session_id = "sess_123"
    pregunta = "Guarda mi nota: el sistema usa LangChain."
    # guardar entrada
    agente.chat_memory.add_message(user_id, session_id, "user", pregunta)
    # invocar agente
    respuesta = agente.invoke({"input": pregunta})
    # guardar respuesta
    agente.chat_memory.add_message(user_id, session_id, "assistant", respuesta["output"])
    print("AGENTE RESPONDIÓ:", respuesta["output"])

    # Activar herramienta matemático: RECONSTRUIR agente
    agente = factory.crear_agente("gemma-ollama", ["memoria_permanente", "matematico"])
    r2 = agente.invoke({"input": "2 + 2"})
    print("AGENTE RESPONDIÓ (matematico):", r2["output"])

if __name__ == "__main__":
    main()
```

---

## 4) Cómo guardar metadata solicitada: user / session / fecha / título
- En core/memory_sql.py la tabla chat_history contiene columnas:
  - user_id (cadena)
  - session_id (cadena)
  - session_title (cadena) — puedes generar con un LLM al final de la sesión y actualizar la fila
  - created_at (timestamp)
  - role + content

- Para asignar titles: cuando detectes que la sesión terminó (p. ej. usuario envía `/end`), llama a un LLM con un prompt para generar un título (p. ej. "Resume this conversation in 6 words") y actualiza rows de esa session_id para setear session_title.

---

## 5) Notas de diseño importantes y errores frecuentes (basado en docs/KB)
- LangChain usa SQLAlchemy para conectarse a DB. Para SQLite no hay problemas especiales. Para otras DB (Postgres, MSSQL) hay matices con drivers; si luego migras a Postgres, revisa parámetros de conexión y extensiones.
- Las herramientas se deben registrar por nombre/ruta/clase. Evita importar módulos que definan tablas SQLAlchemy en el import global si vas a crear varias instancias (puede aparecer "Table already defined" en ciertos paquetes). Preferir lazy import en fábrica evita esos problemas.
- En LangChain las herramientas se "bind" al crear el agente. Si quieres cambiar las herramientas de un agente en tiempo de ejecución, la forma más simple y estable es reconstruir el AgentExecutor con la nueva lista.
- Para evitar problemas de concurrencia con SQLite: usa create_engine(..., connect_args={"check_same_thread": False}) y considera un pool o mover a Postgres en producción.

---

## 6) Cómo validar que las URLs de docs funcionan (ya validadas)
Los enlaces que incluí arriba están verificados con check_links.

---

## 7) Próximos pasos sugeridos (rápidos)
- Prueba local: instala dependencias mínimas y ejecuta cli/main.py.
- Añade un pequeño script que genere títulos de sesión usando tu LLM preferido y lo llame al final de cada sesión.
- Si quieres que te proporcione el código completo con tests y un instalador (install.sh), dime y te lo preparo.

---

Relevant docs:

- [Ollama integration](https://docs.langchain.com/oss/python/integrations/providers/ollama)
- [Build a SQL agent](https://docs.langchain.com/oss/python/langchain/sql-agent)
- [SQLite provider](https://docs.langchain.com/oss/python/integrations/providers/sqlite)
- [Long-term memory](https://docs.langchain.com/oss/python/langchain/long-term-memory)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)



