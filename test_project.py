import pytest
from datetime import datetime
from project import CashFlowTracker, Transaction, check_date_format, export_data, group_uncategorized, group_by_month, read_csv


@pytest.fixture
def cashflowtracker():
    tracker = CashFlowTracker()
    transactions = [
        Transaction("2024-01-01", "", "Salary", 2500.00),
        Transaction("2024-02-02", "", "Walmart", -120.50),
        Transaction("2024-02-05", "Food", "Restaurant", -50.00),
        Transaction("2024-02-10", "", "Walmart", -100.00),
        Transaction("2024-03-01", "Rent", "Rent", -1000.00),
    ]
    for transaction in transactions:
        tracker.add(transaction)
    return tracker


def test_read_csv():
    csv_path = "sample.csv"

    transactions = list(read_csv(csv_path))

    assert len(transactions) == 90
    assert transactions[0].date == datetime.strptime("2024-01-05", "%Y-%m-%d").date()
    assert transactions[0].value == 2500.00
    assert transactions[0].description == "Salary"
    assert transactions[3].value == -120.50
    assert transactions[3].description == "Walmart"


def test_read_csv_data_error(tmpdir):
    missing_date_csv = tmpdir.join("missing_date.csv")
    missing_date_csv.write("Value,Description\n2500.00,Salary\n-120.50,Walmart")

    missing_value_csv = tmpdir.join("missing_value.csv")
    missing_value_csv.write("Date,Description\n2024-01-01,Salary\n2024-02-02,Walmart")

    missing_description_csv = tmpdir.join("missing_description.csv")
    missing_description_csv.write("Date,Value\n2024-01-01,2500.00\n2024-02-02,-120.50")

    with pytest.raises(ValueError, match="'date' column not found in CSV file."):
        list(read_csv(str(missing_date_csv)))

    with pytest.raises(ValueError, match="'value' column not found in CSV file."):
        list(read_csv(str(missing_value_csv)))

    with pytest.raises(ValueError, match="'description' column not found in CSV file."):
        list(read_csv(str(missing_description_csv)))


def test_group_uncategorized(cashflowtracker): 
    uncategorized = group_uncategorized(cashflowtracker)

    assert len(uncategorized) == 2
    assert "Salary" in uncategorized
    assert "Walmart" in uncategorized
    assert "Rent" not in uncategorized
    assert "Restaurant" not in uncategorized

    assert len(uncategorized["Salary"]) == 1
    assert uncategorized["Salary"][0].value == 2500.00

    assert len(uncategorized["Walmart"]) == 2
    assert uncategorized["Walmart"][0].value == -120.50
    assert uncategorized["Walmart"][1].value == -100.00


def test_export_data(cashflowtracker):
    filename = "test_export.csv"
    message = export_data(cashflowtracker, filename)

    with open("test_export.csv", "r") as file:
        lines = file.readlines()
        assert len(lines) == 6
        assert lines[0] == "Date,Category,Description,Value\n"
        assert lines[1] == "2024-01-01,,Salary,2500.0\n"
        assert lines[2] == "2024-02-02,,Walmart,-120.5\n"
        assert lines[3] == "2024-02-05,Food,Restaurant,-50.0\n"
        assert lines[4] == "2024-02-10,,Walmart,-100.0\n"
        assert lines[5] == "2024-03-01,Rent,Rent,-1000.0\n"

    assert message == f"{filename} exported successfully."
    

def test_export_data_invalid_filename(cashflowtracker):
    with pytest.raises(ValueError, match="Invalid file name. Please choose a name that contains only alphanumeric characters, underscores, or hyphens."):
        export_data(cashflowtracker, "test@export.csv")


def test_export_data_invalid_extension():
    list_sample = [1, 2, 3]
    dict_sample = {"a": 1, "b": 2, "c": 3}

    with pytest.raises(ValueError, match="Invalid data type. Please enter a valid data type."):
        export_data(list_sample, "test_export.csv")

    with pytest.raises(ValueError, match="Invalid data type. Please enter a valid data type."):
        export_data(dict_sample, "test_export.csv")


def test_check_date_format():
    date_list = ["2024-01-01", "2024-01-02", "2024-01-03"]
    assert check_date_format(date_list) == "yearfirst"

    date_list = ["01/01/2024", "02/01/2024", "03/30/2024"]
    assert check_date_format(date_list) == "monthfirst"

    date_list = ["01-01-2024", "28-01-2024", "03-01-2024"]
    assert check_date_format(date_list) == "dayfirst"

    date_list = ["01-01-2024", "28-01-2024", "03-01-2024", "2024-01-01"]
    assert check_date_format(date_list) == None

    date_list = ["01-01-2024", "04-01-2024", "03-01-2024"]
    assert check_date_format(date_list) == None


def test_group_by_month(cashflowtracker):
    grouped = group_by_month(cashflowtracker)
    
    assert len(grouped) == 3
    assert "January 2024" in grouped
    assert "February 2024" in grouped
    assert "March 2024" in grouped
    assert len(grouped["January 2024"]) == 1
    assert len(grouped["February 2024"]) == 3
    assert len(grouped["March 2024"]) == 1