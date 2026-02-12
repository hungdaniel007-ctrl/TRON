# rag_agent_poc.py
# Proof of Concept for a RAG agent using LangChain and Ollama
# Based on user-provided documentation and directives.

import os
import bs4
import asyncio

# Add project root to sys.path to handle module resolution
import sys
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# LangChain Imports based on provided documentation
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS  # Using a simple local vector store
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

def print_step(step, step_name):
    """Helper function to print agent steps clearly."""
    print(f"\n--- {step_name} ---")
    if "messages" in step:
        for message in step["messages"]:
            message.pretty_print()

async def main():
    """
    Main asynchronous function to build and run the RAG agent proof of concept.
    """
    print("--- Iniciando Prueba de Concepto: Agente RAG con Ollama y LangChain ---")

    # --- PASO 2: Indexing Pipeline (Carga y División) ---
    print("\n[Paso 2.1] Cargando documento desde la web...")
    try:
        loader = WebBaseLoader(
            web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    class_=("post-content", "post-title", "post-header")
                )
            ),
        )
        docs = loader.load()
        print(f"Documento cargado. {len(docs[0].page_content)} caracteres encontrados.")

        print("\n[Paso 2.2] Dividiendo documento en chunks...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        print(f"Documento dividido en {len(splits)} chunks.")
    except Exception as e:
        print(f"ERROR durante la carga o división de documentos: {e}")
        return

    # --- PASO 3: Configuración del Vector Store (Almacenamiento y Recuperación) ---
    print("\n[Paso 3.1] Inicializando embeddings con Ollama (gemma3:4b)...")
    try:
        # Using a model suitable for embeddings. If gemma3:4b is not ideal,
        # Ollama will still attempt to use it. A dedicated embedding model is better in production.
        embeddings = OllamaEmbeddings(model="gemma3:4b")

        print("\n[Paso 3.2] Creando y poblando Vector Store local (FAISS)...")
        # FAISS is a good local, file-based vector store that doesn't require a separate server.
        vector_store = FAISS.from_documents(splits, embeddings)
        retriever = vector_store.as_retriever(k=2) # Retrieve top 2 relevant chunks
        print("Vector Store creado y poblado en memoria.")
    except Exception as e:
        print(f"ERROR durante la inicialización del Vector Store o Embeddings: {e}")
        print("Por favor, asegúrate de que el servidor de Ollama esté en ejecución y el modelo 'gemma3:4b' esté disponible.")
        return

    # --- PASO 4: Implementación de la Herramienta de Recuperación ---
    print("\n[Paso 4] Definiendo la herramienta de recuperación de contexto (RAG)...")
    @tool
    def retrieve_context(query: str) -> str:
        """
        Recupera fragmentos de información de un post sobre agentes LLM para ayudar a responder una pregunta.
        """
        print(f"\n   [Herramienta 'retrieve_context' invocada con query: '{query}']")
        retrieved_docs = retriever.invoke(query)
        serialized = "\n\n".join(
            (f"Source: {doc.metadata.get('source', 'N/A')}\nContent: {doc.page_content}")
            for doc in retrieved_docs
        )
        print("   [Herramienta 'retrieve_context' finalizada. Documentos recuperados.]")
        return serialized

    tools = [retrieve_context]

    # --- PASO 5: Construcción y Ejecución del Agente RAG ---
    print("\n[Paso 5.1] Inicializando LLM con Ollama (gemma3:4b) para el agente...")
    try:
        llm = ChatOllama(model="gemma3:4b", temperature=0)
        agent_executor = create_react_agent(llm, tools)
        print("Agente RAG creado con éxito.")
    except Exception as e:
        print(f"ERROR al crear el agente: {e}")
        return

    print("\n[Paso 5.2] Ejecutando consulta de prueba contra el agente RAG...")
    query = "What is task decomposition?"
    print(f"   Consulta: '{query}'")

    try:
        # Using ainvoke for the async main function
        final_state = await agent_executor.ainvoke({"messages": [HumanMessage(content=query)]})
        
        print("\n--- Respuesta Final del Agente ---")
        final_message = final_state["messages"][-1]
        final_message.pretty_print()

        print("\n--- PRUEBA DE CONCEPTO FINALIZADA CON ÉXITO ---")

    except Exception as e:
        print(f"\nERROR durante la invocación del agente: {e}")
        print("Esto puede deberse a un problema de conexión con el servidor de Ollama o a un error en la respuesta del modelo.")

if __name__ == "__main__":
    # This runs the async main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.")
