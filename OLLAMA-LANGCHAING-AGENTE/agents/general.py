# OLLAMA-LANGCHAING-AGENTE/agents/general.py
import os
import sys

# Add the project root to sys.path to resolve imports from parent directories
# This allows running the script from the project root, e.g., `python agents/general.py`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# LangChain Imports for a basic chat interaction
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage

def main():
    """
    Main function for the basic chat agent (Iteration 1).
    Connects to Ollama and has a simple conversation with the Gemma model.
    """
    print("--- Iniciando Iteración 1: Agente de Chat Básico ---")
    print("Conectando con el modelo 'gemma3:4b' a través de Ollama...")

    try:
        # 1. Instanciar el modelo LLM
        # Using the recommended langchain_ollama package.
        # It defaults to http://localhost:11434, which is correct as per the user's setup.
        llm = ChatOllama(model="gemma3:4b", temperature=0)
        print("Conexión con el modelo establecida.")

        # 2. Definir una pregunta de prueba
        question = "Hola, ¿puedes presentarte brevemente en español?"
        print(f"\nEnviando pregunta al modelo: '{question}'")

        # 3. Invocar el modelo y obtener la respuesta
        response = llm.invoke([HumanMessage(content=question)])

        # 4. Imprimir la respuesta
        print("\n--- Respuesta del Modelo ---")
        print(response.content)
        print("\n--- Fin de la Iteración 1: ÉXITO ---")

    except Exception as e:
        print(f"\n--- Fin de la Iteración 1: ERROR ---")
        print(f"Ocurrió un error al intentar comunicarse con el modelo Ollama: {e}")
        print("\nPor favor, verifica lo siguiente:")
        print("1. El servidor de Ollama está en ejecución ('ollama serve').")
        print("2. El modelo 'gemma3:4b' ha sido descargado ('ollama pull gemma3:4b').")
        print("3. La dirección del servidor (por defecto http://localhost:11434) es correcta y no está bloqueada por un firewall.")

if __name__ == "__main__":
    main()
