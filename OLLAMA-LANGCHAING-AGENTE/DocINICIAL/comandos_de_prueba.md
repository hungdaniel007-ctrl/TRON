# Comandos de Prueba del Sistema de Agentes Modulares
Fecha: domingo, 15 de febrero de 2026

## Modo Interactivo (ejecutar desde la raíz del proyecto):

```bash
# Iniciar con agente por defecto (tron-ceo), pide titulo
./run.py
# Iniciar con agente por defecto (tron-ceo) y streaming activado, pide titulo
./run.py --stream
# Iniciar con agente Gemma Analyst, pide titulo
./run.py --agent gema-analyst
# Iniciar con agente Gemma Analyst y streaming activado, pide titulo
./run.py --agent gema-analyst --stream
```

## Comandos interactivos dentro del chat (tras ejecutar ./run.py):

```bash
# Para cambiar el modelo a Gemma (Ollama)
/model gema
# Para cambiar el modelo a DeepSeek (API)
/model deepseek
# Para activar/desactivar streaming
/stream
# Para salir del chat
/exit
# Para mostrar ayuda
/help
```

## Modo Headless (ejecutar desde la raíz del proyecto):

```bash
# Agente por defecto (tron-ceo), mensaje simple
./run.py --headless -m "Explica la importancia de la modularidad en Python en una frase concisa."
# Agente por defecto (tron-ceo), mensaje simple con streaming
./run.py --headless -m "Detalla el ciclo de vida de un agente LLM desde la percepcion hasta la accion." --stream
# Agente Gemma Analyst, mensaje simple
./run.py --headless -m "Que es la clorofila y por que es verde?" --agent gema-analyst
# Agente Gemma Analyst, mensaje simple con streaming
./run.py --headless -m "Describe la fotosintesis paso a paso." --agent gema-analyst --stream
# Agente por defecto (tron-ceo), mensaje con override de system prompt
./run.py --headless -m "Saludame como un robot muy antiguo y defectuoso." -ps "Eres un robot muy antiguo y defectuoso. Responde siempre con fallos en la voz y la logica."
# Agente Gemma Analyst, mensaje con override de system prompt
./run.py --headless -m "Resume la arquitectura de microservicios en una frase." --agent gema-analyst -ps "Eres un resumidor experto y conciso."
# Agente por defecto (tron-ceo), mensaje con session persistente
./run.py --headless -m "Recordatorio: mi color favorito es el azul." --session "Mis recordatorios"
# Agente Gemma Analyst, mensaje con override de system prompt y session persistente
./run.py --headless -m "Por que el cielo es azul?" --agent gema-analyst -ps "Eres un cientifico atmosferico." --session "Ciencia Atmosferica"







  5 **Modo Interactivo (ejecutar desde la raíz del proyecto):**
  Iniciar con agente por defecto (tron-ceo), pide título
  ./run.py

  Iniciar con agente por defecto (tron-ceo) y streaming activado, pide título
  ./run.py --stream

  Iniciar con agente 'Gemma Analyst', pide título
  ./run.py --agent gema-analyst

  Iniciar con agente 'Gemma Analyst' y streaming activado, pide título
  ./run.py --agent gema-analyst --stream
   1
   2 **Comandos interactivos dentro del chat (tras ejecutar ./run.py):**
  Para cambiar el modelo a Gemma (Ollama)
  /model gema

  Para cambiar el modelo a DeepSeek (API)
  /model deepseek

  Para activar/desactivar streaming
  /stream

  Para salir del chat
  /exit

  Para mostrar ayuda
  /help
   1
   2 **Modo Headless (ejecutar desde la raíz del proyecto):**
  Agente por defecto (tron-ceo), mensaje simple
  ./run.py --headless -m "Explica la importancia de la modularidad en Python en una frase concisa."

  Agente por defecto (tron-ceo), mensaje simple con streaming
  ./run.py --headless -m "Detalla el ciclo de vida de un agente LLM desde la percepción hasta la acción." --stream

  Agente 'Gemma Analyst', mensaje simple
  ./run.py --headless -m "Que es la clorofila y por que es verde?" --agent gema-analyst

  Agente 'Gemma Analyst', mensaje simple con streaming
  ./run.py --headless -m "Describe la fotosintesis paso a paso." --agent gema-analyst --stream

  Agente por defecto (tron-ceo), mensaje con override de system prompt
  ./run.py --headless -m "Saludame como un robot muy antiguo y defectuoso." -ps "Eres un robot muy antiguo y defectuoso. Responde siempre con fallos en la
  voz y la logica."

  Agente 'Gemma Analyst', mensaje con override de system prompt
  ./run.py --headless -m "Resume la arquitectura de microservicios en una frase." --agent gema-analyst -ps "Eres un resumidor experto y conciso."

  Agente por defecto (tron-ceo), mensaje con session persistente
  ./run.py --headless -m "Recordatorio: mi color favorito es el azul." --session "Mis recordatorios"

  Agente 'Gemma Analyst', mensaje con override de system prompt y session persistente
  ./run.py --headless -m "Por que el cielo es azul?" --agent gema-analyst -ps "Eres un cientifico atmosferico." --session "Ciencia Atmosferica"
  `'
   



 **Modo Interactivo (ejecutar desde la raíz del proyecto):**
  Iniciar con agente por defecto (tron-ceo), pide titulo
  ./run.py

  Iniciar con agente por defecto (tron-ceo) y streaming activado, pide titulo
  ./run.py --stream

  Iniciar con agente 'Gemma Analyst', pide titulo
  ./run.py --agent gema-analyst

  Iniciar con agente 'Gemma Analyst' y streaming activado, pide titulo
  ./run.py --agent gema-analyst --stream
   1
   2 **Comandos interactivos dentro del chat (tras ejecutar ./run.py):**
  Para cambiar el modelo a Gemma (Ollama)
  /model gema

  Para cambiar el modelo a DeepSeek (API)
  /model deepseek

  Para activar/desactivar streaming
  /stream

  Para salir del chat
  /exit

  Para mostrar ayuda
  /help
   1
   2 **Modo Headless (ejecutar desde la raíz del proyecto):**
  Agente por defecto (tron-ceo), mensaje simple
  ./run.py --headless -m "Explica la importancia de la modularidad en Python en una frase concisa."

  Agente por defecto (tron-ceo), mensaje simple con streaming
  ./run.py --headless -m "Detalla el ciclo de vida de un agente LLM desde la percepcion hasta la accion." --stream

  Agente 'Gemma Analyst', mensaje simple
  ./run.py --headless -m "Que es la clorofila y por que es verde?" --agent gema-analyst

  Agente 'Gemma Analyst', mensaje simple con streaming
  ./run.py --headless -m "Describe la fotosintesis paso a paso." --agent gema-analyst --stream

  Agente por defecto (tron-ceo), mensaje con override de system prompt
  ./run.py --headless -m "Saludame como un robot muy antiguo y defectuoso." -ps "Eres un robot muy antiguo y defectuoso. Responde siempre con fallos en la
  voz y la logica."

  Agente 'Gemma Analyst', mensaje con override de system prompt
  ./run.py --headless -m "Resume la arquitectura de microservicios en una frase." --agent gema-analyst -ps "Eres un resumidor experto y conciso."

  Agente por defecto (tron-ceo), mensaje con session persistente
  ./run.py --headless -m "Recordatorio: mi color favorito es el azul." --session "Mis recordatorios"

  Agente 'Gemma Analyst', mensaje con override de system prompt y session persistente
  ./run.py --headless -m "Por que el cielo es azul?" --agent gema-analyst -ps "Eres un cientifico atmosferico." --session "Ciencia Atmosferica"
  `'
   1
   2 He ajustado el prompt para eliminar las comillas simples conflictivas dentro de los bloques de código bash/python que `qwen` debe generar como Markdown,
     reemplazándolas con comillas dobles donde el contexto lo permite o eliminándolas si no son críticas para la instrucción de `qwen`.
   3
   4 Procedo a ejecutar este comando `qwen`.

✦ El prompt que generé para qwen falló nuevamente. El error bash: -c: línea 67: EOF inesperado mientras se buscaba un «» coincidente persiste. Esto indica
  que el problema no eran solo las comillas simples, sino los *backticks* (`  `) de los bloques de código Markdown anidados dentro de la cadena de comillas
  simples externa. Bash interpreta el primer backtick como el inicio de una sustitución de comando, y no encuentra su cierre hasta el final del archivo.

  Mi error: La complejidad de escapar backticks dentro de una cadena de comillas simples o dobles, que a su vez contiene backticks para bloques de código, es
  extremadamente alta y propensa a errores.

  Plan de Corrección Definitivo para este tipo de contenido (Archivos Markdown con código):

   1. Evitar la anidación directa de Markdown: No intentaré pasar el contenido Markdown directamente como una cadena literal que qwen deba escribir.
   2. Usar una estrategia de "plantilla" o generación de código para `qwen`: Le diré a qwen que genere el archivo Markdown, incluyendo los bloques de código,
      pero le daré las instrucciones de forma más abstracta.

  Voy a reintentar la creación del archivo de comandos de prueba con esta nueva estrategia.

  Prompt Bash-Safe para Qwen (Archivo de Comandos de Prueba - INTENTO 3 - Generación de Contenido Abstracta)

    1 qwen --yolo 'Create a new Markdown file at /home/daniel/tron/programas/TRON/OLLAMA-LANGCHAING-AGENTE/DocINICIAL/comandos_de_prueba.md.
    2 The title of the document should be "Comandos de Prueba del Sistema de Agentes Modulares" with today''s date.
    3
    4 The document should then contain two main sections:
    5 1.  "Modo Interactivo (ejecutar desde la raíz del proyecto):"
    6     Below this, list the following commands in a bash code block:
    7     # Iniciar con agente por defecto (tron-ceo), pide titulo
    8     ./run.py
    9     # Iniciar con agente por defecto (tron-ceo) y streaming activado, pide titulo
   10     ./run.py --stream
   11     # Iniciar con agente 'Gemma Analyst', pide titulo
   12     ./run.py --agent gema-analyst
   13     # Iniciar con agente 'Gemma Analyst' y streaming activado, pide titulo
   14     ./run.py --agent gema-analyst --stream
   15
   16 2.  "Comandos interactivos dentro del chat (tras ejecutar ./run.py):"
   17     Below this, list the following commands in a bash code block:
   18     # Para cambiar el modelo a Gemma (Ollama)
   19     /model gema
   20     # Para cambiar el modelo a DeepSeek (API)
   21     /model deepseek
   22     # Para activar/desactivar streaming
   23     /stream
   24     # Para salir del chat
   25     /exit
   26     # Para mostrar ayuda
   27     /help
   28
   29 3.  "Modo Headless (ejecutar desde la raíz del proyecto):"
   30     Below this, list the following commands in a bash code block:
   31     # Agente por defecto (tron-ceo), mensaje simple
   32     ./run.py --headless -m "Explica la importancia de la modularidad en Python en una frase concisa."
   33     # Agente por defecto (tron-ceo), mensaje simple con streaming
   34     ./run.py --headless -m "Detalla el ciclo de vida de un agente LLM desde la percepcion hasta la accion." --stream
   35     # Agente 'Gemma Analyst', mensaje simple
   36     ./run.py --headless -m "Que es la clorofila y por que es verde?" --agent gema-analyst
   37     # Agente 'Gemma Analyst', mensaje simple con streaming
   38     ./run.py --headless -m "Describe la fotosintesis paso a paso." --agent gema-analyst --stream
   39     # Agente por defecto (tron-ceo), mensaje con override de system prompt
   40     ./run.py --headless -m "Saludame como un robot muy antiguo y defectuoso." -ps "Eres un robot muy antiguo y defectuoso. Responde siempre con fallos 
      la voz y la logica."
   41     # Agente 'Gemma Analyst', mensaje con override de system prompt
   42     ./run.py --headless -m "Resume la arquitectura de microservicios en una frase." --agent gema-analyst -ps "Eres un resumidor experto y conciso."
   43     # Agente por defecto (tron-ceo), mensaje con session persistente
   44     ./run.py --headless -m "Recordatorio: mi color favorito es el azul." --session "Mis recordatorios"
   45     # Agente 'Gemma Analyst', mensaje con override de system prompt y session persistente
   46     ./run.py --headless -m "Por que el cielo es azul?" --agent gema-analyst -ps "Eres un cientifico atmosferico." --session "Ciencia Atmosferica"
   47
   48 Ensure the Markdown formatting for code blocks is correct. Use the 'write_file' tool.
```
