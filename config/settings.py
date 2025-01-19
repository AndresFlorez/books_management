import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class MongoSettings(BaseSettings):
    """Settings for Django application."""

    db_host: str = os.getenv('DB_HOST')
    db_port: int = os.getenv('DB_PORT')
    db_user: str = os.getenv('DB_USER')
    db_password: str = os.getenv('DB_PASSWORD')
    db_name: str = os.getenv('DB_NAME')


mongo_settings = MongoSettings()
