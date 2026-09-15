import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
processed_path = PROJECT_ROOT / "data" / "processed" / "diabetic_data_clean.csv"


def load_data(csv_path=processed_path, table_name="encounters"):
    df = pd.read_csv(csv_path)

    df.to_sql(
        table_name,
        con=engine,
        if_exists="replace",  # overwrite table each run for now
        index=False
    )

    print(f"Loaded {len(df)} rows into '{table_name}' table")


if __name__ == "__main__":
    load_data()