import os

master_password_env_key = "PM_MASTER_PASSWORD"
mongodb_uri_key = "MONGODB_URI"

def get_master_password() -> bytes:
    master_password = os.getenv(master_password_env_key)
    if (master_password is None): 
        raise Exception("Cannot found master password from enviroment variable")
    return master_password.encode("utf-8")

def get_mongodb_uri() -> str:
    mongodb_uri = os.getenv(mongodb_uri_key)
    if (mongodb_uri is None): 
        raise Exception("Cannot found mongodb URI from enviroment variable")
    return mongodb_uri

def check_env_change(): 
    pass