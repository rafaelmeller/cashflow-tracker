<h1 align="center" style="font-weight: bold;">Cashflow Tracker Project</h1>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge" alt="Python Badge">
</div>

<div align="center">
  <img src="https://img.shields.io/badge/pytest-tested-brightgreen" alt="Pytest: tested">
</div>

<h4 align="center"> 
     <b>Status:</b> Completed
</h4>

<p align="center">
 <a href="#about-ℹ️">About</a> •
 <a href="#objectives-🎯">Objectives</a> •
 <a href="#features-🌟">Features</a> • 
 <a href="#project-demo-🖥️">Project Demo</a> •
 <a href="#workflow-🔄">Workflow</a> •
 <a href="#architecture-🏗️">Architecture</a> •
 <a href="#setup-⚙️">Setup</a> • 
<a href="#possible-improvements-and-known-limitations-📈">Possible Improvements And Known Limitations</a> •
 <a href="#author-👨🏻‍💻">Author</a> • 
 <a href="#license-📝">License</a>
</p>


###### _Other versions:_ [_Clique aqui para Português_](./README-ptBR.md)

## About ℹ️

This project was created as the final assignment for CS50P, Harvard's Introduction to Programming with Python. It is a CLI application that allows users to import bank extracts in CSV format and work with the data by filtering transactions, generating summaries, and creating budget and goal reports for specific periods. 

The application is designed with a modular approach, separating user interaction, data processing, and reporting functions to ensure clarity and maintainability.

Due to CS50P's requirements for final projects, this application couldn't be fully Object-Oriented (as at least three standalone functions were required for testing). 

The design balances these requirements by:
- Creating testable **I/O and helper functions** to support features like data validation and file management.
- Using **UI helper functions** to streamline the `main()` function, making it shorter, clearer, and less repetitive.


#
## Objectives 🎯

This application was developed to enhance the author's understanding of key Python concepts, including:
- **Classes**: Implementing custom data structures like `Transaction` and `CashFlowTracker`.
- **File Handling**: Managing CSV imports and exports.
- **Regular Expressions**: Validating and processing user inputs.
- **Unit Testing**: Writing and executing tests using Pytest.

#
## Features 🌟

- **CSV file importation**: Import transactions from a CSV file containing income and expense data.
- **Manual Transaction Input**: Add transactions directly via the CLI.
- **Edit and Delete Transactions**: Modify or remove existing transactions.
- **Categorization**: Group and edit categories based on transaction descriptions.
- **Budget and Goal Tracking**: Set spending limits (budgets) and income targets (goals) for categories, with progress tracking.
- **Reports and Exporting**: Generate summaries, budget/goal reports, or filtered datasets and save them as CSV or TXT files.



#
## Project Demo 🖥️
[Click here to watch the recorded demo](https://youtu.be/086DNvuLR84)

#
## Workflow 🔄 

1. **Import Transactions**: 
   - Upload a `.csv` file containing transaction data.
   - Check if the file matches the required format: `date, category, description, value`. If not, point the columns to be used for each field.

2. **Add or Edit Transactions**:
   - Manually add new transactions or edit existing ones through the menu.

3. **Categorize**:
   - Define categories for each transactions, by grouping by description if needed, so that the budgets and goals for each category can be set.

4. **Set Budgets and Goals**:
   - Define spending limits (budgets) or income targets (goals) for specific categories.

5. **Generate Reports**:
   - View summaries of income and expenses by category or period.
   - Export reports as `.csv` or `.txt` files for record-keeping.

#
## Architecture 🏗️

1. **Class Usage**:  
   - `Transaction`: Represents an individual transaction with attributes such as date, type (income/expense), category, description, and value.
   - `Budget` and `Goal`: Track financial targets for specific categories.
   - `CashFlowTracker`: Manages the transactions, budgets, and goals while offering methods for filtering, reporting, and categorizing data.
   
2. **I/O Functions**:  
   - **File Handling**: Functions like `read_csv()` and `export_data()` allow importing and exporting financial data.
   - **Validation**: Input validation ensures compatibility with expected formats.

3. **UI Functions**:  
   - Modular functions such as `get_valid_date()` and `choose_data_set()` streamline user interaction and prevent redundant code in the `main()` function.

4. **Main Function**:  
   - Implements a CLI-based workflow that guides the user through the program's features, including data import, transaction management, reporting, and export.

#
## Setup ⚙️

```bash
# Clone the repository
git clone <repository-url>

# Navigate to the project directory
cd <project-directory>

# Create a virtual environment (ensure Python is already installed on your machine)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Run the application
python3 project.py
```
##### _**Observation:**_ _Remember that in order to work with any .csv file, you need to have it in the same directory of project.py_

#
## Possible Improvements and Known Limitations 📈

- **Create unique identifiers for each transaction:**
Unique identifiers would be useful to facilitate transaction editing, increase control, and reduce the likelihood of duplication.

- **Include Excel files:**
Extend file handling to support `.xlsx` files for better compatibility with commonly used spreadsheet formats, possibly adding graphic analysis to the summaries and reports.

- **Add PDF Reports:**
Generate detailed PDF summaries for more professional outputs.

- **Expand Tests:**
Add tests for class methods and edge cases to improve reliability.

- **Performance Optimization and Scalability:**
For large datasets, some methods (like filtering or generating summaries) might become slow. For persistent storage and improved performance, replacing in-memory storage for a database (like SQLite or PostgreSQL) could help manage and query transactions more efficiently.

- **Adding a GUI:**
Using Tkinter or similar framework to create a graphical interface for a more user-friendly experience.

#
## Author 👨🏻‍💻

This project was designed and developed by **Rafael Meller**.

[![Linkedin Badge](https://img.shields.io/badge/-Rafael_Meller-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/tgmarinho/)](https://www.linkedin.com/in/rafaelmeller/) 
[![Gmail Badge](https://img.shields.io/badge/-rafaelmeller.dev@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=rafaelmeller.dev@gmail.com)](mailto:rafaelmeller.dev@gmail.com)
#
## License 📝

This project is licensed under the [MIT](./LICENSE) license.