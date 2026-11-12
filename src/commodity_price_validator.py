
import csv
from datetime import datetime

FILE_PATH = "data/raw/commodity_prices.csv"

REQUIRED_COLUMNS = [
    "COMMODITY",
    "MARKET",
    "PRICE_PER_KG",
    "CURRENCY",
    "UNIT",
    "PRICE_DATE",
    "DATA_SOURCE"
]

def validate_commodity_prices():
    valid_records = 0
    invalid_records = 0

    with open(FILE_PATH, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not all(
            column in reader.fieldnames for column in REQUIRED_COLUMNS
        ):
            print("ERROR: Required columns are missing!")
            return

        for row_number, row in enumerate(reader, start=2):
            try:
                if any(not row[column].strip() for column in REQUIRED_COLUMNS):
                    raise ValueError("Empty field found")

                price = float(row["PRICE_PER_KG"])

                if price <= 0:
                    raise ValueError("Price must be positive")

                datetime.strptime(row["PRICE_DATE"], "%Y-%m-%d")

                valid_records += 1

            except (ValueError, KeyError):
                invalid_records += 1
                print(f"Invalid record at row {row_number}")

    print("\nATMOSYNC COMMODITY PRICE VALIDATION")
    print("===================================")
    print("Valid records:", valid_records)
    print("Invalid records:", invalid_records)

    if invalid_records == 0:
        print("Validation completed successfully!")

if __name__ == "__main__":
    validate_commodity_prices()
