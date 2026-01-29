import uuid
import click
import sqlite3
from dataclasses import dataclass


@dataclass
class Item:
    id: uuid.UUID
    name: str

@click.group()
def cli():
    pass

#sqlite3.connect("../")


@cli.command()
@click.option("--name", prompt="Cagnotte to be created", help="The name of the cagnotte.")
def create_cagnotte(name: str):
    click.echo(f"Cagnotte created : '{name}'")

@cli.command()
@click.option("--name", prompt="Cagnotte to be removed", help="The name of the cagnotte.")
def delete_cagnotte(name: str):
    click.echo(f"Cagnotte deleted : '{name}'")

@cli.command()
@click.option("--name", prompt="Cagnotte name", help="The name of the cagnotte.")
@click.option("--participant_name", prompt="Participant name", help="The name of the participant.")
@click.option("--amount", prompt="Amount of the expense", help="The amount of the expense.")
def add_expense(cagnotte_name: str, participant_name: str, amount: float):
    click.echo(f"Cagnotte    : '{cagnotte_name}'")
    click.echo(f"Participant : '{participant_name}'")
    click.echo(f"Amount      : '{amount}' $")

@cli.command()
@click.option("--name", prompt="Cagnotte name", help="The name of the cagnotte.")
@click.option("--participant_name", prompt="Participant name", help="The name of the participant.")
def delete_expense(cagnotte_name: str, participant_name: str):
    click.echo(f"'{participant_name}' has retired his expense in the cagnotte '{cagnotte_name}'.")

def calculate():
    pass