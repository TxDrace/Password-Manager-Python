from password_manager_python import crypto
from bson import ObjectId

class Account: 
    def __init__(self, _id:ObjectId, _service:str, _username:str, _password:bytes, _description:str):
        self.id = _id
        self.service = _service
        self.username = _username
        self.password = _password
        self.description = _description

    def get_decrypted_password(self) -> str: 
        return crypto.decrypt(self.password).decode("utf-8")