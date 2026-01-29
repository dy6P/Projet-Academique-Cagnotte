from datetime import date
from datetime import time
import click
import uuid

from dataclasses import dataclass


@dataclass
class Item:
    id: uuid.UUID
    name: str


@click.group()
def cli():
    pass


@cli.command()
@click.option("-n", "--name", prompt="Name", help="The name of the cagnotte.")


def create_cagnotte(name: str):
    item = Item(uuid.uuid4(), name)
    click.echo(item)

def delete_cagnotte(name: str):
    pass

def add_depense(cagnotte_name: str, participant_name: str, amount: float, date: date, time: time):
    pass

def delete_depense(cagnotte_name: str, participant_name: str, date: date, time: time):
    pass