from bson.objectid import ObjectId
from src.models.mongodb.repository.interface.poll_repository_interface import PollRepositoryInterface

class PollRepository(PollRepositoryInterface):
    def __init__(self, db_connection):
        self.db = db_connection
        self.collection = self.db['polls']

    def _convert_id_to_str(self, poll: dict) -> dict:
        """Converte _id de ObjectId para string"""
        if poll and '_id' in poll:
            poll['_id'] = str(poll['_id'])
        return poll

    def _convert_polls_to_str(self, polls: list) -> list:
        """Converte _id de ObjectId para string em uma lista de polls"""
        return [self._convert_id_to_str(poll) for poll in polls]

    def create_poll(self, poll_data: dict) -> str:
        result = self.collection.insert_one(poll_data)
        return str(result.inserted_id)

    def find_by_id(self, poll_id: str) -> dict | None:
        poll = self.collection.find_one({"_id": ObjectId(poll_id)})
        return self._convert_id_to_str(poll) if poll else None

    def find_all_polls(self, skip: int = 0, limit: int = 10) -> list[dict]:
        polls = list(self.collection.find().skip(skip).limit(limit))
        return self._convert_polls_to_str(polls)

    def find_user_polls(self, user_id: str) -> list[dict]:
        polls = list(self.collection.find({"created_by": user_id}))
        return self._convert_polls_to_str(polls)

    def delete_poll(self, poll_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(poll_id)})
        return result.deleted_count > 0
    
    def increment_vote(self, poll_id: str, option_index: int) -> bool:
        result = self.collection.update_one(
            {"_id": ObjectId(poll_id)},
            {"$inc": {f"options.{option_index}.votes": 1}}
        )
        return result.modified_count > 0
