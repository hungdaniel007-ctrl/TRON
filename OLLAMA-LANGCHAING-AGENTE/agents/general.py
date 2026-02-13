import os
import sys
import yaml
import argparse
from dotenv import load_dotenv

# --- Setup sys.path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- LangChain Imports ---
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_ollama.chat_models import ChatOllama
from langchain_deepseek.chat_models import ChatDeepSeek

# --- Configuration Loading ---
def load_model_configs():
    config_path = os.path.join(project_root, "config", "models.yaml")
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR Crítico cargando configuración: {e}")
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
        print(f"ERROR: Modelo '{model_identifier}' no encontrado.")
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
                print("\nERROR: DEEPSEEK_API_KEY no encontrada.")
                return None
            config['api_key'] = deepseek_api_key
            return ChatDeepSeek(**config)
        else:
            print(f"ERROR: Proveedor '{provider}' no soportado.")
            return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

# --- Lógica de Ejecución Síncrona (Robusta para CLI) ---

def run_one_shot(llm, message: str, system_prompt: str = None, stream: bool = False):
    print("--- Modo One-Shot ---")
    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=message))

    print(f"Enviando: '{message}'")
    print("\n--- Respuesta ---")
    
    try:
        if stream:
            # Iteración síncrona directa: Python chequea señales entre chunks
            for chunk in llm.stream(messages):
                print(chunk.content, end="", flush=True)
            print()
        else:
            response = llm.invoke(messages)
            print(response.content)
    except KeyboardInterrupt:
        print("\n\n🛑 Interrumpido por usuario.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def run_chat_mode(llm, initial_model_identifier: str, all_configs: dict, stream: bool = False):
    print("--- Modo Chat Interactivo ---")
    print(f"Streaming: {'✅ Activado' if stream else '❌ Desactivado'}")
    print("Comandos: /model [alias], /stream, /exit")
    print("Tip: Ctrl+C detiene la generación actual inmediatamente.")
    
    current_model_info = next((m for m in all_configs.get('models', []) if m.get('id') == initial_model_identifier or m.get('alias') == initial_model_identifier), None)
    current_model_name = current_model_info['name'] if current_model_info else initial_model_identifier
    print(f"Modelo actual: {current_model_name}")

    history = [] 

    while True:
        try:
            # 1. Entrada de usuario (Manejo de Ctrl+C en espera)
            try:
                user_input = input("\nTú: ").strip()
            except KeyboardInterrupt:
                print("\n(Entrada cancelada. Usa /exit para salir)")
                continue

            if not user_input:
                continue

            # 2. Comandos
            if user_input.lower() == '/exit':
                break
            if user_input.lower() == '/help':
                print("Comandos: /exit, /stream, /model [alias]")
                continue
            if user_input.lower() == '/stream':
                stream = not stream
                print(f"🔄 Streaming: {'Activado' if stream else 'Desactivado'}")
                continue
            
            # Cambio de modelo
            new_model_id = None
            if user_input.lower().startswith('/model '):
                new_model_id = user_input.split(' ', 1)[1].strip()
            elif user_input.startswith('/'):
                potential_alias = user_input.lower()[1:]
                if get_model_id_from_alias(potential_alias, all_configs):
                    new_model_id = potential_alias

            if new_model_id:
                new_llm = load_llm(new_model_id, all_configs)
                if new_llm:
                    llm = new_llm
                    print(f"✅ Modelo cambiado.")
                    history = []
                continue

            # 3. Inferencia
            messages_to_send = history + [HumanMessage(content=user_input)]
            
            print("Agente: ", end="", flush=True)
            full_response = ""
            
            try:
                if stream:
                    # USO DE .stream() SÍNCRONO
                    # flush=True es vital para ver el texto aparecer inmediatamente
                    for chunk in llm.stream(messages_to_send):
                        content = chunk.content
                        print(content, end="", flush=True)
                        full_response += content
                    print() # Salto de línea al terminar
                else:
                    response = llm.invoke(messages_to_send)
                    print(response.content)
                    full_response = response.content
                
                # Solo guardamos si terminó exitosamente
                history.append(HumanMessage(content=user_input))
                history.append(AIMessage(content=full_response))

            except KeyboardInterrupt:
                print("\n\n🛑 Generación detenida por usuario.")
                # Opcional: Guardar respuesta parcial si se desea
                # history.append(HumanMessage(content=user_input))
                # history.append(AIMessage(content=full_response))
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            if "Connection refused" in str(e):
                print("💡 Verifica que 'ollama serve' esté corriendo.")

def main():
    load_dotenv()
    model_configs = load_model_configs()
    default_model_id = model_configs.get('default_model')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-sc', '--headless', action='store_true')
    parser.add_argument('-m', '--message', type=str)
    parser.add_argument('-p', '--system_prompt', type=str, default=None)
    parser.add_argument('--model', type=str, default=default_model_id)
    parser.add_argument('-s', '--stream', action='store_true')

    args = parser.parse_args()
    llm = load_llm(args.model, model_configs)
    
    if not llm: sys.exit(1)

    if args.headless:
        if not args.message: parser.error("Headless requiere -m")
        run_one_shot(llm, args.message, args.system_prompt, stream=args.stream)
    else:
        run_chat_mode(llm, args.model, model_configs, stream=args.stream)

if __name__ == "__main__":
    main()
