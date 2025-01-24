from mongo_connection import mongo_connection_handler

def test_mongo_connection():
    try:
        # Tentar conectar
        print("Tentando conectar ao MongoDB...")
        mongo_connection_handler.connect_to_db()
        
        # Pegar conexão
        db = mongo_connection_handler.get_db_connection()
        
        # Tentar operação simples
        collections = db.list_collection_names()
        print(f"Conexão bem sucedida! Collections existentes: {collections}")
        
        # Tentar inserir documento de teste
        test_collection = db['test_collection']
        result = test_collection.insert_one({"test": "connection"})
        print(f"Documento inserido com ID: {result.inserted_id}")
        
        # Limpar após teste
        test_collection.delete_one({"_id": result.inserted_id})
        
        return True
        
    except Exception as error:
        print(f"Erro ao conectar: {str(error)}")
        return False

if __name__ == "__main__":
    test_mongo_connection() 