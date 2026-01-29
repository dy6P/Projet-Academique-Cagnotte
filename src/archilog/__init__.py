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
@click.option("-n", "--name", prompt="Name", help="The name of the item.")
def display(name: str):
    item = Item(uuid.uuid4(), name)
    click.echo(item)
