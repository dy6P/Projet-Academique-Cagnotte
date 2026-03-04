from dataclasses import dataclass, field
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, select, insert, delete

engine = create_engine("sqlite:///storage/MONEY_POTS.db", echo=False)
metadata = MetaData()

Expenses = Table(
    "Expenses",
    metadata,
    Column("money_pot", String, primary_key=True),
    Column("participant", String, primary_key=True),
    Column("amount", Float, nullable=False),
    Column("date", String, nullable=False),
    Column("time", String, nullable=False)
)

def init_database():
    metadata.create_all(engine)

@dataclass
class Expense:
    money_pot_name: str
    participant_name: str
    amount: float
    date: str
    time: str

    @classmethod
    def from_row(cls, row):
        return cls(
            row.money_pot.lower(),
            row.participant.lower(),
            row.amount,
            row.date,
            row.time,
        )

@dataclass
class Money_pot:
    name: str
    expenses: list[Expense] = field(default_factory=list)

def all_money_pots() -> list[Money_pot]:
    with engine.connect() as conn:
        rows = conn.execute(select(Expenses.c.money_pot).distinct()).all()
    return [Money_pot(r.money_pot) for r in rows]

def describe_money_pot(money_pot_name: str) -> Money_pot:
    with engine.connect() as conn:
        rows = conn.execute(select(Expenses).where(Expenses.c.money_pot == money_pot_name.lower())).all()
    if not rows:
        raise Exception(f"'{money_pot_name}' money_pot not found.")
    expenses = [Expense.from_row(r) for r in rows]
    return Money_pot(money_pot_name, expenses)

def add_expense(money_pot_name: str, participant_name: str, amount: float) -> None:
    remove_expense(money_pot_name, participant_name)
    now = datetime.now()
    with engine.begin() as conn:
        conn.execute(
            insert(Expenses).values(
                money_pot=money_pot_name.lower(),
                participant=participant_name.lower(),
                amount=amount,
                date=now.strftime("%Y-%m-%d"),
                time=now.strftime("%H:%M:%S"),
            )
        )

def remove_expense(money_pot_name: str, participant_name: str) -> None:
    with engine.begin() as conn:
        conn.execute(delete(Expenses).where(
        (Expenses.c.money_pot == money_pot_name.lower()) &
        (Expenses.c.participant == participant_name.lower())
    ))

def delete_money_pot(money_pot_name: str) -> None:
    with engine.begin() as conn:
        conn.execute(delete(Expenses).where(Expenses.c.money_pot == money_pot_name.lower()))