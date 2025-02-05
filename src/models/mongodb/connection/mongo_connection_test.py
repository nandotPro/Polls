import pytest
from src.models.mongodb.connection.mongo_connection import mongo_connection_handler

def test_mongo_connection():
    try:
        # Tentar conectar
        print("Testando conexão com MongoDB...")
        mongo_connection_handler.connect_to_db()
        
        # Pegar conexão
        db = mongo_connection_handler.get_db_connection()
        
        # Verificar se a conexão foi estabelecida
        assert db is not None, "A conexão com o MongoDB não foi estabelecida."
        
        print("✅ Conexão com MongoDB OK!")
    except Exception as e:
        pytest.fail(f"❌ Erro na conexão com MongoDB: {str(e)}")
    finally:
        mongo_connection_handler.close_db_connection()

if __name__ == "__main__":
    test_mongo_connection() 