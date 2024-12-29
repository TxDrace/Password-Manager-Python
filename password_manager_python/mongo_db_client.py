from pymongo import MongoClient
from pymongo.server_api import ServerApi

class SingletonMetaClass(type): 
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class MongoDbClient(metaclass=SingletonMetaClass):
    def __init__(self):
        self.uri = "mongodb+srv://nguyenhaituyen1804:F8B63cumwheGHWkq@cluster0.4kyr8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = MongoClient(self.uri, server_api=ServerApi(version='1', strict=True, deprecation_errors=True))
        self.database = self.client.get_database("password-manager")
        self.collection = self.database.get_collection("credentials")

    