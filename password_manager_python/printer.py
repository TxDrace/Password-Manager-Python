from password_manager_python import account
from rich.console import Console
from rich.table import Table
from typing import List

def print_credentials(credentials:List[account.Account]): 
    with Console() as console:
        table = Table("Idx", "Service", "Username", "Description", show_lines=True)

        for index, credential in enumerate(credentials): 
            table.add_row(str(index + 1), credential.service, credential.username, credential.description)

        console.print(table)

def print_one_credentail_details(credential: account.Account):
    with Console() as console:
        table = Table("Service", "Username", "Password", "Description")
        table.add_row(credential.service, credential.username, str(credential.password), credential.description)
        console.print(table)