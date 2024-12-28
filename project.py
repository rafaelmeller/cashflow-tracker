import csv
import os
import re
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
from tabulate import tabulate
from typing import List, Dict, Tuple, Union


class Transaction:
    def __init__(self, date: str, category: str, description: str, value: float):
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.category = category
        self.description = description
        self.value = value


    def __str__(self):
        return f"{self.date} | {self.category} | {self.description} | ${self.value:.2f}"
    

class Budget:
    def __init__(self, category: str, amount: float, period: str):
        self.category = category
        self.amount = amount
        self.period = period


    def __str__(self):
        return f"Category: {self.category}, Amount: ${self.amount:.2f}, Period: {self.period}"
    

class Goal:
    def __init__(self, category: str, amount: float, period: str):
        self.category = category
        self.amount = amount
        self.period = period


    def __str__(self):
        return f"Category: {self.category}, Amount: ${self.amount:.2f}, Period: {self.period}"


class CashFlowTracker:
    TARGET_PERIODS = ["daily", "weekly", "monthly", "yearly"]

    def __init__(self):
        self.transactions: List[Transaction] = []
        self.budgets: Dict[str, Budget] = {}


    def add(self, transaction: Transaction) -> List[Transaction]:
        self.transactions.append(transaction)
        return self.transactions
 

    def edit(self, old_transaction: Transaction, new_transaction: Transaction) -> List[Transaction]:
        self.delete(old_transaction)
        self.add(new_transaction)
        return self.transactions
    

    def delete(self, transaction: Transaction) -> List[Transaction]:
        self.transactions.remove(transaction)
        return self.transactions


    def categorize(self, transaction: Transaction, category: str) -> List[Transaction]:
        transaction.category = category
        return self.transactions


    def filter(self, date_tuple: Tuple[datetime, datetime] = None, category: str = None, type: str = None):
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


    def set_target(self, category: str, amount: float, period: str) -> Union[Dict[str, Budget], Dict[str, Goal]]:
        if period not in self.TARGET_PERIODS:
            raise ValueError("Invalid period. Please enter a valid period.")
        
        existing_categories = set([t.category for t in self.transactions])
        if category not in existing_categories:
            raise ValueError("Category not found. Please enter a valid category.")

        # Check if the category has transactions with positive or negative values
        has_positive = any(t.value > 0 for t in self.transactions if t.category == category)
        has_negative = any(t.value < 0 for t in self.transactions if t.category == category)

        if has_positive and not has_negative:
            goal = Goal(category, amount, period)
            self.goals[category] = goal
            return self.goals
        
        elif has_negative and not has_positive:
            budget = Budget(category, amount, period)
            self.budgets[category] = budget
            return self.budgets
        else:
            raise ValueError("Category has both positive and negative transactions, please review category.")
        

    def target_report(self) -> str:
        if not self.budgets and not self.goals:
            raise ValueError("No budgets or goals set yet.")
        
        start_date = min([t.date for t in self.transactions])
        end_date = max([t.date for t in self.transactions])
        report_period = end_date - start_date
        report = []

        if report_period.days < 30:
            for budget in self.budgets.values():
                if budget.period == "daily":
                    period_budget = budget.amount * report_period.days
                elif budget.period == "weekly":
                    period_budget = budget.amount * (report_period.days / 7)
                elif budget.period == "monthly":
                    period_budget = budget.amount * (report_period.days / 30)
                elif budget.period == "yearly":
                    period_budget = budget.amount * (report_period.days / 365)
                actual = sum([abs(t.value) for t in self.transactions if t.category == budget.category])
                difference = period_budget - actual
                report.append({
                    "Period": f"From {start_date} to {end_date}",
                    "Category": budget.category,
                    "Budget": period_budget,
                    "Actual": actual,
                    "Difference": difference
                })
            report_table = [[item["Category"], item["Budget"], item["Actual"], item["Difference"]] for item in report]
            return tabulate(report_table, headers=["Category", "Budget", "Actual", "Difference"], tablefmt="grid", floatfmt=".2f")

        else:
            grouped_transactions = group_by_month(self)
            for month, transactions in grouped_transactions.items():
                for budget in self.budgets.values():
                    if budget.period == "daily":
                        period_budget = budget.amount * 30
                    elif budget.period == "weekly":
                        period_budget = budget.amount * (30 / 7)
                    elif budget.period == "monthly":
                        period_budget = budget.amount
                    elif budget.period == "yearly":
                        period_budget = budget.amount / 12
                    actual = sum([abs(t.value) for t in transactions if t.category == budget.category])
                    difference = period_budget - actual
                    report.append({
                        "Month": month,
                        "Category": budget.category,
                        "Budget": period_budget,
                        "Actual": actual,
                        "Difference": difference
                    })
            report_table = [[item["Month"], item["Category"], item["Budget"], item["Actual"], item["Difference"]] for item in report]
            return tabulate(report_table, headers=["Month", "Category", "Budget", "Actual", "Difference"], tablefmt="grid", floatfmt=".2f")
       
        
    def summary(self) -> str:
        # Calculates totals for incomes, expenses, and by category.
        start_date = min([t.date for t in self.transactions])
        end_date = max([t.date for t in self.transactions])
        period = end_date - start_date
        categories = set([t.category for t in self.transactions])
        if categories == {""}:
            total_income = sum([t.value for t in self.transactions if t.value > 0])
            total_expense = sum([t.value for t in self.transactions if t.value < 0])
            total_balance = total_income + total_expense
            average_daily_income = total_income / period.days
            average_daily_expense = total_expense / period.days
        total_income = 0
        total_expense = 0

        for category in categories:
            total_category_income = sum([t.value for t in self.transactions if t.category == category and t.value > 0])
            total_category_expense = sum([t.value for t in self.transactions if t.category == category and t.value < 0])
            total_income += total_category_income
            total_expense += total_category_expense
        
        total_balance = total_income + total_expense
        average_daily_income = total_income / period.days
        average_daily_expense = total_expense / period.days

        summary = {
            "Period": f"From {start_date} to {end_date}",
            "Duration": f"({period.days} days)",
            "Average Daily Income": f"{average_daily_income:.2f}",
            "Total Income": f"{total_income:.2f}",
            "Average Daily Expense": f"{average_daily_expense:.2f}",
            "Total Expense": f"{total_expense:.2f}",
            "Total Balance": f"{total_balance:.2f}"
        }

        summary_table = [[key, value] for key, value in summary.items()]

        return tabulate(summary_table, tablefmt="grid", floatfmt=".2f")
 

    def dataframe(self) -> pd.DataFrame:
        data = {
            "Date": [t.date for t in self.transactions],
            "Category": [t.category for t in self.transactions],
            "Description": [t.description for t in self.transactions],
            "Value": [t.value for t in self.transactions]
        }
        df = pd.DataFrame(data)
        return df


    def __str__(self) -> str:
        if not self.transactions:
            return "No transactions registered yet."
        df = self.dataframe()
        df = df.sort_values("Date")
        df["Value"] = df["Value"].apply(lambda x: f"{float(x):.2f}")

        return tabulate(df, headers="keys", tablefmt="grid", showindex=False, floatfmt=".2f")


