import datetime as dt
from tabulate import tabulate

from expense_utils import calculate_total, category_totals

def build_monthly_report(expenses, year=None, month=None):

    today = dt.date.today()
    if year is None:
        year = today.year

    if month is None:
        month = today.month

    monthly_expenses = [
        expense for expense in expenses
        if expense["date"].year == year
        and expense["date"].month == month
    ]

    month_name = dt.date(
        year, month, 1
    ).strftime("%B %Y")

    report = []

    report.append("=" * 60)
    report.append("           MONTHLY EXPENSE REPORT")
    report.append(f"             Report Month: {month_name}")
    report.append("=" * 60)

    if not monthly_expenses:
        report.append("No expenses found for this month.")
        return "\n".join(report)

    rows = []

    for expense in monthly_expenses:

        rows.append([
            expense["reference_id"],
            expense["date"].strftime("%Y-%m-%d"),
            expense["description"],
            expense["category"],
            f"Rs. {expense['amount']:.2f}"
        ])

    table = tabulate(
        rows,
        headers=[
            "Reference ID",
            "Date",
            "Description",
            "Category",
            "Amount"
        ],
        tablefmt="grid"
    )

    report.append(table)

    
    total = calculate_total(monthly_expenses)
    report.append( f"Total Spending: Rs. {total:.2f}\n")
    
    report.append("Category-wise Spending:\n")
    totals = category_totals(monthly_expenses)

    for category, amount in totals.items():
        report.append( f"{category}: Rs. {amount:.2f}")

    average = total / len(monthly_expenses)
    report.append( f"Average Expense: Rs. {average:.2f}\n")
    report.append("=" * 60)
    return "\n".join(report)

def display_report(report_text):
    print("\n")
    print(report_text)

def save_report(report_text, file_path):
    with open(file_path,"w",encoding="utf-8")as file:
                file.write(report_text)