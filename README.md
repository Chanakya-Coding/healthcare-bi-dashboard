# Healthcare Data Pipeline & BI Dashboard

<img width="1309" height="734" alt="image" src="https://github.com/user-attachments/assets/afb74ecd-3b3e-4d2e-99be-e996413137f7" />


An end-to-end data engineering and BI project: a Python ETL pipeline that extracts, cleans, and loads real-world diabetic patient encounter data into PostgreSQL, paired with an interactive Power BI dashboard connected live to the database.

## Project Overview

This project simulates a realistic healthcare analytics workflow — ingesting messy raw hospital encounter data, applying deliberate data cleaning decisions, structuring it in a relational database, and surfacing key readmission and care metrics through an interactive dashboard.

**Dataset:** [Diabetes 130-US Hospitals (1999–2008)](https://www.kaggle.com/datasets/brandao/diabetes) — 101,766 hospital encounter records covering diabetic patients across 130 US hospitals over 10 years.

## Architecture

Raw CSV → Extract → Transform → Load → PostgreSQL → Power BI (live connection)

| Stage | File | Purpose |
|---|---|---|
| Extract | `src/extract.py` | Loads raw CSV data, no transformation |
| Transform | `src/transform.py` | Cleans, reshapes, and enriches the data |
| Load | `src/load.py` | Writes cleaned data into PostgreSQL |
| Orchestration | `main.py` | Runs the full pipeline end-to-end |

## Tech Stack

- **Python** — pandas, SQLAlchemy, psycopg2, python-dotenv
- **PostgreSQL** — relational data storage
- **SQL** — analytical queries for reporting
- **Power BI Desktop** — live-connected interactive dashboard, DAX measures

## Data Cleaning Decisions

The raw dataset used `?` as a placeholder for missing values instead of true nulls, which required deliberate handling per column rather than a blanket fix:

- **`weight`** — dropped entirely (96.9% missing, no usable signal)
- **`medical_specialty`, `payer_code`, `race`, `diag_2`, `diag_3`** — filled with `"Unknown"` (moderate missingness, still analytically useful)
- **`max_glu_serum`, `A1Cresult`** — filled with `"Not Tested"` rather than `"Unknown"`, since missingness here likely reflects a test not being ordered, not a data gap
- **`diag_1`** — the 21 rows missing this field were dropped (negligible loss, but too central a field to leave blank)
- **`age`** — converted from bracketed strings (e.g. `[70-80)`) into a numeric midpoint (`age_numeric`) for analysis
- **Duplicate patient encounters** — identified that ~46% of all encounters belong to patients with multiple visits (16,767 of 71,509 unique patients). Rows were kept as-is (each represents a real, distinct encounter), but this distinction is accounted for when designing patient-level vs. encounter-level metrics

## SQL Analysis

Five analytical queries (see `sql/queries.sql`) were written and validated in pgAdmin before being used to inform the dashboard's measures:

1. Readmission rate by age group
2. Average length of stay by primary diagnosis
3. Admissions by admission type
4. Patient-level readmission (accounting for repeat encounters)
5. Readmission rate by diabetes medication status

## Dashboard

The Power BI dashboard connects **live** to the PostgreSQL database (via the Npgsql provider) rather than a static file export, so it reflects the current state of the database on refresh.

**Visuals include:**
- Readmission rate by age group (column chart)
- Average length of stay by top diagnoses (bar chart, with ICD-9 codes mapped to readable labels)
- Admission type breakdown (donut chart)
- Readmission rate by medication change status (table)
- Length of stay trend by medication count (line chart)

## Key Insight

Readmission rate rises steadily with patient age, from 18% in the youngest bracket to a peak of ~48% in the 70–90 age range. Patients whose diabetes medication was changed during their stay had a *higher* readmission rate (48.6%) than those with no change (40.5%) — likely reflecting reverse causation, where more clinically complex patients are both more likely to have medication adjusted and more likely to be readmitted, rather than the medication change itself driving readmission.

## Setup

1. Clone the repo
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`
3. Set up a PostgreSQL database and create a `.env` file with:
   DATABASE_URL=postgresql://username:password@localhost:5432/healthcare_db
4. Download `diabetic_data.csv` from the Kaggle dataset link above and place it in `data/raw/`
5. Run the pipeline: `python main.py`
6. Open `dashboard/healthcare_dashboard.pbix` in Power BI Desktop and connect to your local database

## Project Structure

healthcare-bi-pipeline/
├── data/
│   ├── raw/            # original CSV (not tracked in git)
│   └── processed/      # cleaned output
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── sql/
│   └── queries.sql
├── dashboard/
│   └── healthcare_dashboard.pbix
├── main.py
├── requirements.txt
└── README.md
