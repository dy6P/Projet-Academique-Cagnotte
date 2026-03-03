import click

from flask import render_template, request, redirect, url_for, Flask
from .data import (
    add_expense as add_expense_service,
    remove_expense as remove_expense_service,
    delete_money_pot as delete_money_pot_service,
    all_money_pots as all_money_pots_service,
    init_database as init_database_service,
    describe_money_pot as describe_money_pot_service
)
from .domain import describe_money_pot_transactions as describe_money_pot_transactions_service

@click.group()
def cli() -> None:
    pass

@cli.command(help="Initialise database (Create table Expenses if not exists).")
def init_database() -> None:
    init_database_service()

@cli.command(help="Get the list of all money_pots.")
def all_money_pots() -> None:
    for c in all_money_pots_service():
        click.echo(c.name)

@cli.command(help="Get details of a money_pot.")
@click.option("-mpn", "--money_pot_name", prompt="Money_pot name ", required=True)
def describe_money_pot(money_pot_name: str) -> None:
    money_pot = describe_money_pot_service(money_pot_name)
    click.echo("The Money_pot contains : ")
    if not money_pot.expenses:
        click.echo("No expenses recorded.")
    else:
        for e in money_pot.expenses:
            click.echo(
                f"{e.participant_name} : {e.amount}€ "
                f"({e.datetime.strftime('%Y-%m-%d %H:%M:%S')})"
            )


@cli.command(help="Get details of a money_pot.")
@click.option("-mpn", "--money_pot_name", prompt="Money_pot name ", required=True)
def describe_money_pot_transactions(money_pot_name: str) -> None:
    money_pot, transactions = describe_money_pot_transactions_service(money_pot_name)
    click.echo("The Money_pot contains : ")
    if not money_pot.expenses:
        click.echo("No expenses recorded.")
    else:
        for e in money_pot.expenses:
            click.echo(
                f"{e.participant_name} : {e.amount}€ "
                f"({e.datetime.strftime('%Y-%m-%d %H:%M:%S')})"
            )
    click.echo("To balance the money_pot : ")
    if transactions:
        for t in transactions:
            click.echo(
                f"{t.sender_name} must send {t.amount}€ to {t.receiver_name}."
            )
    else:
        click.echo("Nothing to do.")

@cli.command(help="Delete a money_pot with all associated expenses.")
@click.option("-mpn", "--money_pot_name", prompt="Money_pot name ", required=True)
def delete_money_pot(money_pot_name: str) -> None:
    delete_money_pot_service(money_pot_name)

@cli.command(help="Add an expense to a money_pot, create a money_pot if needed.")
@click.option("-mpn", "--money_pot_name", prompt="Money_pot name ", required=True)
@click.option("-pn", "--participant_name", prompt="Participant name ", required=True)
@click.option("-a", "--amount", prompt="Amount ", required=True)
def add_expense(money_pot_name: str, participant_name: str, amount: float) -> None:
    add_expense_service(money_pot_name, participant_name, amount)

@cli.command(help="Remove an expense from a money pot, delete the money pot if no more expense.")
@click.option("-mpn", "--money_pot_name", prompt="Money_pot name ", required=True)
@click.option("-pn", "--participant_name", prompt="Participant name ", required=True)
def remove_expense(money_pot_name: str, participant_name: str) -> None:
    remove_expense_service(money_pot_name, participant_name)


app = Flask(__name__)
init_database_service()

@app.route("/", methods=["GET"])
def home():
    money_pots = all_money_pots_service()
    return render_template("index.html", money_pots=money_pots)

@app.route("/money_pot/view", methods=["POST"])
def describe_money_pot_route():
    name = request.form.get("money_pot_name")
    money_pot, transactions = describe_money_pot_transactions_service(name)
    return render_template(
        "money_pot.html",
        money_pot=money_pot,
        transactions=transactions
    )

@app.route("/money_pot/add_expense", methods=["POST"])
def add_expense_route():
    name = request.form["money_pot_name"]
    participant = request.form["participant_name"]
    amount = float(request.form["amount"])
    add_expense_service(name, participant, amount)
    return redirect(url_for("detail", name=name))

@app.route("/money_pot/remove_expense", methods=["POST"])
def remove_expense_route():
    name = request.form["money_pot_name"]
    participant = request.form["participant_name"]
    remove_expense_service(name, participant)
    return redirect(url_for("detail", name=name))

@app.route("/money_pot/delete", methods=["POST"])
def delete_money_pot_route():
    name = request.form.get("money_pot_name").lower()
    delete_money_pot_service(name)
    return redirect(url_for("home"))
