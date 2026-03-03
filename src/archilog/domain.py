from dataclasses import dataclass

from .data import Money_pot, describe_money_pot

@dataclass
class MeanDeviation:
    participant_name: str
    amount: float

@dataclass
class Transaction:
    sender_name: str
    receiver_name: str
    amount: float

def describe_money_pot_transactions(money_pot_name: str) -> tuple[Money_pot, list[Transaction]]:
    money_pot = describe_money_pot(money_pot_name.lower())
    return money_pot, calculate_transactions(money_pot)

def calculate_transactions(money_pot: Money_pot) -> list[Transaction]:
    if not money_pot.expenses:
        return []
    mean = sum(e.amount for e in money_pot.expenses) / len(money_pot.expenses)
    mean_deviations = [
        MeanDeviation(e.participant_name, round(e.amount - mean, 2))
        for e in money_pot.expenses
    ]
    debtors = [m for m in mean_deviations if m.amount < 0]
    creditors = [m for m in mean_deviations if m.amount > 0]
    transactions: list[Transaction] = []
    i = 0
    j = 0
    while i < len(debtors) and j < len(creditors):
        debtor = debtors[i]
        creditor = creditors[j]
        amount = min(-debtor.amount, creditor.amount)
        amount = round(amount, 2)
        transactions.append(
            Transaction(
                sender_name=debtor.participant_name,
                receiver_name=creditor.participant_name,
                amount=amount,
            )
        )
        debtor.amount = round(debtor.amount + amount, 2)
        creditor.amount = round(creditor.amount - amount, 2)
        if abs(debtor.amount) < 0.01:
            i += 1
        if abs(creditor.amount) < 0.01:
            j += 1
    return transactions