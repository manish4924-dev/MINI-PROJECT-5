import datetime as dt
import os
import expense_utils as eu
from report_utils import build_monthly_report, display_report, save_report

def get_expense_date():
    while True:
        date_text = input(
            "Enter date (YYYY-MM-DD, blank for today): "
        ).strip()

        if date_text == "":
            return dt.date.today()

        try:
            return dt.datetime.strptime(
                date_text, "%Y-%m-%d"
            ).date()

        except ValueError:
            print("Invalid date! Please enter YYYY-MM-DD.")

def add_expense(expenses):
    print("\n----- ADD NEW EXPENSE -----")

    description = input("Enter description: ").strip()
    while not description:
        print("Description cannot be empty.")
        description = input("Enter description: ").strip()

    category = input(
        "Enter category (Food/Travel/Study/Bills/Other): "
    ).strip().title()

    while not category:
        print("Category cannot be empty.")
        category = input("Enter category: ").strip().title()

    while True:
        try:
            amount = float(input("Enter amount (Rs.): "))

            if eu.is_valid_amount(amount):
                break

            print("Amount must be greater than zero.")

        except ValueError:
            print("Please enter a valid amount.")

    expense_date = get_expense_date()

    reference_id = eu.generate_reference_id(expenses)

    expense = {
        "reference_id": reference_id,
        "date": expense_date,
        "description": description,
        "category": category,
        "amount": amount
    }

    expenses.append(expense)

    print("\nExpense added successfully!")
    print("Reference ID:", reference_id)


def main():
    expenses = []
    print("=" * 50)
    print("       PERSONAL EXPENSE TRACKER")
    print("=" * 50)

    while True:

        print("\n1. Add Expense")
        print("2. View All Expenses")
        print("3. Generate Monthly Report")
        print("4. Exit")

        choice = input("\nEnter your choice: ")
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            eu.display_expenses(expenses)
        elif choice == "3":
            report_text = build_monthly_report(expenses)
            display_report(report_text)
            save_choice = input(
                "\nDo you want to save the report? (y/n): "
            ).lower()

            if save_choice == "y":
                folder_path = os.path.dirname(__file__)
                reports_folder = os.path.join(
                    folder_path, "reports"
                )
                os.makedirs(reports_folder, exist_ok=True)
                report_path = os.path.join(
                    reports_folder, "monthly_report.txt"
                )
                if os.path.exists(report_path):
                    overwrite = input(
                        "Report already exists. Replace it? (y/n): "
                    ).lower()

                    if overwrite != "y":
                        print("Report not saved.")
                        continue

                save_report(report_text, report_path)
                print("Report saved successfully!")
                print("Location:", report_path)

        elif choice == "4":
            print("\nThank you for using Expense Tracker!")
            break
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main()