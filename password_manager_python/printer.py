from password_manager_python import account
from rich.console import Console
from rich.table import Table

def print_credentials(_credentials:list[account.Account]): 
    with Console() as console:
        table = Table("Idx", "Service", "Username", "Description", show_lines=True)

        for index, credential in enumerate(_credentials): 
            table.add_row(str(index + 1), credential.service, credential.username, credential.description)

        console.print(table)


def print_one_credentail_details(_credential: account.Account):
    with Console() as console:
        table = Table("Service", "Username", "Password", "Description")
        table.add_row(_credential.service, _credential.username, str(_credential.password), _credential.description)
        console.print(table)


def print_service_list(_service_list:list[str]): 
    with Console() as console:
        table = Table("Idx", "Service", show_lines=True)
        for idx,srv in enumerate(_service_list): 
            table.add_row(str(idx), srv)
        console.print(table)
