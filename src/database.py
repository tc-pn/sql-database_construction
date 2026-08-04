"""
I guess a good practive is to create one user for modifications, and one user for reading and accessing data
"""
import os
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine, text

# en dur
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = (
    "postgresql+psycopg://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/"
    f"{DATABASE_NAME}"
)

engine = create_engine(DATABASE_URL)

# some verifications
with engine.connect() as connection:
    results = connection.execute(text("SELECT current_user, current_database();"))
    print(results.fetchone())