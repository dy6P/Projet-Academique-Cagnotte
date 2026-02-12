import sqlite3
from dataclasses import dataclass, field
from datetime import datetime

db_url = "data.db"
db = None


def get_db():
    global db
    if db is None:
        db = sqlite3.connect(db_url)
    return db


def init_database():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                money_pot TEXT NOT NULL,
                paid_by TEXT NOT NULL,
                amount REAL NOT NULL,
                datetime TEXT NOT NULL,
                PRIMARY KEY (money_pot, paid_by)
            )
        """)


@dataclass
class Expense:
    money_pot: str
    paid_by: str
    amount: float
    datetime: datetime

    @classmethod
    def from_db(cls, row: tuple):
        return cls(row[0], row[1], row[2], datetime.fromisoformat(row[3]))


@dataclass
class MoneyPot:
    name: str
    expenses: list[Expense] = field(default_factory=list)


# money pots
# ==========


def get_money_pot(money_pot_name: str) -> MoneyPot:
    with get_db() as db:
        results = db.execute(
            "select * from expenses where money_pot = ?", (money_pot_name,)
        ).fetchall()
        if results:
            return MoneyPot(money_pot_name, [Expense.from_db(r) for r in results])
        else:
            raise Exception(f"'{money_pot_name}' money pot not found.")


def get_all_money_pots() -> list[MoneyPot]:
    with get_db() as db:
        results = db.execute("select distinct money_pot from expenses").fetchall()
    return [MoneyPot(*r) for r in results]


def delete_money_pot(money_pot_name: str):
    with get_db() as db:
        db.execute("delete from expenses where money_pot = ?", (money_pot_name,))
        db.commit()


# expenses
# ========


def create_expense(money_pot_name: str, paid_by: str, amount: float) -> None:
    with get_db() as db:
        db.execute(
            "insert into expenses(money_pot, paid_by, amount, datetime) values (?, ?, ?, ?)",
            (money_pot_name, paid_by, amount, datetime.now().isoformat()),
        )
        db.commit()


def delete_expense(money_pot_name: str, paid_by: str) -> None:
    with get_db() as db:
        db.execute(
            "delete from expenses where money_pot = ? and paid_by = ?",
            (money_pot_name, paid_by),
        )
        db.commit()
