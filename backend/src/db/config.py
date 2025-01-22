from src.db.manager import SqlDbManager
from settings import settings


db_manager = SqlDbManager(
    settings.DB_URL
)
