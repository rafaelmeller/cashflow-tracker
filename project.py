import csv


class Transaction:
    def __init__(self, date, amount, category, description):
        self.date = date
        # self.type = type
        self.amount = amount
        self.category = category
        self.description = description


    def __str__(self):
        f"{self.date} | {self.category} | {self.description} | ${self.amount:.2f}"



class CashFlowTracker:
    def __init__(self):
        self.transactions = []
        self.budgets = {}


    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        return self.transactions


    def categorize_transactions(self, transaction, category):
        transaction.category = category
        return transaction


    def filter_transactions(self, filtering_condition):
        if isinstance(filtering_condition, tuple):
            start_date, end_date = filtering_condition
            return [t for t in self.transactions if start_date <= t.date <= end_date]
        elif isinstance(filtering_condition, str):
            return [t for t in self.transactions if t.category == filtering_condition]
        else:
            raise ValueError("Invalid filtering condition.")

    
    def generate_summary(self):
        ...
    # generate_summary(): Calculates totals for incomes, expenses, and by category.


    def set_budget(self, category, amount):
        ...


    def __str__(self):
        ...



def main():
    cashflowtracker = CashFlowTracker()
    print("Welcome to CashFlow Tracker!")
    while True:
        print("Here's the menu:")
        print("1. Import transactions from CSV file")
        print("2. Add new transaction manually")
        print("3. Choose category for transactions")
        print("5. Set budget for each category")
        print("4. Generate filtered summary")
        print("5. Set budget for each category")
        print("6. View budget report")  
        print("7. Export summary or report to a CSV or Excel file")
        print("8. Exit")

        choice = input("Enter the number of your choice: ").strip()
        if choice == "1":
            path = input("Enter the path to the CSV file: ")
            read_csv(path)

        elif choice == "2":
            # Add new transaction manually
            pass

        elif choice == "3":
            while True:
                # Choose category of transactions
                print("1. If you want to categorize uncategorized transactions")
                print("2. If you want to change the category already used")
                choice = input("Enter your choice: ").strip()
                if choice == "1":
                    grouped_uncategorized = get_transactions_from_category(cashflowtracker)
                    for description, transactions in grouped_uncategorized.items():
                        print(f"Transactions with description: {description}")
                        for transaction in transactions:
                            print(transaction)
                        category = input("Enter the category for the above transactions: ").strip()
                        for transaction in transactions:
                            cashflowtracker.categorize_transactions(transaction, category)
                        print(f"All transactions with description '{description}' have been categorized as '{category}'.")
                    break
                elif choice == "2":
                    category = input("Enter the category you want to filter transactions by: ").strip()
                    filtered_transactions = get_transactions_from_category(cashflowtracker, category)
                    for description, transactions in filtered_transactions.items():
                        print(f"Transactions with description: {description}")
                        for transaction in transactions:
                            print(transaction)
                        category = input("Enter the category for the above transactions: ").strip()
                        for transaction in transactions:
                            cashflowtracker.categorize_transactions(transaction, category)
                        print(f"All transactions with description '{description}' have been categorized as '{category}'.")
                    break
                else:
                    print("Invalid choice, please check menu and choose the desired action.")
                    continue

        elif choice == "4":
            # Generate filtered summary
            pass

        elif choice == "5":
            # choose budget for each category
            pass

        elif choice == "6":
            # View budget report
            pass

        elif choice == "7":
            # Export summary
            pass

        elif choice == "8":
            print("Thank you for using CashFlow Tracker. Goodbye!")
            break
        
        else:
            print("Invalid choice, please check menu and choose the desired action.")
            continue


def read_csv(path):
    # TODO: Create a function to read transactions from a CSV file and add them to the tracker
    ...


def get_transactions_from_category(cashflowtracker, choice=None):
    if choice:
        return cashflowtracker.filter_transactions(choice)
    else:
        # Filter transactions that are uncategorized
        uncategorized = [t for t in cashflowtracker.transactions if t.category == ""]
        
        # Group uncategorized transactions by description
        grouped_uncategorized = {}
        for transaction in uncategorized:
            if transaction.description not in grouped_uncategorized:
                grouped_uncategorized[transaction.description] = []
            grouped_uncategorized[transaction.description].append(transaction)
        
        return grouped_uncategorized


def export_summary():
    # Create a function to export the summary to a CSV or Excel file.
    ...


if __name__ == "__main__":
    main()