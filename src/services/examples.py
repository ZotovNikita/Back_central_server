from typing import List
from fastapi import Depends
from src.repositories.examples import ExamplesRepository
from src.models.examples import Examples
from src.models.schemas.examples.request import ExamplesRequest


class ExamplesService:
    def __init__(self, repository: ExamplesRepository = Depends()):
        self.repo = repository

    async def get_all(self) -> List[Examples]:
        return await self.repo.get_all()

    async def get_all_by_intent_id(self, intent_id: int) -> List[Examples]:
        return await self.repo.get_all_by_intent_id(intent_id)

    async def add(self, request: ExamplesRequest) -> Examples:
        return await self.repo.add(Examples(**dict(request)))

    async def delete(self, record: Examples) -> None:
        return await self.repo.delete(record)
