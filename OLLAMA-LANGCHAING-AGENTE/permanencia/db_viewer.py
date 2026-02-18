# OLLAMA-LANGCHAING-AGENTE/permanencia/db_viewer.py
"""
Herramienta CLI para visualizar el historial de conversaciones persistido.

Este script permite inspeccionar las conversaciones almacenadas en la base de datos,
listando las sesiones y mostrando los mensajes dentro de una sesión seleccionada.
"""
import argparse
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Index
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import json

# El "plano" de la tabla SQL (debe ser idéntico al de persistence_manager)
Base = declarative_base()

class HistorialChat(Base):
    __tablename__ = 'historial_conversaciones'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(String, nullable=False)
    titulo_conversacion = Column(String, nullable=False)
    rol = Column(String, nullable=False)  # 'user', 'assistant'
    mensaje = Column(Text)
    fecha = Column(String, nullable=False)
    hora = Column(String, nullable=False)
    modelo_usado = Column(String, nullable=True) # Para auditoría
    metadata_json = Column(Text, nullable=True) # Para futuros metadatos (nodos, relaciones, etc.)

    __table_args__ = (Index('idx_session', 'usuario_id', 'titulo_conversacion'),)

def main():
    parser = argparse.ArgumentParser(description="Visor CLI de historial de conversaciones.")
    parser.add_argument('--db-path', type=str, required=True, help="Ruta al archivo de la base de datos SQLite.")
    parser.add_argument('--user', type=str, default="cli_user", help="ID del usuario a filtrar (por defecto: cli_user).")
    
    args = parser.parse_args()

    if not os.path.exists(args.db_path):
        print(f"❌ Error: La base de datos no se encuentra en la ruta: {args.db_path}")
        return

    engine = create_engine(f'sqlite:///{args.db_path}', connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        conversaciones = session.query(HistorialChat.titulo_conversacion).filter_by(
            usuario_id=args.user
        ).distinct().order_by(HistorialChat.titulo_conversacion).all()

        if not conversaciones:
            print(f"No se encontraron conversaciones para el usuario '{args.user}'.")
            return

        print(f"""
--- Conversaciones para el usuario '{args.user}' en {args.db_path} ---""")
        for i, (titulo,) in enumerate(conversaciones):
            print(f"{i+1}. {titulo}")
        print("-" * 50)

        while True:
            try:
                opcion = input("Selecciona el número de una conversación para verla, (S)alir, o (R)ecargar: ").strip().lower()
                if opcion == 's':
                    break
                elif opcion == 'r':
                    # Recargar la lista de conversaciones
                    conversaciones = session.query(HistorialChat.titulo_conversacion).filter_by(
                        usuario_id=args.user
                    ).distinct().order_by(HistorialChat.titulo_conversacion).all()
                    
                    if not conversaciones:
                        print(f"No se encontraron conversaciones para el usuario '{args.user}'.")
                        break

                    print(f"""
--- Conversaciones para el usuario '{args.user}' en {args.db_path} ---""")
                    for i, (titulo,) in enumerate(conversaciones):
                        print(f"{i+1}. {titulo}")
                    print("-" * 50)
                    continue
                
                seleccion = int(opcion) - 1
                if 0 <= seleccion < len(conversaciones):
                    titulo_seleccionado = conversaciones[seleccion][0]
                    
                    mensajes = session.query(HistorialChat).filter_by(
                        usuario_id=args.user,
                        titulo_conversacion=titulo_seleccionado
                    ).order_by(HistorialChat.id).all()
                    
                    print(f"""
--- Conversación: '{titulo_seleccionado}' ---""")
                    for msg in mensajes:
                        print(f"[{msg.fecha} {msg.hora}] {msg.rol.upper()} ({msg.modelo_usado or 'N/A'}):")
                        print(f"  {msg.mensaje}")
                        if msg.metadata_json:
                            try:
                                metadata = json.loads(msg.metadata_json)
                                print(f"  Metadata: {json.dumps(metadata, indent=2)}")
                            except json.JSONDecodeError:
                                print(f"  Metadata (RAW): {msg.metadata_json}")
                        print("-" * 20)
                    print("---------------------------------------")
                else:
                    print("Opción no válida. Por favor, selecciona un número de la lista.")
            except ValueError:
                print("Entrada no válida. Por favor, introduce un número, 'S' o 'R'.")
    except Exception as e:
        print(f"❌ Ocurrió un error al acceder a la base de datos: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
