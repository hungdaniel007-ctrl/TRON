# OLLAMA-LANGCHAING-AGENTE/permanencia/SqlAlchemySQLite.py
# --- FILOSOFÍA DEL PROYECTO ---
# Principio de "Cápsulas Inviolables":
# Se prioriza la identificación, aislamiento y corrección de la funcionalidad rota,
# dejando intactas las partes del código que ya han demostrado ser estables y funcionales.
# Esto minimiza el riesgo de introducir nuevas regresiones y asegura un progreso robusto.
#
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
    def __init__(self, db_type: str, db_config: dict):
        """
        El constructor inicializa el GestorDePersistencia de forma agnóstica a la DB.
        Recibe el tipo de DB (ej. 'sqlite', 'postgresql') y un diccionario de configuración.
        """
        self._db_type = db_type
        self._db_config = db_config
        
        connection_string = self._build_connection_string()
        
        # Nos aseguramos que el directorio para la base de datos SQLite exista si es el caso
        if self._db_type == 'sqlite' and 'db_path' in self._db_config:
            db_dir = os.path.dirname(self._db_config['db_path'])
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
                
        # Configuración específica para SQLite para evitar errores en CLI y servidores
        connect_args = {}
        if self._db_type == 'sqlite':
            connect_args["check_same_thread"] = False
            
        self.engine = create_engine(connection_string, connect_args=connect_args)
        
        # Crea la tabla si no existe
        Base.metadata.create_all(self.engine)
        # La fábrica de sesiones para interactuar con la DB
        self.Session = sessionmaker(bind=self.engine)

    def _build_connection_string(self) -> str:
        """
        Método interno para construir la cadena de conexión de SQLAlchemy.
        """
        if self._db_type == 'sqlite':
            db_path = self._db_config.get('db_path')
            if not db_path:
                raise ValueError("Para SQLite, 'db_path' debe especificarse en db_config.")
            return f'sqlite:///{db_path}'
        elif self._db_type == 'postgresql':
            # Ejemplo para PostgreSQL (requiere psycog2 o similar)
            # host = self._db_config.get('host', 'localhost')
            # port = self._db_config.get('port', 5432)
            # user = self._db_config.get('user', 'user')
            # password = self._db_config.get('password', 'password')
            # dbname = self._db_config.get('dbname', 'mydatabase')
            # return f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
            raise NotImplementedError("Soporte para PostgreSQL aún no implementado.")
        else:
            raise ValueError(f"Tipo de base de datos '{self._db_type}' no soportado.")

    def guardar_mensaje(self, usuario: str, titulo: str, rol: str, contenido: str, modelo: str = None, metadata: dict = None):
        """
        [PUERTO] Puerto de Entrada: Recibe datos de la conversación y los persiste.
        Esta es la interfaz principal para almacenar nuevos mensajes en la base de datos.
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
        [PUERTO] Puerto de Salida: Devuelve los últimos N mensajes de una sesión.
        Esta es la interfaz principal para recuperar el historial de mensajes de la base de datos.
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

    def obtener_titulos_conversacion(self, usuario_id: str) -> list[str]:
        """
        [PUERTO] Puerto de Salida: Devuelve una lista de todos los títulos únicos
        de conversación para un usuario específico.
        """
        session = self.Session()
        titulos = session.query(HistorialChat.titulo_conversacion).filter_by(
            usuario_id=usuario_id
        ).distinct().order_by(HistorialChat.titulo_conversacion).all()
        session.close()
        return [titulo for titulo, in titulos]

    def obtener_conversacion_completa(self, usuario_id: str, titulo: str) -> list:
        """
        [PUERTO] Puerto de Salida: Devuelve todos los mensajes de una conversación específica.
        """
        session = self.Session()
        mensajes = session.query(HistorialChat).filter_by(
            usuario_id=usuario_id,
            titulo_conversacion=titulo
        ).order_by(HistorialChat.id).all()
        session.close()
        return mensajes
