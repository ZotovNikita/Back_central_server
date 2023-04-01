from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.examples import Examples


class ExamplesRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def get_all(self) -> List[Examples]:
        examples = (
            self.session
            .query(Examples)
            .all()
        )
        return examples

    async def add(self, record: Examples) -> Examples:
        self.session.add(record)
        self.session.commit()
        return record
