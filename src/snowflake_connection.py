
import os
import snowflake.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_snowflake_connection():
    connection = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

    return connection


if __name__ == "__main__":
    try:
        conn = create_snowflake_connection()
        print("Snowflake connection successful!")
        print("Connected to ATMOSYNC_DB")
        conn.close()

    except Exception as error:
        print("Snowflake connection failed!")
        print(error)
