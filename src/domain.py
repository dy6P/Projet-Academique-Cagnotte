from dataclasses import dataclass

from archilog.data import Cagnotte, describe_cagnotte

@dataclass
class MeanDeviation:
    participant_name: str
    amount: float


@dataclass
class Transaction:
    sender_name: str
    receiver_name: str
    amount: float

def describe_cagnotte_transactions(cagnotte_name: str) -> tuple[Cagnotte, list[Transaction]]:
    cagnotte = describe_cagnotte(cagnotte_name)
    return cagnotte, calculate_transactions(cagnotte)

def calculate_transactions (cagnotte: Cagnotte) -> list[Transaction]:
    mean = sum(e.amount for e in cagnotte.expenses) / len(cagnotte.expenses)
    mean_deviations = [
        MeanDeviation(e.participant_name, e.amount - mean) for e in cagnotte.expenses
    ]
    transactions: list[Transaction] = []

    #
    # ...

    return transactions