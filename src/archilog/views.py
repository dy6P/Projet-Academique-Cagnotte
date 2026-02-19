import click

from src.archilog.data import (
    create_expense,
    delete_expense,
    delete_cagnotte,
    all_cagnottes,
    create_cagnotte,
)

from src.archilog.domain import describe_cagnotte_transactions

@click.group()
def cli() -> None:
    pass

@cli.command(help="Initialize the database.")
def create_cagnotte(cagnotte_name: str) -> None:
    create_cagnotte(cagnotte_name)


@cli.command(help="Get the list of all cagnottes.")
def all_cagnottes() -> None:
    for c in all_cagnottes():
        click.echo(c.name)

@cli.command(help="Get details of a cagnotte.")
@click.option("-m", "--cagnotte_name", required=True)
def describe_cagnotte_transactions(cagnotte_name: str) -> None:
    mp, transactions = describe_cagnotte_transactions(cagnotte_name)

    click.echo("The money pot contains:")
    for e in mp.expenses:
        click.echo(f"  {e.paid_by} : {e.amount}€ ({e.datetime})")

    click.echo("To balance the money pot:")
    if transactions:
        for t in transactions:
            click.echo(f"  {t.sender} must send {t.amount}€ to {t.receiver}.")
    else:
        click.echo("  Nothing to do.")

@cli.command(help="Delete a cagnotte with all associated expenses.")
@click.option("-m", "--cagnotte_name", required=True)
def delete_cagnotte(cagnotte_name: str) -> None:
    delete_cagnotte(cagnotte_name)


@cli.command(help="Add an expense to a cagnotte, create a cagnotte if needed.")
@click.option("-m", "--cagnotte_name", required=True)
@click.option("-p", "--participant_name", required=True)
@click.option("-a", "--amount", type=float, required=True)
def add_expense(cagnotte_name: str, participant_name: str, amount: float) -> None:
    create_expense(cagnotte_name, participant_name, amount)


@cli.command(
    help="Remove an expense from a money pot, delete the money pot if no more expense."
)
@click.option("-m", "--cagnotte_name-pot", required=True)
@click.option("-p", "--participant_name-by", required=True)
def remove_expense(cagnotte_name: str, participant_name: str) -> None:
    delete_expense(cagnotte_name, participant_name)