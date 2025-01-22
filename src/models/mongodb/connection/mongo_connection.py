from pymongo import MongoClient
from dotenv import load_dotenv
import os


class MongoConnection:
    def __init__(self) -> None:
        load_dotenv()
        self.__connection_string = os.getenv("MONGO_CONNECTION_STRING")
        self.__database_name = os.getenv("MONGO_DATABASE_NAME")
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self) -> None:
        self.__client = MongoClient(self.__connection_string)
        self.__db_connection = self.__client[self.__database_name]

    def get_db_connection(self):
        return self.__db_connection

    def close_db_connection(self) -> None:
        self.__client.close()

mongo_connection_handler = MongoConnection()
