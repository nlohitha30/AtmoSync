
import csv
from src.snowflake_connection import create_snowflake_connection

FILE_PATH = "data/raw/commodity_prices.csv"

def upload_commodity_prices():
    connection = create_snowflake_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ATMOSYNC_DB.RAW_DATA.COMMODITY_PRICES (
                COMMODITY VARCHAR(100),
                MARKET VARCHAR(100),
                PRICE_PER_KG FLOAT,
                CURRENCY VARCHAR(10),
                UNIT VARCHAR(10),
                PRICE_DATE DATE,
                DATA_SOURCE VARCHAR(50)
            )
        """)

        with open(FILE_PATH, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            records = [
                (
                    row["COMMODITY"],
                    row["MARKET"],
                    float(row["PRICE_PER_KG"]),
                    row["CURRENCY"],
                    row["UNIT"],
                    row["PRICE_DATE"],
                    row["DATA_SOURCE"]
                )
                for row in reader
            ]

        if records:
            cursor.executemany("""
                INSERT INTO ATMOSYNC_DB.RAW_DATA.COMMODITY_PRICES
                (COMMODITY, MARKET, PRICE_PER_KG, CURRENCY, UNIT,
                 PRICE_DATE, DATA_SOURCE)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, records)

        connection.commit()
        print("Commodity price upload successful!")
        print("Records uploaded:", len(records))

    except Exception as error:
        connection.rollback()
        print("Upload failed:", error)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    upload_commodity_prices()
