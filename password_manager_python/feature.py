import typer
from password_manager_python import db_jobs, account, printer, receptionist, system_interact, crypto
import pyinputplus as pyip
import pyperclip
import json
from pathlib import Path


def find_credentials(_service:str|None, _username:str|None):
    accounts:list[account.Account] = db_jobs.query_credentials(_service, _username)

    if (len(accounts) > 0): 
        printer.print_credentials(accounts)
        user_choice = pyip.inputInt("Choose an account: ", min=1, max=len(accounts)) - 1
        selected_account:account.Account = accounts[user_choice]

        pyperclip.copy(selected_account.get_decrypted_password())
        typer.echo(typer.style("[Success] Password has been copied to clipboard", fg=typer.colors.GREEN, bold=True))

    else:
        typer.echo(typer.style(f"[Warning] No credentials found for service '{_service}' and username '{_username}'", fg=typer.colors.RED, bold=True))


def add_one_credentail(_service:str, _username:str, _password:str, _description:str):
    new_password_encrypted = crypto.encrypt(_password.encode("utf-8"))
    db_jobs.add_one_credential(_service, _username, new_password_encrypted, _description)
    typer.echo(typer.style("[Success] New credential has been added to database", fg=typer.colors.GREEN, bold=True))


def edit_one_credential(_service:str|None, _username:str|None):
    accounts:list[account.Account] = db_jobs.query_credentials(_service, _username)

    if (len(accounts) > 0): 
        printer.print_credentials(accounts)
        
        user_choice = pyip.inputInt("Choose an account: ", min=1, max=len(accounts)) - 1
        selected_account:account.Account = accounts[user_choice]
        
        # If user enter, return empty string '', not None        
        new_service, new_username, new_password, new_description = receptionist.get_new_credential_data_to_edit()

        if(not (new_service or new_username or new_password or new_description)): 
            typer.echo(typer.style("[Success] No information found, exit the program", fg=typer.colors.GREEN, bold=True))
            raise typer.Exit(0)

        receptionist.ask_for_confirm(message="Are you sure you want to update?")
        
        # Process new data
        new_service = new_service or selected_account.service
        new_username = new_username or selected_account.username
        new_password_encrypted = crypto.encrypt(new_password.encode("utf-8")) if new_password else selected_account.password
        new_description = new_description or selected_account.description
        
        # Call function to update db with new data
        db_jobs.edit_one_credential(selected_account, new_service, new_username, new_password_encrypted, new_description)
        
        typer.echo(typer.style("[Success] Credentials has been updated", fg=typer.colors.GREEN, bold=True))

    else:
        typer.echo(typer.style(f"[Warning] No credentials found for service '{_service}' and username '{_username}'", fg=typer.colors.RED, bold=True))


def remove_one_credential(_service:str|None, _username:str|None): 
    accounts:list[account.Account] = db_jobs.query_credentials(_service, _username)

    if (len(accounts) > 0): 
        printer.print_credentials(accounts)
        user_choice = pyip.inputInt("Choose an account: ", min=1, max=len(accounts)) - 1
        selected_account:account.Account = accounts[user_choice]
        
        receptionist.ask_for_confirm(message="Are you sure you want to delete?")
        db_jobs.remove_one_credential(selected_account)
        
        typer.echo(typer.style("[Success] Credentials has been deleted", fg=typer.colors.GREEN, bold=True))

    else:
        typer.echo(typer.style(f"[Warning] No credentials found for service '{_service}' and username '{_username}'", fg=typer.colors.RED, bold=True))


def reset_database(_new_master_password:str): 
    try: 
        accounts:list[account.Account] = db_jobs.query_credentials()

        for item in accounts:  
            
            password_decrypted = item.get_decrypted_password()
            new_password_encrypted = crypto.encrypt(password_decrypted.encode("utf-8"), _new_master_password.encode("utf-8"))
            db_jobs.edit_one_credential(item, item.service, item.username, new_password_encrypted, item.description)
            typer.echo(typer.style("[Success] Database has been reset", fg=typer.colors.GREEN, bold=True))

    except Exception as e:
        typer.echo(typer.style(f"[Error] An error occur: {e} \nDid you update the enviroment varible: 'PM_MASTER_PASSWORD' yet?", fg=typer.colors.RED, bold=True))


def list_all_service(): 
    service_list = db_jobs.query_all_services()
    printer.print_service_list(service_list)


def generate_password(_len:int=50):
    new_password = crypto.password_random(_len,5)
    pyperclip.copy(new_password)
    typer.echo(typer.style("[Success] Password has been copied to clipboard", fg=typer.colors.GREEN, bold=True))


def import_data_from_json_file(_path:str):
    try:
        with open(_path, 'r') as file:
            accounts = json.load(file)
            for acc in accounts: 
                db_jobs.add_one_credential(
                    acc["service"], 
                    acc["username"],
                    crypto.encrypt(acc["password"].encode("utf-8")),
                    acc["description"]
                )
        typer.echo(typer.style("[Success] Credentials data has been imported", fg=typer.colors.GREEN, bold=True))
    except Exception as e: 
        typer.echo(typer.style(f"[Error] An error occur: {e}", fg=typer.colors.RED, bold=True))


def export_data_to_json_file(_path:str): 
    try:
        accounts:list[account.Account] = db_jobs.query_credentials()
        if (len(accounts) > 0):
            data = []
            for acc in accounts: 
                data.append({
                    "service": acc.service, 
                    "username": acc.username,
                    "password": acc.get_decrypted_password(),
                    "description": acc.description
                })
            with open(Path(_path) / 'credentials-data-export.json', 'w') as file:
                json.dump(data, file, indent=4)
                
            typer.echo(typer.style("[Success] Credentials data has been imported", fg=typer.colors.GREEN, bold=True))
        else:
            typer.echo(typer.style(f"[Warning] No credentials found", fg=typer.colors.RED, bold=True))

    except Exception as e: 
            typer.echo(typer.style(f"[Error] An error occur: {e}", fg=typer.colors.RED, bold=True))

    
