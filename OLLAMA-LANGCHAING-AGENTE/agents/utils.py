# OLLAMA-LANGCHAING-AGENTE/agents/utils.py
# --- HISTORIAL DE ERRORES Y SOLUCIONES ---
# 1.  TypeError: Completions.create() got an unexpected keyword argument 'modelo_base_id'.
#     - Causa: Se pasaban claves de configuración internas del framework ('modelo_base_id', 'temperatura')
#       directamente a los constructores de LangChain (ChatDeepSeek, ChatOllama), que no las reconocen.
#     - Solución: En `load_llm`, "sanitizar" el diccionario `merged_config` antes de pasarlo,
#       eliminando claves no estándar y mapeando nombres (ej. 'temperatura' -> 'temperature').
#
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

def load_llm(model_identifier: str, all_configs: dict, agent_cerebro_config: dict = None):
    """
    Carga una instancia de un modelo de lenguaje (LLM) de LangChain.
    - Usa un identificador (ID o alias) para encontrar la configuración del modelo.
    - Acepta una configuración de agente para sobreescribir parámetros base (ej. temperatura).
    - Soporta diferentes proveedores (Ollama, DeepSeek).
    """
    # Busca el ID real, ya sea directamente o a través de un alias
    model_id = get_model_id_from_alias(model_identifier, all_configs) or model_identifier
    model_info = next((m for m in all_configs.get('models', []) if m.get('id') == model_id), None)

    if not model_info:
        print(f"❌ Error: Configuración de modelo con ID '{model_identifier}' no encontrada en models.yaml.")
        return None

    provider = model_info.get('provider')
    # Carga la configuración base del modelo (models.yaml)
    base_model_config = model_info.get("config", {}).copy()
    provider_model_name = base_model_config.pop("modelo_provider") # Extrae el nombre del modelo del proveedor

    # Combina la configuración base con los overrides del agente
    merged_config = base_model_config.copy()
    _top_k_value = None # Inicializar a None

    if agent_cerebro_config:
        agent_overrides_clean = agent_cerebro_config.copy() # Crear una copia limpia para trabajar
        
        if 'temperatura' in agent_overrides_clean:
            merged_config['temperature'] = agent_overrides_clean.pop('temperatura')
        
        if 'top_k' in agent_overrides_clean:
            _top_k_value = agent_overrides_clean.pop('top_k') # Extraer top_k para manejo especial
            
        if 'modelo_base_id' in agent_overrides_clean:
            agent_overrides_clean.pop('modelo_base_id')
        
        # Fusionar cualquier parametro restante que no haya sido mapeado o limpiado
        merged_config.update(agent_overrides_clean)

    print(f"🧠  Cargando cerebro: {model_info.get("nombre_display")} (Proveedor: {provider})")

    try:
        if provider == 'ollama':
            ollama_options = {}
            if _top_k_value is not None:
                ollama_options['top_k'] = _top_k_value
            if ollama_options: # Solo añadir 'options' si tiene contenido
                merged_config['options'] = ollama_options
            return ChatOllama(model=provider_model_name, **merged_config)
        
        elif provider == 'deepseek':
            deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
            if not deepseek_api_key:
                print("\n❌ Error: DEEPSEEK_API_KEY no fue encontrada en el entorno.")
                return None
            merged_config['api_key'] = deepseek_api_key
            # 'top_k' no es un argumento directo para ChatDeepSeek, por lo tanto no lo incluimos
            # directamente en merged_config. Si LangChain soporta pasarlo via client_kwargs o model_kwargs
            # se haria aqui. Por ahora, asumimos que DeepSeek usara su default.
            return ChatDeepSeek(model=provider_model_name, **merged_config)
            
        else:
            print(f"❌ Error: Proveedor de modelo '{provider}' no es soportado.")
            return None
            
    except KeyError as e:
        print(f"❌ Error de Configuración: Falta la clave obligatoria {e} en la configuración del modelo '{model_id}'.")
        return None
    except Exception as e:
        print(f"❌ Error inesperado al inicializar el modelo '{model_id}': {e}")
        return None
