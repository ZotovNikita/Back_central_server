from sqlalchemy import Column, String
import uuid
from src.utils.guid import GUID
from src.models.base import Base


class Bots(Base):
    __tablename__ = 'bots'
    guid = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
