from pydantic import BaseSettings
import spacy


class Settings(BaseSettings):
    host: str = 'localhost'
    port: int = 9999
    docs_url: str = '/docs'
    redoc_url: str = '/redoc'
    
    db_login: str
    db_password: str
    db_host: str
    db_port: int
    db_database: str
    
    jwt_secret: str
    jwt_algorithm: str
    jwt_expires_seconds: int
    
    admin_login: str
    admin_password: str

    in_doubt_command: str = '/wrong'

    models_dir: str = 'storage/models'
    spacy_model_name: str = 'ru_core_news_lg'
    fit_epochs: int = 15
    step_epochs: int = 5
    verbose: bool = False

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()

spacy_model = spacy.load(settings.spacy_model_name)
