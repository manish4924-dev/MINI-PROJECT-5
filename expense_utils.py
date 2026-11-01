import random
import math
from tabulate import tabulate

def is_valid_amount(amount):
    return (
        isinstance(amount, (int, float))
        and amount > 0
    )

def generate_reference_id(expenses):
    existing_ids = {
        expense["reference_id"]
        for expense in expenses
    }

    while True:
        reference_id = f"EXP-{random.randint(100000, 999999)}"
        if reference_id not in existing_ids:
            return reference_id

def calculate_total(expenses):
    total = sum(expense["amount"]
        for expense in expenses
           )
    return math.floor(total * 100 + 0.5) / 100

def category_totals(expenses):
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = (
            totals.get(category, 0)
            + expense["amount"]
        )

    for category in totals:
        totals[category] = (
            math.floor(totals[category] * 100 + 0.5)
            / 100
        )
    return totals

def display_expenses(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    rows = []

    for expense in expenses:
        rows.append([
            expense["reference_id"],
            expense["date"].strftime("%Y-%m-%d"),
            expense["description"],
            expense["category"],
            f"Rs. {expense['amount']:.2f}"
        ])
    print("----- ALL EXPENSES -----\n")

    print(tabulate(
        rows,
        headers=[
            "Reference ID",
            "Date",
            "Description",
            "Category",
            "Amount"
        ],
        tablefmt="grid"
    ))