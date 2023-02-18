from pydantic import BaseSettings
from src.utils.pattern import singleton


@singleton
class Settings(BaseSettings):
    host: str = 'localhost'
    port: int = 9999

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
