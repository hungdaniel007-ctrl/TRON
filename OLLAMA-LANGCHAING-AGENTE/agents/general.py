import os
import sys
import yaml
import argparse
from dotenv import load_dotenv

# --- Setup sys.path ---
# This allows the script to be run from the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- LangChain Imports ---
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_ollama.chat_models import ChatOllama
from langchain_deepseek.chat_models import ChatDeepSeek

# --- Configuration Loading ---
def load_model_configs():
    """Loads model configurations from config/models.yaml"""
    config_path = os.path.join(project_root, "config", "models.yaml")
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"ERROR: Configuration file not found at {config_path}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to load or parse {config_path}: {e}")
        sys.exit(1)

def get_model_id_from_alias(alias: str, all_configs: dict) -> str | None:
    """Finds a model ID given its alias."""
    for model in all_configs.get('models', []):
        if model.get('alias') == alias:
            return model.get('id')
    return None

def load_llm(model_identifier: str, all_configs: dict):
    """
    Loads and returns a LangChain ChatModel instance based on the model_identifier (ID or alias).
    """
    model_id = get_model_id_from_alias(model_identifier, all_configs) or model_identifier
    model_info = next((m for m in all_configs.get('models', []) if m.get('id') == model_id), None)

    if not model_info:
        print(f"ERROR: Modelo '{model_identifier}' (ID o alias) no encontrado en config/models.yaml")
        return None

    provider = model_info.get('provider')
    config = model_info.get('config', {})

    print(f"\nCargando modelo: {model_info.get('name', model_id)} (Proveedor: {provider})")

    try:
        if provider == 'ollama':
            return ChatOllama(**config)
        elif provider == 'deepseek':
            # Load API key from environment for DeepSeek
            deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
            if not deepseek_api_key:
                print("\nERROR: DEEPSEEK_API_KEY no encontrada en el entorno.")
                print("Por favor, crea un archivo .env en la raíz del proyecto y añade: DEEPSEEK_API_KEY='TU_CLAVE'")
                return None
            config['api_key'] = deepseek_api_key
            return ChatDeepSeek(**config)
        else:
            print(f"ERROR: Proveedor de modelo '{provider}' no es soportado.")
            return None
    except Exception as e:
        print(f"ERROR: No se pudo inicializar el modelo '{model_id}'. Detalles: {e}")
        return None

# --- Main Application Logic ---
def run_one_shot(llm, message: str, system_prompt: str = None, stream: bool = False):
    """
    Handles the headless, one-shot execution mode with optional streaming.
    """
    print("--- Modo One-Shot ---")
    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=message))

    print(f"Enviando mensaje al modelo: '{message}'")
    print("\n--- Respuesta del Modelo ---")
    
    try:
        if stream:
            # Modo Streaming
            for chunk in llm.stream(messages):
                print(chunk.content, end="", flush=True)
            print() # Salto de línea al final
        else:
            # Modo Bloque (Invoke)
            response = llm.invoke(messages)
            print(response.content)
            
    except Exception as e:
        print(f"\nERROR al invocar el modelo: {e}")

