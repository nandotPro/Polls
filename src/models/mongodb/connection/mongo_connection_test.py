import pytest
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from src.models.mongodb.connection.mongo_connection import mongo_connection_handler
import os

def test_mongo_connection():
    """Testa a conexão com o MongoDB"""
    try:
        # Debug: Mostrar a string de conexão atual (ocultando senha)
        connection_string = os.getenv("MONGO_CONNECTION_STRING")
        print(f"\nString de conexão atual: {connection_string}")
        
        # Tentar conectar
        mongo_connection_handler.connect_to_db()
        
        # Pegar conexão
        db = mongo_connection_handler.get_db_connection()
        
        # Verificar se a conexão foi estabelecida
        assert db is not None, "A conexão com o MongoDB não foi estabelecida"
        
        # Teste adicional: tentar realizar uma operação simples
        db.command("ping")
        
        print("✅ Conexão com MongoDB estabelecida com sucesso!")
        
    except ConnectionError as e:
        pytest.fail(f"❌ Erro de conexão com MongoDB: {str(e)}")
    except Exception as e:
        pytest.fail(f"❌ Erro inesperado: {str(e)}")
    finally:
        mongo_connection_handler.close_db_connection()

if __name__ == "__main__":
    test_mongo_connection() 