import sqlite3
from dataclasses import dataclass, field
from datetime import date
from data import Expense

db_url = "storage/CAGNOTTE.db"
db = None

def get_db() -> sqlite3.Connection:
    global db
    if db is None:
        db = sqlite3.connect(db_url)
    return db

@dataclass
class Expense:
    cagnotte_name: str
    participant_name: str
    amount: float
    date: date

    @classmethod
    def create_expense(cls, cagnotte_name: str, row: tuple) -> Expense:
        participant, amount, date_str = row
        return cls(
            cagnotte=cagnotte_name,
            participant=participant,
            amount=amount,
            date=date.fromisoformat(date_str)
        )

@dataclass
class Cagnotte:
    name: str
    expenses: list[Expense] = field(default_factory=list)

def create_cagnotte(cagnotte_name: str) -> None:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {cagnotte_name} (participant TEXT PRIMARY KEY, amount REAL NOT NULL DEFAULT 0.0, date TEXT NOT NULL DEFAULT (DATE('now')))")
        db.commit()

def all_cagnottes() -> list[Cagnotte]:
    with get_db() as db:
        cursor = db.cursor()
        results = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        if results:
            return [Cagnotte(*r) for r in results]
        else:
            raise Exception(f"Erreur dans la fonction all_cagnotte.")

def describe_cagnotte(cagnotte_name: str) -> Cagnotte:
    with get_db() as db:
        cursor = db.cursor()
        results = cursor.execute(f"SELECT * FROM {cagnotte_name}").fetchall()
        if results:
            return Cagnotte(cagnotte_name, [Expense.create_expense(cagnotte_name, r) for r in results])
        else:
            raise Exception(f"'{cagnotte_name}' cagnotte not found.")

def delete_cagnotte(cagnotte_name: str) -> None:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(f"DROP TABLE {cagnotte_name}")
        db.commit()

def create_expense(cagnotte_name: str, participant_name: str, amount: float) -> None:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO {cagnotte_name} (participant, amount) VALUES (?, ?)", (participant_name, amount))
        db.commit()

def delete_expense(cagnotte_name: str, participant_name: str) -> None:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM {cagnotte_name} WHERE participant = ?", (participant_name,))
        db.commit()