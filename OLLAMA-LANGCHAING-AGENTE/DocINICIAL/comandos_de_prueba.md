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
```