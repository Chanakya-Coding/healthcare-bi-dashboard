import pandas as pd
from pathlib import Path
from src.extract import extract_data

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "diabetic_data.csv"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "diabetic_data_clean.csv"


def transform_data(raw_path=RAW_PATH, save_path=PROCESSED_PATH) -> pd.DataFrame:
    df = extract_data(raw_path)

    df = df.replace('?', pd.NA)

    # Drop weight - 96.9% missing, unusable
    df = df.drop(columns=['weight'])

    # Fill moderate-missingness categorical columns with 'Unknown'
    for col in ['medical_specialty', 'payer_code', 'race', 'diag_2', 'diag_3']:
        df[col] = df[col].fillna('Unknown')

    # These are lab test results - missing means test wasn't performed, not unknown
    for col in ['max_glu_serum', 'A1Cresult']:
        df[col] = df[col].fillna('Not Tested')

    df = df.dropna(subset=['diag_1'])

    # Convert age brackets like '[70-80)' to numeric midpoint
    def age_to_midpoint(age_bracket):
        low, high = age_bracket.strip('[]()').split('-')
        return (int(low) + int(high)) / 2

    df['age_numeric'] = df['age'].apply(age_to_midpoint)

    duplicate_patients = df['patient_nbr'].value_counts()
    repeat_patients = duplicate_patients[duplicate_patients > 1]

    print(f"Total unique patients: {df['patient_nbr'].nunique()}")
    print(f"Patients with multiple encounters: {len(repeat_patients)}")
    print(f"Total rows from repeat patients: {repeat_patients.sum()}")

    print("Shape after cleaning:", df.shape)
    print("Remaining nulls:\n", df.isna().sum()[df.isna().sum() > 0])

    df.to_csv(save_path, index=False)
    print(f"Saved cleaned data to {save_path}")

    return df


if __name__ == "__main__":
    transform_data()