from redis import Redis
from dotenv import load_dotenv
import os

class RedisConnection:
    def __init__(self) -> None:
        load_dotenv()
        self.__redis_conn = None

    def connect(self) -> Redis:
        redis_conn = Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            decode_responses=True,
            # password=os.getenv('REDIS_PASSWORD'),
        )
        self.__redis_conn = redis_conn
        return redis_conn
    
    def get_connection(self) -> Redis:
        if not self.__redis_conn:
            self.connect()
        return self.__redis_conn

redis_connection_handler = RedisConnection()