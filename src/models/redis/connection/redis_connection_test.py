import pytest
from src.models.redis.connection.redis_connection import redis_connection_handler

def test_redis_connection():
    try:
        print("Testando conexão com Redis...")
        redis = redis_connection_handler.connect()
        assert redis.ping() == True
        print("✅ Conexão com Redis OK!")
    except Exception as e:
        pytest.fail(f"❌ Erro na conexão com Redis: {str(e)}")