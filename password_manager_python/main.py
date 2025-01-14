import typer
from typing import Optional
from typing_extensions import Annotated
from password_manager_python import feature

app = typer.Typer(no_args_is_help=True)

@app.callback()
def callback():
    """
    A simple CLI tool used for storing credentials in the cloud \n
    """

@app.command(help="Find a credential in the database")
def find(
    service: Annotated[Optional[str], typer.Option("--service", "-s", help="Service, vendor or website associated with this account", show_default=False)] = None,
    username: Annotated[Optional[str], typer.Option("--username", "-u", help="User namem, email of this account", show_default=False)] = None
):
    feature.find_credentials(service, username)


@app.command(help="Add a credential to the database")
def add(
    service: Annotated[str, typer.Option("--service", "-s", help="Service associated with this account", show_default=False, prompt="Service")],
    username: Annotated[str,  typer.Option("--username", "-u", help="Username this account", show_default=False, prompt="Username")],
    password: Annotated[str, typer.Option("--password", "-p", help="Password of this account", show_default=False, prompt="Password", hide_input=True, confirmation_prompt=True)],
    description: Annotated[str, typer.Option("--description", "-d", help="Description of this account", show_default=False, prompt="Description")] = ""
):
    feature.add_one_credentail(service, username, password, description)
    

@app.command(help="Edit a credential in the database")
def edit(
    service: Annotated[Optional[str], typer.Option("--service", "-s", help="Service, vendor or website associated with this account", show_default=False)] = None,
    username: Annotated[Optional[str], typer.Option("--username", "-u", help="User namem, email of this account", show_default=False)] = None
):
    feature.edit_one_credential(service, username)
    

@app.command(help="Remove a credential in the database")
def remove(
    service: Annotated[Optional[str], typer.Argument(help="Service, vendor or website associated with this account", show_default=False)] = None,
    username: Annotated[Optional[str], typer.Argument(help="User namem, email of this account", show_default=False)] = None
):
    feature.remove_one_credential(service, username)


@app.command(help="Reset master password, re-encrypt all passwords with new master password")
def reset(
    master_password: Annotated[str, typer.Option("--master-password", "-mp", help="New master password", show_default=False, prompt="New master password", hide_input=True, confirmation_prompt=True)],
):
    feature.reset_database(master_password)


@app.command(help="List all services associated with your accounts")
def list():
    feature.list_all_service()


@app.command(help="Import data from a json file")
def import_data(
    path: Annotated[str, typer.Option("--path", "-p", help="Path to data file", show_default=False, prompt="Path to data file")],
):
    feature.import_data_from_json_file(path)


@app.command(help="Export data to a json file")
def export_data(
    path: Annotated[str, typer.Option("--path", "-p", help="Destination folder", show_default=False, prompt="Path to destination folder")],
):
    feature.export_data_to_json_file(path)