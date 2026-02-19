import uuid
import click
import sqlite3
from datetime import date
from dataclasses import dataclass


@dataclass
class Item:
    id: uuid.UUID
    name: str

@click.group()
def cli():
    pass

db = sqlite3.connect("storage/CAGNOTTE.db")

@cli.command()
def all_cagnotte():
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(cursor.fetchall())

@cli.command()
@click.option("--name", prompt="Cagnotte searched", help="The name of the cagnotte.")
def describe_cagnotte(name: str):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {name}")
    columns = [desc[0] for desc in cursor.description]
    print(columns)
    for row in cursor.fetchall():
        print(row)

@cli.command()
@click.option("--name", prompt="Cagnotte to be created", help="The name of the cagnotte.")
def create_cagnotte(name: str):
    cursor = db.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} (participant TEXT PRIMARY KEY, amount REAL NOT NULL DEFAULT 0.0, debt REAL NOT NULL DEFAULT 0.0, date TEXT NOT NULL DEFAULT (DATE('now')))")
    db.commit()
    click.echo(f"Cagnotte created : {name}")

@cli.command()
@click.option("--name", prompt="Cagnotte to be removed", help="The name of the cagnotte.")
def delete_cagnotte(name: str):
    cursor = db.cursor()
    cursor.execute(f"DROP TABLE {name}")
    db.commit()
    click.echo(f"Cagnotte deleted : {name}")

@cli.command()
@click.option("--cagnotte_name", prompt="Cagnotte name", help="The name of the cagnotte.")
@click.option("--participant_name", prompt="Participant name", help="The name of the participant.")
@click.option("--amount", prompt="Amount of the expense", help="The amount of the expense.")
def add_expense(cagnotte_name: str, participant_name: str, amount: float):
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO {cagnotte_name} (participant, amount) VALUES (?, ?)", (participant_name, amount))
    db.commit()
    calculate(cagnotte_name)
    click.echo(f"Cagnotte    : {cagnotte_name}")
    click.echo(f"Participant : {participant_name}")
    click.echo(f"Date        : {date.today()}")
    click.echo(f"Amount      : {amount} $")

@cli.command()
@click.option("--cagnotte_name", prompt="Cagnotte name", help="The name of the cagnotte.")
@click.option("--participant_name", prompt="Participant name", help="The name of the participant.")
def delete_expense(cagnotte_name: str, participant_name: str):
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM {cagnotte_name} WHERE participant = ?", (participant_name,))
    db.commit()
    click.echo(f"{participant_name} has retired his expense in the cagnotte {cagnotte_name}.")

#@cli.command()
#@click.option("--name", prompt="Cagnotte name", help="The name of the cagnotte.")
def calculate(name: str):
    cursor1 = db.cursor()
    cursor1.execute(f"SELECT participant, amount FROM {name}")
    resultat = cursor1.fetchall()
    nb_participants = len(resultat)
    total =  0
    participations = {}
    for expense in resultat:
        total += expense[1]
        participations[expense[0]] = expense[1]
    mean = total / nb_participants
    cursor2 = db.cursor()
    for participant in participations.keys():
        amount = participations[participant]
        debt = mean - amount
        cursor2.execute(f"UPDATE {name} SET debt = ? WHERE participant = ?", (debt, participant))
    db.commit()

db.close()
