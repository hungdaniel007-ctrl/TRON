import os
import sys
import yaml
import argparse
import threading
import queue
import requests
import json
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_ollama import ChatOllama
from langchain_deepseek import ChatDeepSeek

# --- Control de streaming global ---
stop_event = threading.Event()
current_stream_thread = None
streaming_lock = threading.Lock()

def load_model_configs():
    config_path = os.path.join(project_root, "config", "models.yaml")
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR: No se pudo cargar config/models.yaml: {e}")
        sys.exit(1)

def get_model_id_from_alias(alias: str, all_configs: dict) -> str | None:
    for model in all_configs.get('models', []):
        if model.get('alias') == alias:
            return model.get('id')
    return None

def load_llm(model_identifier: str, all_configs: dict):
    model_id = get_model_id_from_alias(model_identifier, all_configs) or model_identifier
    model_info = next((m for m in all_configs.get('models', []) if m.get('id') == model_id), None)

    if not model_info:
        print(f"\nERROR: Modelo '{model_identifier}' no encontrado.")
        return None

    provider = model_info.get('provider')
    config = model_info.get('config', {})

    print(f"\nCargando modelo: {model_info.get('name', model_id)} (Proveedor: {provider})")

    try:
        if provider == 'ollama':
            return ChatOllama(**config)
        elif provider == 'deepseek':
            deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
            if not deepseek_api_key:
                print("\nERROR: DEEPSEEK_API_KEY no encontrada en .env")
                return None
            config['api_key'] = deepseek_api_key
            return ChatDeepSeek(**config)
        else:
            print(f"ERROR: Proveedor '{provider}' no soportado.")
            return None
    except Exception as e:
        print(f"ERROR al cargar modelo: {e}")
        return None

def stream_with_cancel(llm, messages, output_queue, stop_event):
    """
    Función que corre en thread separado. Si stop_event se setea,
    simplemente dejamos de procesar chunks y salimos.
    """
    try:
        # Para Ollama, usamos la API nativa con requests para poder cerrar la conexión
        if isinstance(llm, ChatOllama):
            # Extraer config del modelo
            model_name = llm.model
            base_url = getattr(llm, 'base_url', "http://localhost:11434")
            
            # Convertir mensajes LangChain a formato Ollama
            ollama_messages = []
            for msg in messages:
                if isinstance(msg, SystemMessage):
                    ollama_messages.append({"role": "system", "content": msg.content})
                elif isinstance(msg, HumanMessage):
                    ollama_messages.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    ollama_messages.append({"role": "assistant", "content": msg.content})
            
            # Hacer request streaming con requests
            url = f"{base_url}/api/chat"
            payload = {
                "model": model_name,
                "messages": ollama_messages,
                "stream": True,
                "options": {
                    "temperature": getattr(llm, 'temperature', 0.7),
                }
            }
            
            response = requests.post(url, json=payload, stream=True)
            
            full_content = ""
            for line in response.iter_lines():
                if stop_event.is_set():
                    response.close()  # ¡Cerrar conexión HTTP real!
                    output_queue.put(("cancelled", full_content))
                    return
                
                if line:
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            chunk_content = data["message"]["content"]
                            full_content += chunk_content
                            output_queue.put(("chunk", chunk_content))
                        
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
            
            output_queue.put(("done", full_content))
            
        else:
            # Para otros modelos (DeepSeek, OpenAI, etc.), usar LangChain nativo
            # pero con chequeo frecuente de stop_event
            full_content = ""
            for chunk in llm.stream(messages):
                if stop_event.is_set():
                    output_queue.put(("cancelled", full_content))
                    return
                content = chunk.content or ""
                full_content += content
                output_queue.put(("chunk", content))
            
            output_queue.put(("done", full_content))
            
    except Exception as e:
        output_queue.put(("error", str(e)))

