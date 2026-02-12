# OLLAMA-LANGCHAING-AGENTE/core/factory.py
import os
import yaml
from functools import lru_cache
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI # Using ChatOpenAI for OpenRouter compatible APIs

# Load config from config.yaml
@lru_cache(maxsize=1)
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_model(model_id: str, task_type: str = "general"):
    """
    Dynamically initializes and returns a LangChain chat model based on model_id and task_type.
    model_id can be 'ollama/<model_name>', 'openrouter/<model_name>', or a direct model name
    from config.yaml's 'models' section.
    """
    config = load_config()
    models_config = config.get("models", {})

    # Determine the actual model name and provider based on model_id
    if model_id.startswith("ollama/"):
        actual_model_name = model_id.split("ollama/")[1]
        provider = "ollama"
    elif model_id.startswith("openrouter/"):
        actual_model_name = model_id.split("openrouter/")[1]
        provider = "openrouter"
    elif model_id in models_config:
        # Use predefined models from config.yaml
        if task_type == "simple_task":
            actual_model_name = models_config.get("simple_task", models_config.get("default_ollama"))
            provider = "ollama"
        elif task_type == "complex_task":
            actual_model_name = models_config.get("complex_task", models_config.get("default_ollama"))
            provider = "openrouter" # Assuming complex tasks use OpenRouter
        elif task_type == "image_gen":
            actual_model_name = models_config.get("image_gen", "dall-e-3") # Default for image gen
            provider = "openrouter" # Assuming image gen uses OpenRouter
        else: # Default or general tasks
            actual_model_name = models_config.get("default_ollama")
            provider = "ollama"
    else:
        # Fallback if model_id is a direct model name without prefix or config entry
        actual_model_name = model_id
        if "llama" in model_id or "gemma" in model_id: # Basic heuristic for Ollama models
            provider = "ollama"
        else:
            provider = "openrouter" # Assume other direct names are via OpenRouter/OpenAI compatible

    # Set parameters based on task type
    temperature = 0.7
    max_tokens = 4096

    if task_type == "complex_task":
        temperature = 0.1 # More deterministic for complex logic
        max_tokens = 8192 # Larger context window for complex tasks
    elif task_type == "image_gen":
        temperature = 0.5 # Creative tasks
        max_tokens = 500 # Output might be shorter, like a prompt
    elif task_type == "simple_read":
        temperature = 0.0 # Strict for reading tasks
        max_tokens = 1024 # Smaller context

    if provider == "ollama":
        if not actual_model_name:
             raise ValueError("Ollama model name not specified in config or model_id.")
        return ChatOllama(model=actual_model_name, temperature=temperature, base_url="http://localhost:11434")
    elif provider == "openrouter":
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY", config.get("openrouter", {}).get("api_key"))
        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment or config.yaml")
        
        # OpenRouter compatible models can often be used via ChatOpenAI
        # The base_url and api_key point to OpenRouter
        return ChatOpenAI(
            model=actual_model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            openai_api_key=openrouter_api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            model_name=actual_model_name # Ensure model_name is passed
        )
    else:
        raise ValueError(f"Unsupported model provider: {provider}")

if __name__ == "__main__":
    # Example usage:
    # Ensure Ollama server is running and models are pulled (e.g., ollama pull llama3.1:8b gemma2)
    # Ensure OPENROUTER_API_KEY is set in your environment for OpenRouter models

    print("--- Testing Ollama models ---")
    try:
        ollama_model_general = get_model("default_ollama", "general")
        print(f"Loaded Ollama model for general task: {ollama_model_general.model}")
        # response = ollama_model_general.invoke("Hello, who are you?")
        # print(f"Response: {response.content}")

        ollama_model_simple = get_model("gemma2", "simple_task")
        print(f"Loaded Ollama model for simple task: {ollama_model_simple.model}")
        # response = ollama_model_simple.invoke("What is 1+1?")
        # print(f"Response: {response.content}")
    except Exception as e:
        print(f"Error loading Ollama model: {e}")

    print("\n--- Testing OpenRouter models (requires OPENROUTER_API_KEY) ---")
    # You would typically set this in your shell environment or a .env file
    # os.environ["OPENROUTER_API_KEY"] = "sk-or-..." # Placeholder, replace with actual key if running directly
    try:
        openrouter_model_complex = get_model("deepseek/deepseek-chat", "complex_task")
        print(f"Loaded OpenRouter model for complex task: {openrouter_model_complex.model_name}")
        # response = openrouter_model_complex.invoke("Explain the theory of relativity.")
        # print(f"Response: {response.content}")

        openrouter_model_image = get_model("dall-e-3", "image_gen")
        print(f"Loaded OpenRouter model for image generation: {openrouter_model_image.model_name}")
        # response = openrouter_model_image.invoke("A painting of a cat.")
        # print(f"Response: {response.content}")
    except ValueError as e:
        print(f"Error loading OpenRouter model: {e}")
    except Exception as e:
        print(f"Other error with OpenRouter model: {e}")