def run_chat_mode(llm, initial_model_identifier: str, all_configs: dict, stream: bool = False):
    """
    Handles the interactive chat loop with streaming support.
    """
    print("--- Modo Chat Interactivo ---")
    print(f"Modo Streaming: {'Activado' if stream else 'Desactivado'}")
    print("Comandos disponibles: /model [id|alias], /stream, /help, /exit")
    
    current_model_info = next((m for m in all_configs.get('models', []) if m.get('id') == initial_model_identifier or m.get('alias') == initial_model_identifier), None)
    current_model_name = current_model_info['name'] if current_model_info else initial_model_identifier
    print(f"Modelo actual: {current_model_name}")

    history = [] 

    while True:
        try:
            user_input = input("\nTú: ")
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break

        if not user_input.strip():
            continue

        # --- Comandos ---
        if user_input.lower() == '/exit':
            print("Saliendo del chat. ¡Hasta luego!")
            break

        if user_input.lower() == '/help':
            print("\nComandos:")
            print("  /exit          - Salir del chat.")
            print("  /stream        - Activar/Desactivar streaming.")
            print("  /model [alias] - Cambiar modelo (ej: /model deepseek).")
            print("  /model         - Listar modelos.")
            continue
        
        if user_input.lower() == '/stream':
            stream = not stream
            print(f"🔄 Modo Streaming: {'Activado' if stream else 'Desactivado'}")
            continue

        if user_input.lower() == '/model':
            print("\nModelos disponibles:")
            for model_cfg in all_configs.get('models', []):
                alias_info = f" (alias: /{model_cfg['alias']})" if model_cfg.get('alias') else ""
                print(f"  - {model_cfg['id']} ({model_cfg['name']}){alias_info}")
            continue

        # Cambio de modelo (Soporta "/model alias" y "/alias")
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
                current_model_info = next((m for m in all_configs.get('models', []) if m.get('id') == new_model_id or m.get('alias') == new_model_id), None)
                current_model_name = current_model_info['name'] if current_model_info else new_model_id
                print(f"✅ Modelo cambiado a: {current_model_name}")
                history = [] # Reset history on model change
            continue

        # --- Inferencia ---
        messages_to_send = history + [HumanMessage(content=user_input)]
        
        try:
            print("Agente: ", end="", flush=True)
            
            if stream:
                full_response = ""
                # Usamos llm.stream() para recibir tokens uno a uno
                for chunk in llm.stream(messages_to_send):
                    content = chunk.content
                    print(content, end="", flush=True)
                    full_response += content
                print() # Salto de línea final
                
                # Guardamos en historial
                history.append(HumanMessage(content=user_input))
                history.append(AIMessage(content=full_response))
            else:
                # Modo clásico sin streaming
                response = llm.invoke(messages_to_send)
                print(response.content)
                
                # Guardamos en historial
                history.append(HumanMessage(content=user_input))
                history.append(response)
                
        except Exception as e:
            print(f"\n❌ ERROR al invocar el modelo: {e}")
            if "Connection refused" in str(e):
                print("💡 PISTA: Verifica que Ollama esté corriendo ('ollama serve').")


def main():
    """
    Main entry point, parses CLI arguments and starts the correct mode.
    """
    load_dotenv()

    model_configs = load_model_configs()
    default_model_id = model_configs.get('default_model')
    if not default_model_id:
        print("ERROR: 'default_model' no está definido en config/models.yaml")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Agente de chat con modelos dinámicos.")
    parser.add_argument(
        '-sc', '--headless',
        action='store_true',
        help="Ejecutar en modo 'sin cabeza' (one-shot)."
    )
    parser.add_argument(
        '-m', '--message',
        type=str,
        help="Mensaje para enviar al modelo en modo one-shot."
    )
    parser.add_argument(
        '-p', '--system_prompt',
        type=str,
        default=None,
        help="(Opcional) Prompt de sistema."
    )
    parser.add_argument(
        '--model',
        type=str,
        default=default_model_id,
        help=f"ID o alias del modelo. Default: {default_model_id}"
    )
    # Nuevo argumento para streaming
    parser.add_argument(
        '-s', '--stream',
        action='store_true',
        help="Activar respuesta en tiempo real (streaming)."
    )

    args = parser.parse_args()

    llm = load_llm(args.model, model_configs)
    if not llm:
        sys.exit(1)

    if args.headless:
        if not args.message:
            parser.error("El modo headless (-sc) requiere un mensaje (-m).")
        run_one_shot(llm, args.message, args.system_prompt, stream=args.stream)
    else:
        run_chat_mode(llm, args.model, model_configs, stream=args.stream)

if __name__ == "__main__":
    main()
