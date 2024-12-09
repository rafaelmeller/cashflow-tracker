import csv


class Transaction:
    def __init__(self, date, type, amount, category, description):
        self.date = date
        self.type = type
        self.amount = amount
        self.category = category
        self.description = description

    def __str__(self):
        f"{self.date} | {self.type} | {self.category} | {self.description} | ${self.amount:.2f}"



class CashFlowTracker:
    ...
    # Attributes: transactions (list of Transaction objects).
    # Methods:
        # add_transaction(): Adds a new transaction (manually or via CSV upload).
        # filter_transactions(): Filters transactions by date or category.
        # generate_summary(): Calculates totals for incomes, expenses, and by category.

def main():
    print("Welcome to CashFlow Tracker!")
    while True:
        print("Here's the menu:")
        print("1. Import transactions from CSV file")
        print("2. Add new transaction manually")
        print("3. Choose category of uncategorized transactions")
        print("4. Generate summary")
        print("5. Export summary to a CSV or Excel file")
        print("6. Exit")

        choice = input("Enter the number of your choice: ").strip()
        if choice == "1":
            path = input("Enter the path to the CSV file: ")
            read_csv(path)
        elif choice == "2":
            # Add new transaction manually
            pass
        elif choice == "3":
            # Choose category of uncategorized transactions
            pass
        elif choice == "4":
            # Generate summary
            pass
        elif choice == "5":
            # Export summary
            pass
        elif choice == "6":
            print("Thank you for using CashFlow Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            continue


def read_csv(path):
    # Create a function to read transactions from a CSV file and add them to the tracker.
    ...


def categorize_transaction():
    # Create a function to re-categorize transactions that are uncategorized.
    ...


def export_summary():
    # Create a function to export the summary to a CSV or Excel file.
    ...


if __name__ == "__main__":
    main()