from sqlalchemy import Column, String
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from src.models.base import Base


class Bots(Base):
    __tablename__ = 'bots'
    guid = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
