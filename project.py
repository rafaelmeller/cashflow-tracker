import csv
from datetime import datetime
import re


class Transaction:
    def __init__(self, date, category, description, value):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.category = category
        self.description = description
        self.value = value


    def __str__(self):
        return f"{self.date} | {self.category} | {self.description} | ${self.value:.2f}"


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
        # TODO
        ...
    # Calculates totals for incomes, expenses, and by category.


    def set_budget(self, category, amount):
        # TODO
        ...


    def __str__(self):
        # TODO
        ...



def main():
    cashflowtracker = CashFlowTracker()
    print("Welcome to CashFlow Tracker!")
    print("(Press Ctrl+C to exit the program at any time.)")
    try:
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

            main_choice = input("Enter the number of your choice: ").strip()

            if main_choice == "1":
                while True:
                    path = input("Enter the path to the CSV file: ").strip()
                    if not path.endswith(".csv"):
                        print("Invalid file format. Please enter a valid CSV file.")
                        continue
                    try:
                        for transaction in read_csv(path):
                            cashflowtracker.add_transaction(transaction)
                        print("Transactions have been imported successfully.")

                    except ValueError as e:
                        print(f"Error: {e}")
                        print("To fix this, we have to custom the values for the fields")
                        with open(path) as file:
                            headers = file.readline().strip().split(",")
                            print("Here are the columns in your CSV file:")
                            for index, header in enumerate(headers):
                                print(f"{index + 1}. {header}")

                            while True:
                                try:
                                    date_index = int(input("Enter the number of the column to use for the date: ").strip())
                                    date = headers[date_index - 1]
                                    break
                                except ValueError:
                                    print("Invalid column number. Please enter a valid number.")
                                    continue

                            while True:
                                try:
                                    description_index = int(input("Enter the number of the column to use for the description: ").strip())
                                    description = headers[description_index - 1]
                                    break
                                except ValueError:
                                    print("Invalid column number. Please enter a valid number.")
                                    continue
                            
                            while True:
                                try:
                                    value_index = int(input("Enter the number of the column to use for the value: ").strip())
                                    value = headers[value_index - 1]
                                    break
                                except ValueError:
                                    print("Invalid column number. Please enter a valid number.")
                                    continue

                            try:
                                for transaction in read_csv(path, date, description, value):
                                    cashflowtracker.add_transaction(transaction)
                                print("Transactions have been imported successfully.")
                            except ValueError as e:
                                print("Error: {e}")
                                continue
                    
            elif main_choice == "2":
                print("Enter the details of the transaction:")
                while True:
                    date = input("Date (YYYY-MM-DD): ").strip()
                    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                        print("Invalid date format. Please enter a valid date.")
                        continue
                    break

                while True:
                    print("Now the category.")
                    categories == None

                    # TODO: Review this part
                    categories = set([t.category for t in cashflowtracker.transactions])

                    if categories == None:
                        print("There are no categories being used yet.")
                        print("Type one for your transaction.")
                        category = input("Category: ").strip()
                        break
                    else:
                        print("Here is the list of the already existing categories:")
                        for index, category in enumerate(categories):
                            print(f"{index + 1}. {category}")
                        print("Type one for your transaction.")
                        category = input("Category: ").strip()
                        break  

                while True:
                    description = input("Description: ").strip()
                    if not description:
                        print("Description cannot be empty. Please enter a valid description.")
                        continue
                    break

                while True:
                    print("Now, the value. If it is an income, follow the example: '100.00'")
                    print("If it is an expense, follow the example: '-100.00'")
                    value = input("Value: ").strip()
                    try:
                        value = float(value)
                        break
                    except ValueError:
                        print("Invalid value. Please enter a valid value.")
                        continue
        
                transaction = Transaction(date, category, description, value)
                cashflowtracker.add_transaction(transaction)

            elif main_choice == "3":
                while True:
                    # Choose category of transactions
                    print("1. If you want to categorize uncategorized transactions")
                    print("2. If you want to change a category already in use")
                    sub_choice_3 = input("Enter your choice: ").strip()
                    if sub_choice_3 == "1":
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
                    elif sub_choice_3 == "2":
                        category = input("Enter the category you want to filter transactions by: ").strip()

                        # TODO: Review this part
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

            elif main_choice == "4":
                # TODO:
                # Generate filtered summary
                # Remember to datetime.strptime(date, "%Y-%m-%d")
                pass

            elif main_choice == "5":
                # TODO:
                # choose budget for each category
                pass

            elif main_choice == "6":
                # TODO:
                # View budget report
                pass

            elif main_choice == "7":
                # TODO:
                # Export summary
                pass

            elif main_choice == "8":
                print("Thank you for using CashFlow Tracker. Goodbye!")
                break

            else:
                print("Invalid choice, please check menu and choose the desired action.")
                continue
    except KeyboardInterrupt:
        print("Operation cancelled by the user, saving changes...")

        # TODO: Save cashflowtracker to a CSV file
        print("Changes saved sucessfully.")

        print("Thank you for using CashFlow Tracker. Goodbye!")
        exit(0)


def read_csv(path, date="date", description="description", value="value"):
    # Setting defaut or custom values for the fields
    date_field = date
    description_field = description
    value_field = value

    with open(path, newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        try:
            date_index = header.index(date_field)
        except ValueError:
            raise ValueError("'date' column not found in CSV file.")

        try:
            value_index = header.index(value_field)
        except ValueError:
            raise ValueError("'value' column not found in CSV file.")
        
        try:
            description_index = header.index(description_field)
        except ValueError:
            raise ValueError("'description' column not found in CSV file.")

        for row in reader:
            date = row[date_index]
            value = float(row[value_index])
            description = row[description_index]
            transaction = Transaction(date, "", description, value)
            yield transaction


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
    # TODO: Create a function to export the summary to a CSV or Excel file.
    ...


if __name__ == "__main__":
    main()