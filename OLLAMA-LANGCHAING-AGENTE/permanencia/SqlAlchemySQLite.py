# OLLAMA-LANGCHAING-AGENTE/permanencia/SqlAlchemySQLite.py
"""
Nodo de Permanencia:
- Encapsula TODA la lógica de base de datos.
- Utiliza SQLAlchemy para ser agnóstico del motor de DB (hoy SQLite, mañana podría ser PostgreSQL).
- Define el "Contrato de Datos" de la tabla de historial.
"""
import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Text, Index
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# El "plano" de la tabla SQL, definido como una clase de Python (ORM)
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

    # Índices para acelerar las búsquedas por sesión
    __table_args__ = (Index('idx_session', 'usuario_id', 'titulo_conversacion'),)

# El "conector" que el agente usará para hablar con este nodo
class GestorDePersistencia:
    def __init__(self, db_path: str):
        """
        El constructor recibe la ruta al archivo de la base de datos.
        Si el directorio no existe, lo crea.
        """
        # Nos aseguramos que el directorio para la base de datos exista
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            
        # El motor de conexión. check_same_thread=False es vital para evitar errores en CLI y servidores.
        self.engine = create_engine(f'sqlite:///{db_path}', connect_args={"check_same_thread": False})
        # Crea la tabla si no existe
        Base.metadata.create_all(self.engine)
        # La fábrica de sesiones para interactuar con la DB
        self.Session = sessionmaker(bind=self.engine)

    def guardar_mensaje(self, usuario: str, titulo: str, rol: str, contenido: str, modelo: str = None, metadata: dict = None):
        """
        Puerto de Entrada: Recibe datos de la conversación y los persiste.
        """
        session = self.Session()
        ahora = datetime.now()
        
        # Convertir metadatos a JSON si existen
        metadata_str = json.dumps(metadata) if metadata else None
        
        nuevo_registro = HistorialChat(
            usuario_id=usuario,
            titulo_conversacion=titulo,
            rol=rol,
            mensaje=contenido,
            fecha=ahora.strftime("%Y-%m-%d"),
            hora=ahora.strftime("%H:%M:%S"),
            modelo_usado=modelo,
            metadata_json=metadata_str
        )
        
        session.add(nuevo_registro)
        session.commit()
        session.close()

    def obtener_historial_reciente(self, usuario: str, titulo: str, limite: int) -> list:
        """
        Puerto de Salida: Devuelve los últimos N mensajes de una sesión.
        """
        if limite == 0:
            return []
        
        session = self.Session()
        # Query: Filtrar por sesión, ordenar por ID descendente para obtener los más nuevos
        # La indentación correcta es clave en estas llamadas encadenadas.
        mensajes = session.query(HistorialChat).filter_by(
            usuario_id=usuario, 
            titulo_conversacion=titulo
        ).order_by(HistorialChat.id.desc()).limit(limite).all()
        
        session.close()
        
        # Devolvemos los mensajes en orden cronológico (el más antiguo primero)
        return mensajes[::-1]
