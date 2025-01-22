import json
from src.models.redis.connection.redis_connection import RedisConnection

class UserCacheRepository:
    def __init__(self):
        self.redis = RedisConnection().get_connection
        self.EXPIRE_TIME = 3600  # 1 hora em segundos

    def set_user(self, user_id: str, user_data: dict) -> None:
        key = f"user:{user_id}"
        self.redis.setex(
            key,
            self.EXPIRE_TIME,
            json.dumps(user_data)
        )

    def get_user(self, user_id: str) -> dict | None:
        key = f"user:{user_id}"
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def delete_user(self, user_id: str) -> None:
        key = f"user:{user_id}"
        self.redis.delete(key)