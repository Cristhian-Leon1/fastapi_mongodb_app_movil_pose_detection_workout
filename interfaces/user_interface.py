from bson import ObjectId
from pymongo.collection import Collection

from backend.models.user_model import UserModel


class UserInterface:
    @staticmethod
    def add_user(collection: Collection, user: dict):
        return collection.insert_one(user)

    @staticmethod
    def get_user(collection: Collection, email: dict):
        return collection.find_one({"email": email})

    @staticmethod
    def update_user(collection: Collection, user_id: ObjectId, updated_data: dict):
        collection.update_one({"_id": user_id}, {"$set": updated_data})

    @staticmethod
    def delete_user(collection: Collection, user_id: ObjectId):
        collection.delete_one({"_id": user_id})

    @staticmethod
    def delete_all_users(collection: Collection):
        collection.delete_many({})
