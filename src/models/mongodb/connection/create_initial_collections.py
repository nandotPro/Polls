from mongo_connection import mongo_connection_handler

def up():
    try:
        print("Executando migration: create_initial_collections")
        
        # Conectar ao MongoDB
        mongo_connection_handler.connect_to_db()
        db = mongo_connection_handler.get_db_connection()
        
        # Criar collection users com índices
        if "users" not in db.list_collection_names():
            db.create_collection("users")
            db.users.create_index("email", unique=True)
            db.users.create_index("username", unique=True)
            print("Collection 'users' criada com índices!")
        
        # Criar collection polls com índices
        if "polls" not in db.list_collection_names():
            db.create_collection("polls")
            db.polls.create_index("created_by")  # Para buscar enquetes por usuário
            db.polls.create_index("created_at")  # Para ordenação por data
            print("Collection 'polls' criada com índices!")
        
        print("Migration executada com sucesso!")
        
    except Exception as error:
        print(f"Erro na migration: {str(error)}")
        raise error

if __name__ == "__main__":
    up() 