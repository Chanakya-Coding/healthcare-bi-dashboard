from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("Connected successfully!")
        print(result.fetchone())
except Exception as e:
    print("Connection failed:")
    print(e)


