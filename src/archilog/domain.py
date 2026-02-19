from dataclasses import dataclass

from src.archilog.data import Cagnotte, describe_cagnotte

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

    debtors = [m for m in mean_deviations if m.amount < 0]
    creditors = [m for m in mean_deviations if m.amount > 0]

    i = 0
    j = 0

    while i < len(debtors) and j < len(creditors):
        debtor = debtors[i]
        creditor = creditors[j]

        amount = min(-debtor.amount, creditor.amount)

        transactions.append(
            Transaction(
                sender_name=debtor.participant_name,
                receiver_name=creditor.participant_name,
                amount=round(amount, 2),
            )
        )

        debtor.amount += amount
        creditor.amount -= amount

        if abs(debtor.amount) < 0.01:
            i += 1
        if abs(creditor.amount) < 0.01:
            j += 1

    return transactions