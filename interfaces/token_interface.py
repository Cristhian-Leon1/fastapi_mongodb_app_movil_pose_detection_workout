from pymongo.collection import Collection


class TokenInterface:

    @staticmethod
    def add_token(collection: Collection, token: dict):
        return collection.insert_one(token)

    @staticmethod
    def get_token(collection: Collection, token: dict):
        return collection.find_one({"token": token})
