from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data


def main():
    print("Starting pipeline...\n")

    print("Step 1: Extracting raw data...")
    extract_data()

    print("\nStep 2: Transforming data...")
    transform_data()

    print("\nStep 3: Loading into PostgreSQL...")
    load_data()

    print("\nPipeline complete!")


if __name__ == "__main__":
    main()