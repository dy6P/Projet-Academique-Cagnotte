from dataclasses import dataclass

from archilog.data import MoneyPot, get_money_pot


@dataclass
class MeanDeviation:
    name: str
    amount: float


@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float


def get_money_pot_details(money_pot_name: str) -> tuple[MoneyPot, list[Transaction]]:
    money_pot = get_money_pot(money_pot_name)
    return money_pot, compute_transactions(money_pot)


# pure function, easily testable
def compute_transactions(money_pot: MoneyPot) -> list[Transaction]:
    mean = sum(e.amount for e in money_pot.expenses) / len(money_pot.expenses)
    mean_deviations = [
        MeanDeviation(e.paid_by, e.amount - mean) for e in money_pot.expenses
    ]
    transactions: list[Transaction] = []

    # TODO compute transcations below
    # ...

    return transactions
