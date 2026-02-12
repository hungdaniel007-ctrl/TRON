# OLLAMA-LANGCHAING-AGENTE/core/persistence.py
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver
from sqlalchemy import create_engine

def get_checkpointer(uri: str):
    """
    Returns a LangGraph Checkpointer configured with the specified SQLAlchemy URI.
    Supports SQLite and PostgreSQL.
    """
    if uri.startswith("sqlite:///"):
        # For SQLite, use SqliteSaver
        return SqliteSaver.from_conn_string(uri)
    elif uri.startswith("postgresql://") or uri.startswith("postgresql+psycopg2://"):
        # For PostgreSQL, use PostgresSaver
        return PostgresSaver.from_conn_string(uri)
    else:
        raise ValueError(f"Unsupported database URI scheme: {uri}")

if __name__ == "__main__":
    # Example usage for SQLite
    sqlite_uri = "sqlite:///test_memory.db"
    sqlite_saver = get_checkpointer(sqlite_uri)
    print(f"SQLite Checkpointer created for {sqlite_uri}: {sqlite_saver}")

    # Example usage for PostgreSQL (will fail if psycopg2-binary not installed or DB not running)
    # postgres_uri = "postgresql+psycopg2://user:password@host:port/database"
    # try:
    #     postgres_saver = get_checkpointer(postgres_uri)
    #     print(f"PostgreSQL Checkpointer created for {postgres_uri}: {postgres_saver}")
    # except Exception as e:
    #     print(f"Could not create PostgreSQL Checkpointer: {e}")
