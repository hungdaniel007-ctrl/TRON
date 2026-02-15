# OLLAMA-LANGCHAING-AGENTE/agents/agente.py
"""
Nodo Agente Inteligente y Orquestador Principal
- Punto de entrada para el sistema modular.
- Reemplaza la lógica de ejecución de general.py, mientras lo usa como librería.
- Es instanciable, configurable por YAML y respeta todos los estándares CLI.
"""
import sys
import os
import argparse
import yaml
import subprocess
import tempfile
import threading
import queue
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

# --- Imports del Proyecto ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from agents.utils import load_llm, load_model_configs, get_model_id_from_alias
from permanencia.SqlAlchemySQLite import GestorDePersistencia
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_ollama.chat_models import ChatOllama

# Evento global para la cancelación del streaming
stop_streaming_event = threading.Event()

class AgenteInteligente:
    def __init__(self, agente_config: dict, global_model_configs: dict, system_prompt_override: str = None):
        self.config = agente_config
        self.global_configs = global_model_configs
        self.nombre = self.config['nombre']
        self.system_prompt = system_prompt_override if system_prompt_override else self.config['system_prompt']
        
        self.modelo_actual_id = self.config['modelo_base']
        self.llm = load_llm(self.modelo_actual_id, self.global_configs)
        
        memoria_config = self.config['memoria']
        self.memoria = GestorDePersistencia(db_path=memoria_config['db_path'])
        self.ventana_contexto = memoria_config['ventana_contexto']
        
        self.usuario_actual = "cli_user"
        self.titulo_actual = None

    def _stream_ollama_with_cancel(self, messages, output_queue):
        """
        Función de streaming específica para Ollama que usa la API nativa
        y corre en un thread para permitir cancelación real.
        """
        try:
            model_name = self.llm.model
            base_url = getattr(self.llm, 'base_url', "http://localhost:11434")
            
            ollama_messages = []
            for msg in messages:
                if isinstance(msg, SystemMessage):
                    ollama_messages.append({"role": "system", "content": msg.content})
                elif isinstance(msg, HumanMessage):
                    ollama_messages.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    ollama_messages.append({"role": "assistant", "content": msg.content})
            
            url = f"{base_url}/api/chat"
            payload = {
                "model": model_name,
                "messages": ollama_messages,
                "stream": True,
                "options": { "temperature": getattr(self.llm, 'temperature', 0.7) }
            }
            
            response = requests.post(url, json=payload, stream=True)
            
            full_content = ""
            for line in response.iter_lines():
                if stop_streaming_event.is_set():
                    response.close()
                    output_queue.put(("cancelled", full_content))
                    return
                
                if line:
                    try:
                        data = json.loads(line)
                        chunk_content = data.get("message", {}).get("content", "")
                        full_content += chunk_content
                        output_queue.put(("chunk", chunk_content))
                        if data.get("done", False): break
                    except json.JSONDecodeError: continue
            
            output_queue.put(("done", full_content))
            
        except Exception as e:
            output_queue.put(("error", str(e)))

    def procesar_mensaje(self, entrada_usuario: str, stream: bool = True, quiet: bool = False):
        # La persistencia solo se activa si hay un título de sesión.
        persistir = self.titulo_actual is not None

        mensajes_para_llm = [SystemMessage(content=self.system_prompt)]
        
        if persistir:
            historial_db = self.memoria.obtener_historial_reciente(
                self.usuario_actual, self.titulo_actual, limite=self.ventana_contexto
            )
            for mensaje_db in historial_db:
                if mensaje_db.rol == 'user':
                    mensajes_para_llm.append(HumanMessage(content=mensaje_db.mensaje))
                elif mensaje_db.rol == 'assistant':
                    mensajes_para_llm.append(AIMessage(content=mensaje_db.mensaje))
        
        mensajes_para_llm.append(HumanMessage(content=entrada_usuario))

        if persistir:
            self.memoria.guardar_mensaje(self.usuario_actual, self.titulo_actual, 'user', entrada_usuario)

        if not quiet:
            print(f"\n{self.nombre}: ", end="", flush=True)

        respuesta_completa = ""
        cancelled = False
        
        try:
            # Lógica de streaming diferenciada
            if stream:
                if isinstance(self.llm, ChatOllama):
                    # ---- Streaming robusto para Ollama ----
                    stop_streaming_event.clear()
                    output_queue = queue.Queue()
                    stream_thread = threading.Thread(target=self._stream_ollama_with_cancel, args=(mensajes_para_llm, output_queue))
                    stream_thread.start()
                    
                    while stream_thread.is_alive() or not output_queue.empty():
                        try:
                            status, data = output_queue.get(timeout=0.1)
                            if status == "chunk":
                                print(data, end="", flush=True)
                                respuesta_completa += data
                            elif status in ("done", "cancelled", "error"):
                                if status == "cancelled": cancelled = True
                                if status == "error": print(f"❌ Error en thread: {data}")
                                break
                        except queue.Empty: continue
                    print()
                else:
                    # ---- Streaming estándar para otros proveedores ----
                    for chunk in self.llm.stream(mensajes_para_llm):
                        content = chunk.content or ""
                        print(content, end="", flush=True)
                        respuesta_completa += content
                    print()
            else:
                # ---- Modo sin streaming ----
                resp = self.llm.invoke(mensajes_para_llm)
                print(resp.content)
                respuesta_completa = resp.content
            
            if persistir and not cancelled:
                self.memoria.guardar_mensaje(
                    self.usuario_actual, self.titulo_actual, 'assistant', respuesta_completa, modelo=self.modelo_actual_id
                )
            
        except KeyboardInterrupt:
            if 'stream_thread' in locals() and stream_thread.is_alive():
                stop_streaming_event.set()
                stream_thread.join(timeout=2.0)
            
            if not quiet: print("\n\n🛑 Generación detenida por el usuario.")
            if persistir:
                self.memoria.guardar_mensaje(
                    self.usuario_actual, self.titulo_actual, 'assistant', 
                    respuesta_completa + " [GENERACIÓN INTERRUMPIDA]", modelo=self.modelo_actual_id
                )
        except Exception as e:
            if not quiet: print(f"\n\n❌ Ocurrió un error: {e}")

    def gestionar_titulo_sesion(self) -> str:
        """
        Gestiona la creación o selección del título de la conversación.
        Implementa la lógica de pedir título al inicio.
        """
        titulo = input("Introduce el título para esta conversación (o presiona Enter para decidirlo después): ").strip()
        if titulo:
            print(f"Sesión iniciada con el título: '{titulo}'")
            return titulo
        else:
            print("No se especificó título. Se usará un título temporal y se sugerirá un nombre más adelante.")
            # En el futuro, aquí comenzaría el estado "probationary"
            return "sesion_temporal_" + datetime.now().strftime("%Y%m%d%H%M%S")

    def cambiar_modelo(self, nuevo_identificador: str) -> bool:
        """
        Permite cambiar el cerebro (LLM) del agente en tiempo de ejecución.
        """
        nuevo_id_real = get_model_id_from_alias(nuevo_identificador, self.global_configs) or nuevo_identificador
        
        # Evitar recargar el mismo modelo
        if nuevo_id_real == self.modelo_actual_id:
            print(f"El modelo '{self.modelo_actual_id}' ya está cargado.")
            return True

        nuevo_llm = load_llm(nuevo_id_real, self.global_configs)
        
        if nuevo_llm:
            self.llm = nuevo_llm
            self.modelo_actual_id = nuevo_id_real
            print(f"✅ Cerebro del agente '{self.nombre}' cambiado a: {self.modelo_actual_id}")
            return True
        else:
            print(f"❌ No se pudo cambiar al modelo: {nuevo_identificador}")
            return False

    def iniciar_modo_interactivo(self, stream_por_defecto: bool = True):
        """
        Bucle de chat para la interacción continua con el agente.
        """
        self.titulo_actual = self.gestionar_titulo_sesion()
        
        print("-" * 50)
        print(f"Iniciando Chat Interactivo con '{self.nombre}' (Modelo: {self.modelo_actual_id})")
        print(f"Sesión: '{self.titulo_actual}'")
        print("Comandos: /exit, /model [alias], /stream, /help")
        print("-" * 50)
        
        stream_activo = stream_por_defecto

        while True:
            try:
                u_in = input("\nTú: ").strip()
                if not u_in:
                    continue
                
                # --- Lógica de Comandos ---
                if u_in.lower() == '/exit':
                    print("Cerrando sesión. ¡Hasta luego!")
                    break
                
                if u_in.lower() == '/help':
                    print("\nComandos disponibles:")
                    print("  /exit          - Salir del chat.")
                    print("  /model [alias] - Cambiar el modelo en caliente (ej: /model gema).")
                    print("  /stream        - Activar/desactivar el modo streaming.")
                    print("  /help          - Mostrar esta ayuda.")
                    continue

                if u_in.lower().startswith('/model '):
                    nuevo_modelo_id = u_in.split(" ", 1)[1]
                    self.cambiar_modelo(nuevo_modelo_id)
                    continue
                
                if u_in.lower() == '/stream':
                    stream_activo = not stream_activo
                    print(f"Streaming ahora está {'✅ Activado' if stream_activo else '❌ Desactivado'}.")
                    continue

                # --- Lógica de Chat Normal ---
                self.procesar_mensaje(u_in, stream=stream_activo, quiet=False)
                
            except (KeyboardInterrupt, EOFError):
                print("\n\nCerrando sesión. ¡Hasta luego!")
                break

    def ejecutar_modo_headless(self, mensaje: str, titulo: str, stream: bool = False):
        self.titulo_actual = titulo
        # La persistencia se decide dentro de procesar_mensaje
        self.procesar_mensaje(mensaje, stream=stream, quiet=True)

