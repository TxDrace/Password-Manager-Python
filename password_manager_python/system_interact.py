import os

master_password_env_key = "PM_MASTER_PASSWORD"

def get_master_password() -> bytes:
    master_password = os.getenv(master_password_env_key)
    if (master_password is None): 
        raise Exception("Cannot found master password from enviroment variable")
    return master_password.encode("utf-8")


def check_env_change(): 
    pass