import click

from .data import (
    create_expense as create_expense_service,
    delete_expense as delete_expense_service,
    delete_cagnotte as delete_cagnotte_service,
    all_cagnottes as all_cagnottes_service,
    create_cagnotte as create_cagnotte_service,
)

from .domain import describe_cagnotte_transactions as describe_cagnotte_transactions_service

@click.group()
def cli() -> None:
    pass

@cli.command(help="Create a cagnotte.")
@click.option("-cn", "--cagnotte_name", prompt="Cagnotte name ", required=True)
def create_cagnotte(cagnotte_name: str) -> None:
    create_cagnotte_service(cagnotte_name)


@cli.command(help="Get the list of all cagnottes.")
def all_cagnottes() -> None:
    for c in all_cagnottes_service():
        click.echo(c.name)

@cli.command(help="Get details of a cagnotte.")
@click.option("-cn", "--cagnotte_name", prompt="Cagnotte name ", required=True)
def describe_cagnotte_transactions(cagnotte_name: str) -> None:
    cagnotte, transactions = describe_cagnotte_transactions_service(cagnotte_name)
    click.echo("The Cagnotte contains : ")
    for e in cagnotte.expenses:
        click.echo(f"{e.participant_name} : {e.amount}€ ({e.date})")
    click.echo("To balance the cagnotte : ")
    if transactions:
        for t in transactions:
            click.echo(f"{t.sender_name} must send {t.amount}€ to {t.receiver_name}.")
    else:
        click.echo("Nothing to do.")

@cli.command(help="Delete a cagnotte with all associated expenses.")
@click.option("-cn", "--cagnotte_name", prompt="Cagnotte name ", required=True)
def delete_cagnotte(cagnotte_name: str) -> None:
    delete_cagnotte_service(cagnotte_name)


@cli.command(help="Add an expense to a cagnotte, create a cagnotte if needed.")
@click.option("-cn", "--cagnotte_name", prompt="Cagnotte name ", required=True)
@click.option("-pn", "--participant_name", prompt="Participant name ", required=True)
@click.option("-a", "--amount", prompt="Amount ", required=True)
def add_expense(cagnotte_name: str, participant_name: str, amount: float) -> None:
    create_expense_service(cagnotte_name, participant_name, amount)


@cli.command(help="Remove an expense from a money pot, delete the money pot if no more expense.")
@click.option("-cn", "--cagnotte_name", prompt="Cagnotte name ", required=True)
@click.option("-pn", "--participant_name", prompt="Participant name ", required=True)
def remove_expense(cagnotte_name: str, participant_name: str) -> None:
    delete_expense_service(cagnotte_name, participant_name)