# --- PUNTO DE ENTRADA PRINCIPAL ---
def main():
    load_dotenv()
    model_configs = load_model_configs()
    try:
        with open(os.path.join(project_root, "config", "agentes.yaml"), "r") as f:
            agentes_configs = yaml.safe_load(f)
    except FileNotFoundError:
        print("❌ Error Fatal: El archivo 'config/agentes.yaml' no fue encontrado.")
        sys.exit(1)

    default_agent_id = agentes_configs['agentes'][0]['id'] if agentes_configs.get('agentes') else None
    parser = argparse.ArgumentParser(description="Framework de Agentes Modulares con Persistencia")
    parser.add_argument('--agent', type=str, default=default_agent_id, help=f"ID del agente a utilizar. Defecto: {default_agent_id}")
    parser.add_argument('-sc', '--headless', action='store_true', help="Activar modo 'sin cabeza' (raw output).")
    parser.add_argument('-m', '--message', type=str, help="Mensaje a enviar en modo headless.")
    parser.add_argument('-ps', '--prompt-sistema', type=str, default=None, help="Sobrescribe el system_prompt del agente.")
    parser.add_argument('-s', '--stream', action='store_true', help="Activar streaming.")
    parser.add_argument('--session', type=str, default=None, help="Título de la sesión para guardar la conversación. Si no se especifica en modo headless, no se guarda.")

    args = parser.parse_args()

    info_agente_seleccionado = next((a for a in agentes_configs['agentes'] if a['id'] == args.agent), None)
    if not info_agente_seleccionado:
        print(f"❌ Error Fatal: Agente '{args.agent}' no definido en 'agentes.yaml'.")
        sys.exit(1)
        
    if not args.headless:
        print(f"Iniciando fábrica para el agente: '{args.agent}'...")
        
    agente = AgenteInteligente(info_agente_seleccionado, model_configs, system_prompt_override=args.prompt_sistema)

    if args.headless:
        if not args.message:
            parser.error("-m/--message es obligatorio en modo headless (-sc).")
        agente.ejecutar_modo_headless(args.message, titulo=args.session, stream=args.stream)
    else:
        agente.iniciar_modo_interactivo(stream_por_defecto=args.stream)

if __name__ == "__main__":
    main()
