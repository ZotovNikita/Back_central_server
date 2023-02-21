from sqlalchemy import Column, String
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from src.models.base import Base


class Roles(Base):
    __tablename__ = 'roles'
    guid = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = Column(String, nullable=False)
