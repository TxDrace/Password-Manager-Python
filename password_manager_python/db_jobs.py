from password_manager_python import mongo_db_client, account, crypto
import typer
import nacl.utils

def query_credentials(_service:str|None = None, _username:str|None = None) -> list[account.Account]: 
    try:
        query = {}
        if _service is not None and _username is None: 
            query = { 
                "service": {
                    "$regex": _service,
                    "$options": "i"
                }
            }
        elif _service is None and _username is not None:
            query = { 
                "username": {
                    "$regex": _username,
                    "$options": "i"
                }
            }

        elif _service is not None and _username is not None: 
            query = { 
                "service": {
                    "$regex": _service,
                    "$options": "i"
                },
                "username": {
                    "$regex": _username,
                    "$options": "i"
                }
            }
        
        accounts:list[account.Account] = []
        client = mongo_db_client.MongoDbClient()
        result = client.collection.find(query)
        for item in result:
            accounts.append(account.Account(
                item["_id"], item["service"], item["username"], item["password"], item["description"]
            ))
        return accounts

    except Exception as e:
        raise Exception("Unable to find credentials due to the following error: ", e)


def add_one_credential(_service:str, _username:str, _password:nacl.utils.EncryptedMessage, _description:str):
    try: 
        client = mongo_db_client.MongoDbClient()
        client.collection.insert_one({
            "service": _service,
            "username": _username,
            "password": _password,
            "description": _description
        })

    except Exception as e:
        raise Exception("Unable to add new account due to the following error: ", e)
    

def edit_one_credential(selected_account:account.Account,
                        _new_service:str, 
                        _new_username:str, 
                        _new_password:nacl.utils.EncryptedMessage, 
                        _new_description:str): 

    try: 
        client = mongo_db_client.MongoDbClient()
        client.collection.update_one(
            {
                "_id": selected_account.id
            },
            {
                "$set": {
                    "service": _new_service,
                    "username": _new_username,
                    "password": _new_password,
                    "description": _new_description
                }
            }
        )

    except Exception as e:
        raise Exception("Unable to add edit account due to the following error: ", e)
    

def remove_one_credential(_account:account.Account): 
    try: 
        client = mongo_db_client.MongoDbClient()
        client.collection.delete_one({"_id":_account.id})

    except Exception as e:
        raise Exception("Unable to add delete account due to the following error: ", e)


def query_all_services() -> list[str]:
    try: 
        client = mongo_db_client.MongoDbClient()
        service_list = client.collection.distinct("service")
        return service_list

    except Exception as e:
        raise Exception("Unable to add new account due to the following error: ", e)