from pymongo import MongoClient
from pymongo.server_api import ServerApi


def establish_connection():
    try:
        uri = ("mongodb+srv://admin:adminadmin@invernaderoup.1aeb9rn.mongodb.net/InvernaderoUP_DB?retryWrites=true&w"
               "=majority")
        client = MongoClient(uri, server_api=ServerApi('1'))

        db = client.get_database()
        users_collection = db.Users
        tokens_collection = db.Tokens

        client.admin.command('ping')
        print("Ping completado. Conexión establecida correctamente a MongoDB!")
        return users_collection, tokens_collection
    except Exception as e:
        print(e)


