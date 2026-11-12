
import pandas as pd
from snowflake_connection import create_snowflake_connection

CSV_FILE = "data/processed/cleaned_sensor_data.csv"

def upload_sensor_data():
    df = pd.read_csv(CSV_FILE)

    conn = create_snowflake_connection()
    cursor = conn.cursor()

    try:
        insert_query = """
        INSERT INTO ATMOSYNC_DB.RAW_DATA.SENSOR_DATA
        (CONTAINER_ID, COMMODITY, TEMPERATURE_C,
         HUMIDITY_PCT, VIBRATION, TIMESTAMP)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        rows = [
            (
                row.container_id,
                row.commodity,
                row.temperature_c,
                row.humidity_pct,
                row.vibration,
                pd.to_datetime(row.timestamp).tz_convert(None).to_pydatetime()
            )
            for row in df.itertuples(index=False)
        ]

        cursor.executemany(insert_query, rows)
        conn.commit()

        print("Sensor data uploaded successfully!")
        print("Total records uploaded:", len(rows))

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    upload_sensor_data()
