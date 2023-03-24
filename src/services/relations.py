from typing import List
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.relations import Relations
from src.models.schemas.relations.request import RelationsRequest


class RelationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get(self, id: int) -> Relations:
        relation = (
            self.session
            .query(Relations)
            .filter(Relations.id == id)
            .one_or_none()
        )

        if not relation:
            raise HTTPException(status_code=404, detail='Связь не найдена')

        return relation

    def all(self) -> List[Relations]:
        relations = (
            self.session
            .query(Relations)
            .all()
        )

        if not relations:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return relations

    def add(self, request: RelationsRequest, user: dict) -> Relations:
        is_exist = (
            self.session
            .query(Relations)
            .filter_by(id=request.id)
            .count()
        )
        if is_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        relation = Relations()
        for field, value in request:
            setattr(relation, field, value)

        self.session.add(relation)
        self.session.commit()
        return relation

    def update(self, id: int, request: RelationsRequest) -> Relations:
        relation = self.get(id)
        same_relation = self.get(request.id)

        if same_relation and id != same_relation.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        for field, value in request:
            setattr(relation, field, value)

        self.session.commit()
        return relation

    def delete(self, id: int) -> None:
        relation = self.get(id)
        self.session.delete(relation)
        self.session.commit()
