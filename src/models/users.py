from sqlalchemy import Column, String
import uuid
from src.utils.guid import GUID
from src.models.base import Base


class Users(Base):
    __tablename__ = 'users'
    guid = Column(GUID(), primary_key=True, default=uuid.uuid4)
    login = Column(String, nullable=False, unique=True)
    password_hashed = Column(String, nullable=False)
