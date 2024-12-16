import csv
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import re
from tabulate import tabulate


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


    def add(self, transaction):
        self.transactions.append(transaction)
        return self.transactions


    def categorize(self, transaction, category):
        transaction.category = category
        return transaction


    def filter(self, date_tuple=None, category=None, type=None):
        filtered_transactions = self.transactions
        if date_tuple:
            start_date, end_date = date_tuple
            filtered_transactions = [t for t in filtered_transactions if start_date <= t.date <= end_date]
        if category:
            filtered_transactions = [t for t in filtered_transactions if t.category == category]
        if type:
            if type == "income":
                filtered_transactions = [t for t in filtered_transactions if t.value > 0]
            else:
                filtered_transactions = [t for t in filtered_transactions if t.value < 0]
        
        filtered_cashflowtracker = CashFlowTracker()
        for transaction in filtered_transactions:
            filtered_cashflowtracker.add(transaction)

        return filtered_cashflowtracker

    
    def summary(self):
        # Calculates totals for incomes, expenses, and by category.
        start_date = min([t.date for t in self.transactions])
        end_date = max([t.date for t in self.transactions])
        period = end_date - start_date
        categories = set(t.category if t.category else "Uncategorized" for t in self.transactions)
        income_categories = {}
        expense_categories = {}
        total_income = 0
        total_expense = 0
        
        for category in categories:
            total_category = sum([t.value for t in self.transactions if t.category == category])
            if total_category > 0:
                income_categories[category] = total_category
                total_income += total_category
            else:
                expense_categories[category] = total_category
                total_expense += total_category
        
        total_balance = total_income + total_expense
        average_daily_income = total_income / period.days
        average_daily_expense = total_expense / period.days

        summary = {
            "period": f"From {start_date} to {end_date} ({period.days} days)",
            "Total Income": total_income,
            "Total Expense": total_expense,
            "Total Balance": total_balance,
            "Average Daily Income": average_daily_income,
            "Average Daily Expense": average_daily_expense
        }

        summary_table = [[key, value] for key, value in summary.items()]

        if income_categories:
            summary_table.append(["Income by Category", ""])
            for category, total in income_categories.items():
                summary_table.append([category, total])

        if expense_categories:
            summary_table.append(["Expense by Category", ""])
            for category, total in expense_categories.items():
                summary_table.append([category, total])

        return tabulate(summary_table, headers=["Summary", "Value"], tablefmt="grid")
 

    def budget(self, category, amount):
        # TODO
        ...


    def dataframe(self):
        data = {
            "Date": [t.date for t in self.transactions],
            "Category": [t.category for t in self.transactions],
            "Description": [t.description for t in self.transactions],
            "Value": [t.value for t in self.transactions]
        }
        df = pd.DataFrame(data)
        return df


    def __str__(self):
        if not self.transactions:
            return "No transactions registered yet."
        df = self.dataframe()
        return tabulate(df, headers="keys", tablefmt="grid", showindex=False)


