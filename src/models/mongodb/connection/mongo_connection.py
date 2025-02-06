from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv
import os


class MongoConnection:
    def __init__(self) -> None:
        load_dotenv()
        self.__connection_string = os.getenv("MONGO_CONNECTION_STRING")
        self.__database_name = os.getenv("MONGO_DATABASE_NAME")
        
        if not self.__connection_string or not self.__database_name:
            raise ValueError("Variáveis de ambiente MONGO_CONNECTION_STRING e MONGO_DATABASE_NAME são obrigatórias")
            
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self) -> None:
        try:
            if not self.__client:
                # Configurações para conexão local sem SSL
                self.__client = MongoClient(
                    self.__connection_string,
                    serverSelectionTimeoutMS=5000,  # Timeout de 5 segundos
                    ssl=False,  # Desabilita SSL para conexão local
                    tls=False   # Desabilita TLS para conexão local
                )
                self.__db_connection = self.__client[self.__database_name]
                # Teste de conexão
                self.__client.admin.command('ping')
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            if self.__client:
                self.__client.close()
            raise ConnectionError(f"Falha ao conectar ao MongoDB: {str(e)}")
        except Exception as e:
            if self.__client:
                self.__client.close()
            raise e

    def get_db_connection(self):
        if self.__db_connection is None:
            self.connect_to_db()
        return self.__db_connection

    def close_db_connection(self) -> None:
        if self.__client:
            self.__client.close()
            self.__client = None
            self.__db_connection = None

mongo_connection_handler = MongoConnection()
