from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.schema import Sequence
from fastapi_utils.guid_type import GUID
from src.models.base import Base


class Intents(Base):
    __tablename__ = 'intents'
    # ! не решает проблемы
    seq = Sequence('intents_seq', start=0, minvalue=0, maxvalue=2147483647)  # ! автоматически не создавалась в alembic
    id = Column(Integer, seq, primary_key=True)
    name = Column(String, nullable=False)
    message = Column(String, nullable=False)
    bot_guid = Column(GUID, ForeignKey('bots.guid'), nullable=False)
    created_by = Column(GUID, ForeignKey('users.guid'), nullable=False)