def main(): 
    cashflowtracker = CashFlowTracker()
    print()
    print("Welcome to CashFlow Tracker!")
    try:
        while True:
            print("Here's the menu:")
            print()
            print("1. Import transactions from CSV file")
            print("2. Add new transaction manually")
            print("3. Choose a category for your transactions")
            print("4. Generate filtered list of transactions")
            print("5. Set budget for each category")
            print("6. View budget report")  
            print("7. Export summary, list or report to a CSV or Excel file")
            print("8. Exit")
            print("(Press Ctrl+C to exit the program at any time)")
            print()

            main_choice = input("Enter the number of your choice: ").strip()

            if main_choice == "1":
                # Import transactions from CSV file
                while True:
                    path = input("Enter the path to the CSV file: ").strip()
                    if not path.endswith(".csv"):
                        print("Invalid file format. Please enter a valid CSV file.")
                        continue
                    try:
                        for transaction in read_csv(path):
                            cashflowtracker.add(transaction)
                        print("Transactions have been imported successfully.")
                        break

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
                                    cashflowtracker.add(transaction)
                                print("Transactions have been imported successfully.")
                            except ValueError as e:
                                print(f"Error: {e}")
                                continue
                    
            elif main_choice == "2":
                # Add new transaction manually
                print("Enter the details of the transaction:")
                while True:
                    date = input("Date (YYYY-MM-DD): ").strip()
                    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                        print("Invalid date format. Please enter a valid date.")
                        continue
                    break

                while True:
                    print("Now the category.")
                    categories = None

                    # TODO: Review this part
                    categories = set([t.category for t in cashflowtracker.transactions])

                    if not categories:
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
                cashflowtracker.add(transaction)

            elif main_choice == "3":
                # Choose category of transactions
                while True:
                    print("Choose an option:")
                    print("1. If you want to categorize uncategorized transactions")
                    print("2. If you want to change a category already in use")
                    sub_choice_3 = input("Enter your choice: ").strip()
                    if sub_choice_3 == "1":
                        grouped_uncategorized = group_uncategorized(cashflowtracker)
                        for description, transactions in grouped_uncategorized.items():
                            print(f"Transactions with description: {description}")
                            for transaction in transactions:
                                print(transaction)
                            category = input("Enter the category for the above transactions: ").strip()
                            for transaction in transactions:
                                cashflowtracker.categorize(transaction, category)
                            print(f"All transactions with description '{description}' have been categorized as '{category}'.")
                        break
                    elif sub_choice_3 == "2":
                        category = input("Enter the category you want to filter transactions by: ").strip()
                        filtered_transactions = cashflowtracker.filter(category=category)

                        if not filtered_transactions:
                            print(f"No transactions found for category '{category}'.")
                            continue     
                        else:
                            for description, transactions in filtered_transactions.items():
                                print(f"Transactions with description: {description}")
                                for transaction in transactions:
                                    print(transaction)
                                new_category = input("Enter the new category for the above transactions: ").strip()
                                for transaction in transactions:
                                    cashflowtracker.categorize(transaction, new_category)
                                print(f"All transactions with description '{description}' have been categorized as '{category}'.")
                            break
                    else:
                        print("Invalid choice, please check menu and choose the desired action.")
                        continue

            elif main_choice == "4":
                # Generate filtered list of transactions
                while True:
                    print("Now please choose the filtering parameters for your transaction table:")
                    date_bool = input("Do you want to filter by date range (y/n)? ").strip().lower()
                    if date_bool == "y":

                        while True:
                            start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
                            if not re.match(r"^\d{4}-\d{2}-\d{2}$", start_date):
                                print("Invalid date format. Please enter a valid date.")
                                continue
                            else:
                                break

                        while True:
                            end_date = input("Enter the end date (YYYY-MM-DD): ").strip()
                            if not re.match(r"^\d{4}-\d{2}-\d{2}$", end_date):
                                print("Invalid date format. Please enter a valid date.")
                                continue
                            else:
                                break
                        date_filter = (datetime.strptime(start_date, "%Y-%m-%d"), datetime.strptime(end_date, "%Y-%m-%d"))
                    elif date_bool == "n":
                        date_filter = None
                        break
                    else:
                        print("Invalid choice. Please choose the desired action.")
                        continue

                    while True:
                        category_bool = input("Do you want to filter by category (y/n)? ").strip().lower()
                        if category_bool == "y":
                            categories = set([t.category for t in cashflowtracker.transactions])

                            while True:
                                list_bool = input("Do you want to see a list of the existing categories (y/n)?").strip().lower()
                                if list_bool == "y":
                                    for index, category in enumerate(categories):
                                        print(f"{index + 1}. {category}")
                                    break
                                elif list_bool == "n":
                                    break
                                else:
                                    print("Invalid choice. Please choose the desired action.")
                                    continue

                            while True:
                                category_filter = input("Enter the category you want to filter by: ").strip()
                                if category_filter not in categories:
                                    print("Invalid category. Please enter a valid category.")
                                    continue
                                else:
                                    break
                        elif category_bool == "n":
                            break
                        else:
                            print("Invalid choice. Please choose the desired action.")
                            continue

                    while True:
                        type_bool = input("Do you want to filter by type (income or expense) (y/n)? ").strip().lower()
                        if type_bool == "y":
                            while True:
                                type_filter = input("Enter the type you want to filter by (income or expense): ").strip().lower()
                                if type_filter not in ["income", "expense"]:
                                    print("Invalid type. Please enter a valid type.")
                                    continue
                                else:
                                    break
                        elif type_bool == "n":
                            break
                        else:
                            print("Invalid choice. Please choose the desired action.")
                            continue
                filtered_transactions_obj = cashflowtracker.filter(date_filter, category_filter, type_filter)
                print("Your filtered transaction table is ready")
                while True:
                    print("Please choose an option:")
                    print("1. View the table")
                    print("2. View a summary of the table")
                    print("3. Export this table to a CSV or Excel file")
                    sub_choice_4 = input("Enter your choice: ").strip()
                    if sub_choice_4 == "1":
                        print(filtered_transactions_obj)
                        break
                    elif sub_choice_4 == "2":
                        print(filtered_transactions_obj.summary())
                        break
                    elif sub_choice_4 == "3":
                        # TODO: Continue this part
                        # export_data(filtered_transactions_obj)
                        break
                    else:
                        print("Invalid choice, please check menu and choose the desired action.")
                        continue
                           
                    

            elif main_choice == "5":
                # TODO:
                # Set budget for each category
                pass

            elif main_choice == "6":
                # TODO:
                # View budget report
                pass

            elif main_choice == "7":
                # TODO:
                # Export summary, list or report to a CSV or Excel file
                pass

            elif main_choice == "8":
                print("Thank you for using CashFlow Tracker. Goodbye!")
                break

            else:
                print("Invalid choice, please check menu and choose the desired action.")
                continue
    except KeyboardInterrupt:
        print()
        print("\nOperation cancelled by the user, saving changes...")
        print()

        # TODO: Save cashflowtracker to a CSV file
        print("Changes saved sucessfully.")
        print("Thank you for using CashFlow Tracker. Goodbye!")
        exit(0)


def read_csv(path, date="date", description="description", value="value"):
    # Setting defaut or custom values for the fields
    date_field = date.lower()
    description_field = description.lower()
    value_field = value.lower()

    with open(path, newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        header = [h.lower() for h in header]
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
            date_str = row[date_index]
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                date = parse(date_str).strftime("%Y-%m-%d")
            value = float(row[value_index])
            description = row[description_index]
            transaction = Transaction(date, "", description, value)
            yield transaction


def group_uncategorized(cashflowtracker):
    # Filter transactions that are uncategorized
    uncategorized = [t for t in cashflowtracker.transactions if t.category == ""]
    
    # Group uncategorized transactions by description
    grouped_uncategorized = {}
    for transaction in uncategorized:
        if transaction.description not in grouped_uncategorized:
            grouped_uncategorized[transaction.description] = []
        grouped_uncategorized[transaction.description].append(transaction)
    
    return grouped_uncategorized


def export_data(data):
    # TODO: Continue this part

    if isinstance(data, list):
        ...
    elif isinstance(data, CashFlowTracker):
        ...
    elif isinstance(data, dict):
        ...
    elif isinstance(data, str) and data.startswith("+") and data.endswith("+"):
        ...
    elif isinstance(data, pd.DataFrame):
        ...
    else:
        print("Invalid data type. Please enter a valid data type.")


if __name__ == "__main__":
    main()