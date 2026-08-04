"""
This module is used to connect to the PostGres SQL database
"""

import os
import pandas as pd
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

class Connector:
    def __init__(self):
        self.database_url = DATABASE_URL
        self.engine = create_engine(DATABASE_URL) 
        self.current_user = self._get_current_user()
        self.current_database = self._get_current_database() 

    def __call__(self, data : pd.DataFrame):
        data.to_sql("data", self.engine, if_exists="replace", index=False)
    
    def _get_current_user(self):
        with self.engine.connect() as connection:
            res = connection.execute(text("SELECT current_user;"))
        return res.fetchone()

    def _get_current_database(self):
        with self.engine.connect() as connection:
            res = connection.execute(text("SELECT current_database();"))
        return res.fetchone()
