from sqlalchemy import Column, ForeignKey, Integer, String
from src.models.base import Base


class Examples(Base):
    __tablename__ = 'examples'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    intent_id = Column(Integer, ForeignKey('intents.id'), nullable=False)
