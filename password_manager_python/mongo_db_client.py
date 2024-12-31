from pymongo import MongoClient
from pymongo.server_api import ServerApi
from password_manager_python import system_interact

class SingletonMetaClass(type): 
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class MongoDbClient(metaclass=SingletonMetaClass):
    def __init__(self):
        self.uri = system_interact.get_mongodb_uri()
        self.client = MongoClient(self.uri, server_api=ServerApi(version='1'))
        self.database = self.client.get_database("password-manager")
        self.collection = self.database.get_collection("credentials")

    