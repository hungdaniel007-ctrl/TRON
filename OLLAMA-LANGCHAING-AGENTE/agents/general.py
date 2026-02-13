# OLLAMA-LANGCHAING-AGENTE/agents/general.py
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
def run_one_shot(llm, message: str, system_prompt: str = None):
    """
    Handles the headless, one-shot execution mode.
    """
    print("--- Modo One-Shot ---")
    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=message))

    print(f"Enviando mensaje al modelo: '{message}'")
    try:
        response = llm.invoke(messages)
        print("\n--- Respuesta del Modelo ---")
        print(response.content)
    except Exception as e:
        print(f"\nERROR al invocar el modelo: {e}")

def run_chat_mode(llm, initial_model_identifier: str, all_configs: dict):
    """
    Handles the interactive chat loop.
    """
    print("--- Modo Chat Interactivo ---")
    print("Comandos disponibles: /model [id_del_modelo|alias], /help, /exit")
    
    current_model_info = next((m for m in all_configs.get('models', []) if m.get('id') == initial_model_identifier or m.get('alias') == initial_model_identifier), None)
    current_model_name = current_model_info['name'] if current_model_info else initial_model_identifier
    print(f"Modelo actual: {current_model_name}")

    history = [] # For simplicity, conversation history is not maintained between model switches in this basic version.

    while True:
        user_input = input("\nTú: ")

        if user_input.lower() == '/exit':
            print("Saliendo del chat. ¡Hasta luego!")
            break

        if user_input.lower() == '/help':
            print("\nComandos:")
            print("  /exit          - Salir del chat.")
            print("  /model [id|alias] - Cambiar al modelo especificado (ej: /model deepseek-chat o /model deepseek).")
            print("  /model         - Mostrar modelos disponibles.")
            print("  /help          - Mostrar este mensaje de ayuda.")
            print("\nModelos disponibles:")
            for model_cfg in all_configs.get('models', []):
                alias_info = f" (alias: /{model_cfg['alias']})" if model_cfg.get('alias') else ""
                print(f"  - {model_cfg['id']} ({model_cfg['name']}){alias_info}")
            continue

        if user_input.lower() == '/model':
            print("\nModelos disponibles:")
            for model_cfg in all_configs.get('models', []):
                alias_info = f" (alias: /{model_cfg['alias']})" if model_cfg.get('alias') else ""
                print(f"  - {model_cfg['id']} ({model_cfg['name']}){alias_info}")
            print("\nPara cambiar, usa: /model [id_del_modelo|alias]")
            continue

        if user_input.lower().startswith('/model '):
            new_model_identifier = user_input.split(' ', 1)[1].strip()
            new_llm = load_llm(new_model_identifier, all_configs)
            if new_llm:
                llm = new_llm
                current_model_info = next((m for m in all_configs.get('models', []) if m.get('id') == new_model_identifier or m.get('alias') == new_model_identifier), None)
                current_model_name = current_model_info['name'] if current_model_info else new_model_identifier
                print(f"Modelo cambiado a: {current_model_name}")
                history = [] # Reset history on model change
            continue
        
        # Handle alias commands directly, e.g., "/gema"
        if user_input.lower().startswith('/'):
            potential_alias = user_input.lower()[1:] # Remove leading '/'
            model_id_from_alias = get_model_id_from_alias(potential_alias, all_configs)
            if model_id_from_alias:
                new_llm = load_llm(model_id_from_alias, all_configs)
                if new_llm:
                    llm = new_llm
                    current_model_info = next((m for m in all_configs.get('models', []) if m.get('id') == model_id_from_alias), None)
                    current_model_name = current_model_info['name'] if current_model_info else model_id_from_alias
                    print(f"Modelo cambiado a: {current_model_name}")
                    history = [] # Reset history on model change
                continue


        # Regular chat message
        messages_to_send = history + [HumanMessage(content=user_input)]
        try:
            response = llm.invoke(messages_to_send)
            print(f"Agente: {response.content}")
            history.append(HumanMessage(content=user_input)) # Add user message to history
            history.append(response) # Add AI response to history
        except Exception as e:
            print(f"\nERROR al invocar el modelo: {e}")
            print("Asegúrate de que el modelo esté disponible y configurado correctamente (ej. clave API).")


def main():
    """
    Main entry point, parses CLI arguments and starts the correct mode.
    """
    # Load .env file for API keys
    load_dotenv()

    # Load model configurations
    model_configs = load_model_configs()
    default_model_id = model_configs.get('default_model')
    if not default_model_id:
        print("ERROR: 'default_model' no está definido en config/models.yaml")
        sys.exit(1)

    # Setup CLI argument parser
    parser = argparse.ArgumentParser(description="Agente de chat con modelos dinámicos.")
    parser.add_argument(
        '-sc', '--headless',
        action='store_true',
        help="Ejecutar en modo 'sin cabeza' (one-shot). Requiere -m."
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
        help="(Opcional) Prompt de sistema para el modo one-shot."
    )
    parser.add_argument(
        '--model',
        type=str,
        default=default_model_id,
        help=f"ID o alias del modelo a usar. Por defecto: {default_model_id}"
    )

    args = parser.parse_args()

    # Load the selected or default language model
    llm = load_llm(args.model, model_configs)
    if not llm:
        sys.exit(1) # Exit if model loading failed

    if args.headless:
        if not args.message:
            parser.error("El modo headless (-sc) requiere un mensaje (-m).")
        run_one_shot(llm, args.message, args.system_prompt)
    else:
        run_chat_mode(llm, args.model, model_configs)

if __name__ == "__main__":
    main()