def run_one_shot(llm, message: str, system_prompt: str = None, stream: bool = False):
    print("--- Modo One-Shot ---")
    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=message))

    print(f"Enviando: '{message}'")
    
    if not stream:
        try:
            response = llm.invoke(messages)
            print(f"\n--- Respuesta ---\n{response.content}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        return

    # Streaming con cancelación
    print("\n--- Respuesta (streaming) ---")
    print("Agente: ", end="", flush=True)
    
    global stop_event, current_stream_thread
    stop_event.clear()
    output_queue = queue.Queue()
    
    # Iniciar thread de streaming
    thread = threading.Thread(target=stream_with_cancel, args=(llm, messages, output_queue, stop_event))
    thread.start()
    current_stream_thread = thread
    
    full_content = ""
    try:
        while thread.is_alive() or not output_queue.empty():
            try:
                status, data = output_queue.get(timeout=0.1)
                if status == "chunk":
                    print(data, end="", flush=True)
                    full_content += data
                elif status in ("done", "cancelled"):
                    if status == "cancelled":
                        print("\n\n🛑 Generación cancelada.")
                    break
                elif status == "error":
                    print(f"\n❌ Error: {data}")
                    break
            except queue.Empty:
                continue
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo...")
        stop_event.set()
        thread.join(timeout=2.0)
    
    print()

def run_chat_mode(llm, initial_model_identifier: str, all_configs: dict, stream: bool = False):
    print("--- Modo Chat Interactivo ---")
    print(f"Streaming: {'✅ Activado' if stream else '❌ Desactivado'}")
    print("🛑 Ctrl+C = Cancela generación | /model [alias] | /stream | /exit")
    
    current_model_identifier = initial_model_identifier
    history = []
    
    while True:
        try:
            user_input = input("\nTú: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n¡Hasta luego!")
            break

        if not user_input:
            continue

        # Comandos
        if user_input.lower() == '/exit':
            print("¡Hasta luego!")
            break
            
        if user_input.lower() == '/help':
            print("\nComandos disponibles:")
            print("  /exit              - Salir del chat")
            print("  /model [alias/id]  - Cambiar de modelo")
            print("  /stream            - Toggle streaming on/off")
            print("  /clear             - Limpiar historial")
            print("  Ctrl+C             - Cancelar generación actual")
            continue
            
        if user_input.lower() == '/stream':
            stream = not stream
            print(f"Streaming: {'✅ Activado' if stream else '❌ Desactivado'}")
            continue
            
        if user_input.lower() == '/clear':
            history = []
            print("Historial limpiado.")
            continue
            
        if user_input.lower().startswith('/model '):
            parts = user_input.split(' ', 1)
            if len(parts) == 2:
                new_model_id = parts[1].strip()
                new_llm = load_llm(new_model_id, all_configs)
                if new_llm:
                    llm = new_llm
                    current_model_identifier = new_model_id
                    history = []  # Reset historial al cambiar modelo
                    print(f"✅ Modelo cambiado a: {new_model_id}")
                else:
                    print(f"❌ No se pudo cargar: {new_model_id}")
            continue

        # Preparar mensajes
        messages_for_llm = list(history) + [HumanMessage(content=user_input)]
        
        if not stream:
            # Modo no-streaming (invoke)
            print("Agente: ", end="", flush=True)
            try:
                response = llm.invoke(messages_for_llm)
                print(response.content)
                history.append(HumanMessage(content=user_input))
                history.append(AIMessage(content=response.content))
            except Exception as e:
                print(f"\n❌ Error: {e}")
            continue

        # === STREAMING CON CANCELACIÓN REAL ===
        print("Agente: ", end="", flush=True)
        
        global stop_event, current_stream_thread
        stop_event.clear()
        output_queue = queue.Queue()
        
        # Iniciar thread de streaming
        thread = threading.Thread(target=stream_with_cancel, args=(llm, messages_for_llm, output_queue, stop_event))
        thread.start()
        current_stream_thread = thread
        
        full_content = ""
        cancelled = False
        
        try:
            while thread.is_alive() or not output_queue.empty():
                try:
                    status, data = output_queue.get(timeout=0.1)
                    
                    if status == "chunk":
                        print(data, end="", flush=True)
                        full_content += data
                    elif status == "done":
                        break
                    elif status == "cancelled":
                        cancelled = True
                        print("\n🛑 Cancelado.")
                        break
                    elif status == "error":
                        print(f"\n❌ Error: {data}")
                        break
                        
                except queue.Empty:
                    continue
                    
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo generación...")
            stop_event.set()
            thread.join(timeout=2.0)
            cancelled = True
        
        # Solo guardar en historial si no fue cancelado
        if not cancelled and full_content.strip():
            history.append(HumanMessage(content=user_input))
            history.append(AIMessage(content=full_content))
            # Limitar historial a últimos 20 mensajes para no saturar contexto
            if len(history) > 40:
                history = history[-40:]
        
        print()  # Nueva línea después de respuesta

def main():
    load_dotenv()
    model_configs = load_model_configs()
    default_model_id = model_configs.get('default_model')

    parser = argparse.ArgumentParser(description="Agente CLI Multi-Modelo con Streaming Real")
    parser.add_argument('-sc', '--headless', action='store_true', help="Modo one-shot (sin interacción)")
    parser.add_argument('-m', '--message', type=str, help="Mensaje para modo one-shot")
    parser.add_argument('-p', '--system-prompt', type=str, default=None, help="System prompt inicial")
    parser.add_argument('--model', type=str, default=default_model_id, help="ID o alias del modelo")
    parser.add_argument('-s', '--stream', action='store_true', help="Activar streaming")

    args = parser.parse_args()

    if not args.model:
        print("ERROR: No se especificó modelo y no hay default en config.")
        sys.exit(1)

    llm = load_llm(args.model, model_configs)
    if not llm:
        sys.exit(1)

    if args.headless:
        if not args.message:
            parser.error("Modo headless requiere -m 'mensaje'")
        run_one_shot(llm, args.message, args.system_prompt, args.stream)
    else:
        run_chat_mode(llm, args.model, model_configs, args.stream)

if __name__ == "__main__":
    main()