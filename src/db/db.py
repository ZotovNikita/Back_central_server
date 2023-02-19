from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from src.core.settings import settings


connection_string = URL.create(
    drivername='postgresql+psycopg2',
    username=settings.db_login,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_database
)

engine = create_engine(connection_string)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