def main(): 
    cashflowtracker = CashFlowTracker()
    filtered_cashflow = None
    print()
    print("Welcome to CashFlow Tracker!")
    try:
        while True:
            data_choice = None
            print()
            print("Menu:")
            print("1. Import transactions from CSV file")
            print("2. Add or edit a transaction manually")
            print("3. Choose a category for your transactions")
            print("4. Generate filtered cashflow table")
            print("5. Set a budget for each category")
            print("6. Create a budget report")
            print("7. View your data (complete cashflow, filtered cashflow or a summary)")  
            print("8. Export data, summary, or report to a CSV file")
            print("9. Exit")
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
                        print()
                        print("Transactions have been imported successfully.")
                        break
                    except FileNotFoundError:
                        print()
                        print("File not found. Please enter a valid path.")
                        continue
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
                                    print()
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
                                    print()
                                    value_index = int(input("Enter the number of the column to use for the value: ").strip())
                                    value = headers[value_index - 1]
                                    break
                                except ValueError:
                                    print("Invalid column number. Please enter a valid number.")
                                    continue

                            try:
                                for transaction in read_csv(path, date, description, value):
                                    cashflowtracker.add(transaction)
                                print()
                                print("Transactions have been imported successfully to your main CashFlow data.")
                            except ValueError as e:
                                print(f"Error: {e}")
                                continue
                    
            elif main_choice == "2":
                # Add new transaction manually
                object = cashflowtracker
                if filtered_cashflow:
                    print("Please choose if you want edit or add a new transaction to:")
                    print("1. Your complete cashflow data")
                    print("2. Your already filtered cashflow data")
                    while True:
                        print()
                        data_choice = input("Please type the number of your choice: ").strip()
                        if data_choice == "1":
                            object = cashflowtracker
                            break
                        elif data_choice == "2":
                            object = filtered_cashflow
                            break
                        else:
                            print("Invalid choice, please check menu and choose the desired option.")
                            continue
                print("Please choose your next action:")
                print("1. Add a new transaction")
                print("2. Edit or delete an existing transaction")
                print("3. Go back to the main menu")
                while True:
                    choice = input("Enter the number of your choice: ").strip()
                    if choice == "1":
                        print("Enter the details of the transaction:")
                        while True:
                            date = input("Date (YYYY-MM-DD): ").strip()
                            if not re.match(r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$", date):
                                print("Invalid date format. Please enter a valid date.")
                                print()
                                continue
                            break

                        while True:
                            print()
                            print("Now the category.")
                            categories = set([t.category for t in object.transactions])

                            if categories == {""}:
                                print("There are no categories being used yet.")
                                print("Type one for your transaction.")
                                category = input("Category: ").strip()
                                break
                            else:
                                print("Here is the list of the already existing categories:")
                                for category in categories:
                                    if category == "":
                                        continue
                                    print(f"- {category}")
                                print("Type a name for your transaction.")
                                category = input("Category: ").strip()
                                break  

                        while True:
                            print()
                            description = input("Description: ").strip()
                            if not description:
                                print("Description cannot be empty. Please enter a valid description.")
                                continue
                            break

                        while True:
                            print()
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
                        object.add(transaction)
                        break
                    elif choice == "2":
                        print("Please choose a way to find the transaction you want to edit:")
                        print("1. By date")
                        print("2. By category")
                        print("3. By description")
                        print("4. By value")
                        while True:
                            choice = input("Enter the number of your choice: ").strip()
                            if choice == "1":
                                while True:
                                    date = input("Enter the date of the transaction you want to edit (YYYY-MM-DD): ").strip()
                                    if not re.match(r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$", date):
                                        print("Invalid date format. Please enter a valid date.")
                                        print()
                                        continue
                                    break
                                transactions = [t for t in object.transactions if t.date == datetime.strptime(date, "%Y-%m-%d").date()]
                                if not transactions:
                                    print("No transactions found for the date entered.")
                                    continue
                                else:
                                    for index, transaction in transactions:
                                        print(f"{index + 1}. {transaction}")
                                    while True:
                                        try:
                                            choice = int(input("Enter the number of the transaction you want to edit: ").strip())
                                            if (choice - 1) < 0 or (choice - 1) > len(transactions):
                                                print("Invalid transaction number. Please enter a valid number.")
                                                print()
                                                continue
                                            break
                                        except ValueError:
                                            print("Invalid transaction number. Please enter a valid number.")
                                            continue
                                    transaction = transactions[choice - 1]
                                    print()
                                    print("Transaction found:")
                                    print(transaction)
                                # TODO: Edit transaction
                                break
                            elif choice == "2":
                                while True:
                                    print("Here is the list of the already existing categories:")
                                    categories = set([t.category for t in object.transactions])
                                    for index, category in categories:
                                        print(f"{index + 1}. {category}")
                                    try:
                                        choice = int(input("Enter the number of the category of the transaction you want to edit: ").strip())
                                        if (choice - 1) < 0 or (choice - 1) > len(transactions):
                                            print("Invalid category number. Please enter a valid number.")
                                            print()
                                            continue
                                        break
                                    except ValueError:
                                        print("Invalid category number. Please enter a valid number.")
                                        continue
                                category = categories[choice - 1]
                                transactions = [t for t in object.transactions if t.category == category]
                                for index, transaction in transactions:
                                    print(f"{index + 1}. {transaction}")
                                while True:
                                    try:
                                        choice = int(input("Enter the number of the transaction you want to edit: ").strip())
                                        if (choice - 1) < 0 or (choice - 1) > len(transactions):
                                            print("Invalid transaction number. Please enter a valid number.")
                                            print()
                                            continue
                                        break
                                    except ValueError:
                                        print("Invalid transaction number. Please enter a valid number.")
                                        continue
                                transaction = transactions[choice - 1]
                                # TODO: Edit transaction
                                break
                            elif choice == "3":
                                while True:
                                    keyword = input("Enter a keyword to search for in the description of the transaction you want to edit: ").strip()
                                    transactions = [t for t in object.transactions if keyword.lower() in t.description.lower()]
                                    if not transactions:
                                        print("No transactions found for the keyword entered.")
                                        continue
                                    else:
                                        break
                                for index, transaction in transactions:
                                    print(f"{index + 1}. {transaction}")
                                while True:
                                    try:
                                        choice = int(input("Enter the number of the transaction you want to edit: ").strip())
                                        if (choice - 1) < 0 or (choice - 1) > len(transactions):
                                            print("Invalid transaction number. Please enter a valid number.")
                                            print()
                                            continue
                                        break
                                    except ValueError:
                                        print("Invalid transaction number. Please enter a valid number.")
                                        continue
                                transaction = transactions[choice - 1]
                                # TODO: Edit transaction
                                break       
                            elif choice == "4":
                                while True:
                                    try:
                                        value = float(input("Enter the value of the transaction you want to edit: ").strip())
                                        transactions = [t for t in object.transactions if t.value == value]
                                        if not transactions:
                                            print("No transactions found for the value entered.")
                                            continue
                                        else:
                                            break
                                    except ValueError:
                                        print("Invalid value. Please enter a valid value.")
                                        continue
                                for index, transaction in transactions:
                                    print(f"{index + 1}. {transaction}")
                                while True:
                                    try:
                                        choice = int(input("Enter the number of the transaction you want to edit: ").strip())
                                        if (choice - 1) < 0 or (choice - 1) > len(transactions):
                                            print("Invalid transaction number. Please enter a valid number.")
                                            print()
                                            continue
                                        break
                                    except ValueError:
                                        print("Invalid transaction number. Please enter a valid number.")
                                        continue
                                transaction = transactions[choice - 1]
                                # TODO: Edit transaction
                                break
                            else:
                                print("Invalid choice. Please check menu and choose the desired action.")
                                continue       
                    elif choice == "3":
                        break
                    else:
                        print("Invalid choice, please check menu and choose the desired action.")
                        continue
                if data_choice == "1":
                    cashflowtracker = object    
                elif data_choice == "2":
                    filtered_cashflow = object
                elif not data_choice:
                    cashflowtracker = object
                data_choice = None
                                      
            elif main_choice == "3":
                # Choose category of transactions
                object = cashflowtracker
                if filtered_cashflow:
                    print()
                    print("Please choose if you want to change transaction categories of:")
                    print("1. Your complete cashflow data")
                    print("2. Your already filtered cashflow data")
                    while True:
                        data_choice = input("Please type the number of your choice: ").strip()
                        if data_choice == "1":
                            object = cashflowtracker
                            break
                        elif data_choice == "2":
                            object = filtered_cashflow
                            break
                        else:
                            print("Invalid choice, please check menu and choose the desired option.")
                            continue

                while True:
                    print()
                    print("Choose an option:")
                    print("1. If you want to categorize uncategorized transactions")
                    print("2. If you want to change a category already in use")
                    choice = input("Enter your choice: ").strip()
                    if choice == "1":
                        grouped_uncategorized = group_uncategorized(object)
                        for description, transactions in grouped_uncategorized.items():
                            print()
                            print(f"Transactions with description: {description}")
                            for transaction in transactions:
                                print(transaction)
                            category = input("Enter the category for the above transactions: ").strip()
                            for transaction in transactions:
                                object.categorize(transaction, category)
                            print(f"All transactions with description '{description}' have been categorized as '{category}'.")
                        if data_choice == "1":
                            cashflowtracker = object
                        elif data_choice == "2":
                            filtered_cashflow = object
                        elif not data_choice:
                            cashflowtracker = object
                        data_choice = None
                        break

                    elif choice == "2":
                        object = cashflowtracker
                        if filtered_cashflow:
                            print()
                            print("Please choose if you want to change transaction categories of:")
                            print("1. Your complete cashflow data")
                            print("2. Your already filtered cashflow data")
                            while True:
                                data_choice = input("Please type the number of your choice: ").strip()
                                if data_choice == "1":
                                    object = cashflowtracker
                                    break
                                elif data_choice == "2":
                                    object = filtered_cashflow
                                    break
                                else:
                                    print("Invalid choice, please check menu and choose the desired option.")
                                    continue
                        category = input("Enter the category you want to filter transactions by: ").strip()
                        temporary_filtered = object.filter(category=category)
                        if not temporary_filtered.transactions:
                            print(f"No transactions found for category '{category}'.")
                            continue     
                        else:
                            print(f"Transactions with category '{category}':")
                            for transaction in temporary_filtered.transactions:
                                print(transaction)
                            new_category = input("Enter the new category for the transactions above: ").strip()
                            for transaction in temporary_filtered.transactions:
                                object.categorize(transaction, new_category)
                            print(f"All transactions that had previously the category '{category}' have been categorized as '{new_category}'.")
                            if data_choice == "1":
                                cashflowtracker = object
                            elif data_choice == "2":
                                filtered_cashflow = object
                            elif not data_choice:
                                cashflowtracker = object
                            data_choice = None
                            break
                    else:
                        print("Invalid choice, please check menu and choose the desired action.")
                        continue

            elif main_choice == "4":
                # Generate filtered list of transactions
                if filtered_cashflow:
                    print()
                    print("Important: If you make a new filtered cashflow, your last one will be lost.")
                    print("Please choose an option: ")
                    print("1. Export your filtered cashflow before starting the new one")
                    print("2. Start a new filtered cashflow without saving the last one")
                    while True:
                        data_choice = input("Enter the number of your choice: ").strip()
                        if data_choice == "1":
                            print("Exporting the filtered cashflow...")
                            export_data(filtered_cashflow, "filtered_cashflow")
                            print("Filtered cashflow exported successfully.")
                            filtered_cashflow = None
                            break
                        elif data_choice == "2":
                            filtered_cashflow = None
                            break
                        else:
                            print("Invalid choice. Please choose a valid option.")
                            continue
                main_bool = []
                while not main_bool == ["date", "category", "type"]:
                    print("Now please choose the filtering parameters for your filtered cashflow:")
                    while "date" not in main_bool:
                        print()
                        date_bool = input("Do you want to filter by date range (y/n)? ").strip().lower()
                        if date_bool == "y":

                            while True:
                                start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
                                if not re.match(r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$", start_date):
                                    print("Invalid date format. Please enter a valid date.")
                                    continue
                                else:
                                    break

                            while True:
                                end_date = input("Enter the end date (YYYY-MM-DD): ").strip()
                                if not re.match(r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$", end_date):
                                    print("Invalid date format. Please enter a valid date.")
                                    continue
                                else:
                                    break
                            date_filter = (datetime.strptime(start_date, "%Y-%m-%d").date(), datetime.strptime(end_date, "%Y-%m-%d").date())
                            main_bool.append("date")
                        elif date_bool == "n":
                            date_filter = None
                            main_bool.append("date")
                        else:
                            print("Invalid choice. Please choose the desired action.")
                            continue

                    while "category" not in main_bool:
                        print()
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
                                try:
                                    print()
                                    category_index = int(input("Enter the number of the category you want to filter by: ").strip())
                                    if (category_index - 1) <= 0 or (category_index - 1) > len(categories):
                                        print("Invalid category number. Please enter a valid number.")
                                        print()
                                        continue
                                    else:
                                        category_filter = categories[category_index - 1]
                                        main_bool.append("category")
                                        break
                                except ValueError:
                                    print("Invalid category number. Please enter a valid number.")
                                    continue
                        elif category_bool == "n":
                            category_filter = None
                            main_bool.append("category")
                        else:
                            print("Invalid choice. Please choose the desired action.")
                            continue

                    while "type" not in main_bool:
                        print()
                        type_bool = input("Do you want to filter by type (income or expense) (y/n)? ").strip().lower()
                        if type_bool == "y":
                            while True:
                                type_filter = input("Enter the type of transaction you want to filter by (income or expense): ").strip().lower()
                                if type_filter not in ["income", "expense"]:
                                    print("Invalid type. Please enter a valid type ('income' or 'expense').")
                                    continue
                                else:
                                    main_bool.append("type")
                                    break
                        elif type_bool == "n":
                            type_filter = None
                            main_bool.append("type")
                            break
                        else:
                            print("Invalid choice. Please choose the desired action.")
                            continue

                filtered_cashflow = cashflowtracker.filter(date_filter, category_filter, type_filter)
                print()
                print("Your filtered cashflow date is ready")
                while True:
                    print()
                    print("Please choose an option:")
                    print("1. View a table of it")
                    print("2. View a summary of it")
                    print("3. Export it to a CSV file")
                    print("4. Go back to the main menu")
                    choice = input("Enter your choice: ").strip()
                    if choice == "1":
                        print(filtered_cashflow)
                        continue
                    elif choice == "2":
                        print(filtered_cashflow.summary())
                        continue
                    elif choice == "3":
                        while True:
                            try:
                                name = input("Please choose a file name: ").strip()
                                message = export_data(filtered_cashflow, name)
                                print()
                                print(f"{message}")
                                break
                            except ValueError as e:
                                print()
                                print(f"Error: {e}")
                                continue
                    elif choice == "4":
                        break
                    else:
                        print("Invalid choice, please check menu and choose the desired action.")
                        continue


            elif main_choice == "5":
                # Set budget for each category
                object = cashflowtracker
                if filtered_cashflow:
                    print()
                    print("Please choose if you want to set budgets to:")
                    print("1. Your main cashflow data")
                    print("2. Your already filtered cashflow data")
                    while True:
                        data_choice = input("Please type the number of your choice: ").strip()
                        if data_choice == "1":
                            object = cashflowtracker
                            break
                        elif data_choice == "2":
                            object = filtered_cashflow
                            break
                        else:
                            print("Invalid choice, please check menu and choose the desired option.")
                            continue

                categories = set([t.category for t in object.transactions])
                if not object.transactions:
                    print("There are no transactions registered yet.")
                    print("Please add transactions before setting a budget.")
                    continue
                elif categories == {""}:
                    print("There are no categories being used yet.")
                    print("Please categorize your transactions before setting a budget.")
                    continue
                else:
                    while True:
                        categories_with_budget = [category for category in categories if category in object.budgets]
                        categories_without_budget = [category for category in categories if category not in object.budgets]
                        print()
                        print("Choose an option:")
                        print("1. See all the budgets already set")
                        print("2. Set a budget for a category with no budget yet")
                        print("3. Exit to the main menu")
                        choice = input("Type the number of your option: ")
                        if choice == "1":
                            print()
                            if categories_with_budget:
                                for index, category in enumerate(categories_with_budget, start=1):
                                    print(f"{index}. {category}")
                                while True:
                                    print("Please choose an option:")
                                    print("1. Change an existing budget")
                                    print("2. Go back to budget menu")
                                    while True:
                                        choice = input("Please type the number of the desired option: ")
                                        if choice == "1":
                                            while True:
                                                try:
                                                    print()
                                                    choice = int(input("Choose the number of the category to set a budget for: ").strip())
                                                    if (choice - 1) < 0 or (choice - 1) > len(categories_with_budget):
                                                        print("Invalid category number. Please enter a valid number.")
                                                        print()
                                                        continue
                                                    break
                                                except ValueError:
                                                    print("Invalid category number. Please enter a valid number.")
                                                    continue
                                            category = categories_with_budget[choice - 1]
                                            print("What is the period for this budget?")
                                            for index, period in enumerate(CashFlowTracker.TARGET_PERIODS, start=1):
                                                print(f"{index}. {period}")
                                            while True:
                                                choice = input("Enter number correspondent to the desired period: ").strip().lower()
                                                if choice not in ["1", "2", "3", "4"]:
                                                    print("Invalid period. Please enter a valid period.")
                                                    continue
                                                break
                                            period = CashFlowTracker.TARGET_PERIODS[int(choice) - 1]
                                            while True:
                                                try:
                                                    amount = float(input("Enter the budget amount: ").strip())
                                                    if amount < 0:
                                                        print("Invalid amount. Please enter a valid amount.")
                                                        continue
                                                    break
                                                except ValueError:
                                                    print("Invalid amount. Please enter a valid amount.")
                                                    continue
                                            object.set_target(category, amount, period)
                                            print(f"Budget of ${amount:.2f} set for '{category}' in a {period} period.")

                                        elif choice == "2":
                                            break
                                        else:
                                            print("Invalid choice, please check menu and choose the desired option.")
                                            continue
                            else:
                                print("No budgets set yet.")
                                continue
                        elif choice == "2":
                            print("Here is the list of the categories with no budget:")
                            for index, category in enumerate(categories_without_budget, start=1):
                                print(f"{index}. {category}")
                            while True:
                                try:
                                    print()
                                    choice = int(input("Choose the number of the category to set a budget for: ").strip())
                                    if (choice - 1) < 0 or (choice - 1) > len(categories_without_budget):
                                        print("Invalid category number. Please enter a valid number.")
                                        print()
                                        continue
                                    break
                                except ValueError:
                                    print("Invalid category number. Please enter a valid number.")
                                    continue
                            category = categories_without_budget[choice - 1]
                            print("What is the period for this budget?")
                            for index, period in enumerate(CashFlowTracker.TARGET_PERIODS, start=1):
                                print(f"{index}. {period}")
                            while True:
                                choice = input("Enter number correspondent to the desired period: ").strip().lower()
                                if choice not in ["1", "2", "3", "4"]:
                                    print("Invalid period. Please enter a valid period.")
                                    continue
                                break
                            period = CashFlowTracker.TARGET_PERIODS[int(choice) - 1]
                            while True:
                                try:
                                    amount = float(input("Enter the budget amount: ").strip())
                                    if amount < 0:
                                        print("Invalid amount. Please enter a valid amount.")
                                        continue
                                    break
                                except ValueError:
                                    print("Invalid amount. Please enter a valid amount.")
                                    continue
                            object.set_target(category, amount, period)
                            print(f"Budget of ${amount:.2f} set for '{category}' in a {period} period.")  
                        elif choice == "3":
                            break
                        else:
                            print("Invalid choice, please check menu and choose the desired option.")
                            continue
                    if data_choice == "1":
                        cashflowtracker = object
                    elif data_choice == "2":
                        filtered_cashflow = object
                    elif not data_choice:
                            cashflowtracker = object
                    data_choice = None

            elif main_choice == "6":
                # Create a budget report
                print()
                print("Do you want to generate a budget report for:")
                print("1. Your complete cashflow data")
                print("2. Your last filtered cashflow data")
                while True:
                    choice = input("Enter the number of your choice: ").strip()
                    if choice == "1":
                        try:
                            print(cashflowtracker.target_report())
                        except ValueError as e:
                            print(f"Error: {e}")
                            print()
                        break
                    elif choice == "2":
                        try:
                            print(filtered_cashflow.target_report())
                        except ValueError as e:
                            print(f"Error: {e}")
                        break
                    else:
                        print("Invalid choice, please check menu and choose the desired action.")
                        continue

            elif main_choice == "7":
                # View your data (complete cashflow, filtered cashflow or a summary)
                while True:
                    print()
                    print("Choose a data to view:")
                    print("1. Complete cashflow data")
                    print("2. Your last filtered cashflow data")
                    print("3. Summary of your data")
                    print("4. Go back to the main menu")
                    choice = input("Enter your choice: ").strip()
                    if choice == "1":
                        print(cashflowtracker)
                        continue
                    elif choice == "2":
                        if filtered_cashflow:
                            print(filtered_cashflow)
                            continue
                        else:
                            print("No filtered cashflow data available.")
                            continue
                    elif choice == "3":
                        object = cashflowtracker
                        if filtered_cashflow:
                            print()
                            print("Please choose if you want to get summary for:")
                            print("1. Your main cashflow data")
                            print("2. Your already filtered cashflow data")
                            while True:
                                data_choice = input("Please type the number of your choice: ").strip()
                                if data_choice == "1":
                                    object = cashflowtracker
                                    break
                                elif data_choice == "2":
                                    object = filtered_cashflow
                                    break
                                else:
                                    print("Invalid choice, please check menu and choose the desired option.")
                                    continue
                        print(object.summary())
                        continue
                    elif choice == "4":
                        break
                    else:
                        print("Invalid choice, please check menu and choose the desired action.")
                        continue
                    
            elif main_choice == "8":
                # Export data, summary, or report to a CSV file
                print()
                print("Please choose which data you wish to export:")
                print("1. Your complete cashflow data")
                print("2. Your filtered cashflow data")
                print("3. A summary of your data")
                print("4. A budget report")
                print("5. Go back to the main menu")
                while True:
                    choice = input("Enter the number of your choice: ").strip()
                    if choice == "1":
                        while True:
                            try:
                                name = input("Please choose a file name: ").strip()
                                message = export_data(cashflowtracker, name)
                                print(f"{message}")
                                break
                            except ValueError as e:
                                print(f"Error: {e}")
                                continue
                    elif choice == "2":
                        if not filtered_cashflow:
                            print("No filtered cashflow data available.")
                            continue
                        while True:
                            try:
                                name = input("Please choose a file name: ").strip()
                                message = export_data(filtered_cashflow, name)
                                print(f"{message}")
                                break
                            except ValueError as e:
                                print(f"Error: {e}")
                                continue
                        continue
                    elif choice == "3":
                        object = cashflowtracker
                        if filtered_cashflow:
                            print("Please choose if you want to export a budget report of:")
                            print("1. Your main cashflow data")
                            print("2. Your already filtered cashflow data")
                            while True:
                                data_choice = input("Please type the number of your choice: ").strip()
                                if data_choice == "1":
                                    object = cashflowtracker
                                    break
                                elif data_choice == "2":
                                    object = filtered_cashflow
                                    break
                                else:
                                    print("Invalid choice, please check menu and choose the desired option.")
                                    continue
                        while True:
                            try:
                                name = input("Please choose a file name: ").strip()
                                message = export_data(object.target_report(), name)
                                print(f"{message}")
                                data_choice = None
                                break
                            except ValueError as e:
                                print(f"Error: {e}")
                                continue
                        continue
                    elif choice == "4":
                        object = cashflowtracker
                        if filtered_cashflow:
                            print("Please choose if you want to export a summary of:")
                            print("1. Your main cashflow data")
                            print("2. Your already filtered cashflow data")
                            while True:
                                data_choice = input("Please type the number of your choice: ").strip()
                                if data_choice == "1":
                                    object = cashflowtracker
                                    break
                                elif data_choice == "2":
                                    object = filtered_cashflow
                                    break
                                else:
                                    print("Invalid choice, please check menu and choose the desired option.")
                                    continue
                        while True:
                            try:
                                name = input("Please choose a file name: ").strip()
                                message = export_data(object.summary(), name)
                                print(f"{message}")
                                data_choice = None
                                break
                            except ValueError as e:
                                print(f"Error: {e}")
                                continue
                        continue
                    elif choice == "5":
                        break
                    else:
                        print("Invalid choice, please check menu and choose the desired action.")
                        continue            

            elif main_choice == "9":
                print()
                print("Thank you for using CashFlow Tracker. Goodbye!")
                break

            else:
                print("Invalid choice, please check menu and choose the desired action.")
                continue
    except KeyboardInterrupt:
        print()
        print("\nOperation cancelled by the user, saving changes...")
        print()
        if cashflowtracker.transactions:
            message = export_data(cashflowtracker)
            print(f"{message}")
        if filtered_cashflow:
            message = export_data(filtered_cashflow, "filtered_cashflow")
            print(f"{message}")
        print()
        print("Thank you for using CashFlow Tracker. Goodbye!")
        print()
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

        date_list = []
        for _ in range(30):
            try:
                date_list.append(next(reader)[date_index])
            except StopIteration:
                break

        date_format = check_date_format(date_list)

        if date_format is None:
            raise ValueError("'date' format couldn't be identified.")
        
        file.seek(0)
        next(reader)

        for row in reader:
            date_str = row[date_index]
            try:
                if date_format == "dayfirst":
                    date = parse(date_str, dayfirst=True).strftime("%Y-%m-%d")
                else:
                    date = parse(date_str, dayfirst=False).strftime("%Y-%m-%d")
            except ValueError:
                raise ValueError("'date' format should be one of the following: 'YYYY-MM-DD', 'MM-DD-YYYY', 'DD-MM-YYYY'")

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


def group_by_month(object):
    # Group transactions by month
    transactions = object.transactions
    grouped_transactions = {}
    for transaction in transactions:
        month = transaction.date.strftime("%B %Y")
        if month not in grouped_transactions:
            grouped_transactions[month] = []
        grouped_transactions[month].append(transaction)
    
    return grouped_transactions


def check_date_format(date_list):
    patterns = {
        "yearfirst": r"^\d{4}[-/](0[1-9]|1[012])[-/](0[1-9]|[12][0-9]|3[01])$",
        "monthfirst": r"^(0[1-9]|1[012])[-/](0[1-9]|[12][0-9]|3[01])[-/]\d{4}$",
        "dayfirst": r"^(0[1-9]|[12][0-9]|3[01])[-/](0[1-9]|1[012])[-/]\d{4}$"
    }

    matching_patterns = []

    for key, pattern in patterns.items():
        if all(re.match(pattern, date) for date in date_list):
            matching_patterns.append(key)

    if len(matching_patterns) == 1:
        return matching_patterns[0]
    else:
        return None


def export_data(data, name="cashflowtracker"):
    if name.endswith(".csv"):
        name = name.rstrip(".csv")

    if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9_\-()]*$", name):
        raise ValueError("Invalid file name. Please choose a name that contains only alphanumeric characters, underscores, or hyphens.")

    base_name = name
    counter = 1
    while os.path.exists(f"{name}.csv"):
        name = f"{base_name}({counter})"
        counter += 1

    if isinstance(data, CashFlowTracker):
        df = data.dataframe()
        df["Value"] = df["Value"].apply(lambda x: f"{x:.2f}")
        df.to_csv(f"{name}.csv", index=False)
    elif isinstance(data, str):
        with open(f"{name}.csv", "w") as file:
            file.write(data)
    elif isinstance(data, pd.DataFrame):
        data["Value"] = data["Value"].apply(lambda x: f"{x:.2f}")
        data.to_csv(f"{name}.csv", index=False)
    else:
        raise ValueError("Invalid data type. Please enter a valid data type.")
    
    message = f"{name}.csv exported successfully."
    return message


if __name__ == "__main__":
    main()