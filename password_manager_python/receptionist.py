import pyinputplus as pyip
import typer

def get_new_credential_data_to_edit() -> tuple: 
    typer.echo(typer.style("Enter new information for this credential [Press ENTER to retain]", fg=typer.colors.BRIGHT_CYAN, bold=True))
    service = pyip.inputStr("New service: ", default=None, blank=True)
    username = pyip.inputStr("New username: ", default=None, blank=True)
    password = pyip.inputPassword("New password: ", default=None, blank=True)
    description = pyip.inputStr("New description: ", default=None, blank=True)
    return (service, username, password, description)


def ask_for_confirm(message:str) -> bool:
    return typer.confirm(typer.style(message, fg=typer.colors.YELLOW, bold=True), abort=True)