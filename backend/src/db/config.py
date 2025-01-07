import os
from dotenv import load_dotenv

from src.db.manager import SqlDbManager


load_dotenv()


db_manager = SqlDbManager(
    os.getenv("DB_LINK")
)
