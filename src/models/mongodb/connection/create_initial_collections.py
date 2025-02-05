from mongo_connection import mongo_connection_handler

def create_collections(db):
    """Cria as coleções necessárias no banco de dados."""
    collections = {
        "users": ["email", "username"],
        "polls": ["created_by", "created_at"]
    }
    
    for collection_name, indexes in collections.items():
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            for index in indexes:
                db[collection_name].create_index(index, unique=True)
            print(f"Collection '{collection_name}' criada com índices!")

def up():
    try:
        print("Executando migration: create_initial_collections")
        
        # Conectar ao MongoDB
        mongo_connection_handler.connect_to_db()
        db = mongo_connection_handler.get_db_connection()
        
        # Criar coleções
        create_collections(db)
        
        print("Migration executada com sucesso!")
        
    except Exception as error:
        print(f"Erro na migration: {str(error)}")
        raise error

if __name__ == "__main__":
    up() 