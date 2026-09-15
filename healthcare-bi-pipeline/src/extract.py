import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "diabetic_data.csv"


def extract_data(path=RAW_DATA_PATH):
    df = pd.read_csv(path)
    return df


if __name__ == "__main__":
    df = extract_data()
    print(f"Extracted {df.shape[0]} rows and {df.shape[1]} columns")