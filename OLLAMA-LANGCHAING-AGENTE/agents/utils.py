# OLLAMA-LANGCHAING-AGENTE/agents/utils.py
"""
Módulo de Utilidades:
- Contiene funciones puras y reutilizables para la carga de configuraciones y modelos.
- No contiene lógica de ejecución ni de estado.
"""
import os
import sys
import yaml
from dotenv import load_dotenv

# --- LangChain Imports ---
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_ollama.chat_models import ChatOllama
from langchain_deepseek.chat_models import ChatDeepSeek

# --- Configuration Loading ---
def load_model_configs():
    """
    Carga las configuraciones de todos los modelos desde config/models.yaml.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(project_root, "config", "models.yaml")
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ Error Crítico: No se encontró el archivo de configuración de modelos en {config_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error Crítico cargando configuración de modelos: {e}")
        sys.exit(1)

def get_model_id_from_alias(alias: str, all_configs: dict) -> str | None:
    """
    Busca el ID real de un modelo a partir de su alias.
    """
    for model in all_configs.get('models', []):
        if model.get('alias') == alias:
            return model.get('id')
    return None

def load_llm(model_identifier: str, all_configs: dict):
    """
    Carga una instancia de un modelo de lenguaje (LLM) de LangChain.
    - Usa un identificador (ID o alias) para encontrar la configuración del modelo.
    - Soporta diferentes proveedores (Ollama, DeepSeek).
    - Carga las claves de API desde el entorno si es necesario.
    """
    model_id = get_model_id_from_alias(model_identifier, all_configs) or model_identifier
    model_info = next((m for m in all_configs.get('models', []) if m.get('id') == model_id), None)

    if not model_info:
        print(f"❌ Error: Modelo '{model_identifier}' no encontrado en config/models.yaml.")
        return None

    provider = model_info.get('provider')
    config = model_info.get('config', {})

    print(f"🧠  Cargando cerebro: {model_info.get('name', model_id)} (Proveedor: {provider})")

    try:
        if provider == 'ollama':
            return ChatOllama(**config)
        elif provider == 'deepseek':
            # La variable de entorno DEEPSEEK_API_KEY debe estar disponible
            deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
            if not deepseek_api_key:
                print("\n❌ Error: DEEPSEEK_API_KEY no fue encontrada en el entorno.")
                print("   Por favor, crea un archivo .env y añade: DEEPSEEK_API_KEY='TU_CLAVE'")
                return None
            config['api_key'] = deepseek_api_key
            return ChatDeepSeek(**config)
        else:
            print(f"❌ Error: Proveedor de modelo '{provider}' no es soportado por este sistema.")
            return None
    except Exception as e:
        print(f"❌ Error inesperado al inicializar el modelo '{model_id}': {e}")
        return None
