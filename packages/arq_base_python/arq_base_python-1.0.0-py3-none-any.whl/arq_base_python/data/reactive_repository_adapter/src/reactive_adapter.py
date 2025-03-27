from typing import Generic, TypeVar
from fastapi import HTTPException, status
from sqlmodel import Session, select
from reactivex import Observable, of
from adapters.database.src.config.db import engine
from cqrs.core_api.src.common.reactive_crud import ReactiveCrud

T = TypeVar('T', bound='SQLModel')

NOT_FOUND = "Item not found"


class SessionManager(Generic[T]):
    def __init__(self, entity: type[T]):
        self.entity = entity

    def save(self, session: Session, entity: T) -> T:
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    def delete(self, session: Session, entity: T) -> None:
        session.delete(entity)
        session.commit()
        return None

    def get_or_404(self, session: Session, entity_id: int) -> T:
        entity = session.get(self.entity, entity_id)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{self.entity.__name__} with id {entity_id} not found")
        return entity


class ReactiveAdapter(ReactiveCrud, Generic[T]):
    def __init__(self, entity: type[T]):
        self.entity = entity
        self.repository = SessionManager(entity)

    def all(self) -> Observable[T]:
        with Session(engine) as session:
            stmt = select(self.entity)
            result = session.exec(stmt)
            return of(*result.all())

    def save(self, entity: T) -> Observable[T]:
        with Session(engine) as session:
            return of(self.repository.save(session, entity))

    def update(self, entity_in: T) -> Observable[T]:
        with Session(engine) as session:
            entity_db = session.get(self.entity, entity_in.id)
            if not entity_db:
                # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                #                     detail=f"{self.entity.__name__} with id {entity_in.id} not found")
                entity_in.id = None
                return of(self.repository.save(session, entity_in))
            update_dict = entity_in.model_dump()
            entity_db.sqlmodel_update(update_dict)
            return of(self.repository.save(session, entity_db))

    def delete(self, var1: int) -> Observable[None]:
        with Session(engine) as session:
            item = self.repository.get_or_404(session, var1)
            return of(self.repository.delete(session, item))
