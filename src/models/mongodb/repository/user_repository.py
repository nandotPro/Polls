from bson.objectid import ObjectId
from src.models.mongodb.connection.mongo_connection import mongo_connection_handler
from src.models.mongodb.repository.interface.user_repository_interface import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def __init__(self):
        self.db = mongo_connection_handler.get_db_connection()
        self.collection = self.db['users']

    def register_user(self, user_data: dict) -> str:
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    def login_user(self, email: str, password_hash: str) -> dict | None:
        return self.collection.find_one({
            "email": email,
            "password_hash": password_hash
        })

    def find_by_email(self, email: str) -> dict | None:
        return self.collection.find_one({"email": email})

    def find_by_id(self, user_id: str) -> dict | None:
        return self.collection.find_one({"_id": ObjectId(user_id)})

    def find_by_username(self, username: str) -> dict | None:
        return self.collection.find_one({"username": username})

    def delete_user(self, user_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0