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
    Column("datetime", String, nullable=False)
)

def init_database():
    metadata.create_all(engine)

@dataclass
class Expense:
    money_pot_name: str
    participant_name: str
    amount: float
    datetime: datetime

    @classmethod
    def from_row(cls, row):
        return cls(
            row.money_pot.lower(),
            row.participant.lower(),
            row.amount,
            datetime.fromisoformat(row.datetime),
        )

@dataclass
class Money_pot:
    name: str
    expenses: list[Expense] = field(default_factory=list)

def all_money_pots() -> list[Money_pot]:
    stmt = select(Expenses.c.money_pot).distinct()
    with engine.connect() as conn:
        rows = conn.execute(stmt).all()
    return [Money_pot(r.money_pot) for r in rows]

def describe_money_pot(money_pot_name: str) -> Money_pot:
    stmt = select(Expenses).where(Expenses.c.money_pot == money_pot_name.lower())
    with engine.connect() as conn:
        rows = conn.execute(stmt).all()
    if not rows:
        raise Exception(f"'{money_pot_name}' money_pot not found.")
    expenses = [Expense.from_row(r) for r in rows]
    return Money_pot(money_pot_name, expenses)

def add_expense(money_pot_name: str, participant_name: str, amount: float) -> None:
    stmt = insert(Expenses).values(
        money_pot=money_pot_name.lower(),
        participant=participant_name.lower(),
        amount=amount,
        datetime=datetime.now().isoformat(),
    )
    with engine.begin() as conn:
        conn.execute(stmt)

def remove_expense(money_pot_name: str, participant_name: str) -> None:
    stmt = delete(Expenses).where(
        (Expenses.c.money_pot == money_pot_name.lower()) & (Expenses.c.participant == participant_name.lower())
    )
    with engine.begin() as conn:
        conn.execute(stmt)

def delete_money_pot(money_pot_name: str) -> None:
    stmt = delete(Expenses).where(Expenses.c.money_pot == money_pot_name.lower())
    with engine.begin() as conn:
        conn.execute(stmt)