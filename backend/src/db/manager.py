from abc import ABC, abstractmethod
from typing import Iterable
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, select, and_
from sqlmodel.sql.expression import _ColumnExpressionArgument, SelectOfScalar
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import Base


class BaseDbManager(ABC):
    @abstractmethod
    def create(self, objs: Iterable[Base]) -> None:
        """ Add new objects to the corresponding collection. """

    @abstractmethod
    def get(self, obj_type: type, id: int) -> Base:
        """ Get an object from the corresponding collection by id. """

    @abstractmethod
    def filter(self, obj_type: type, filters: Iterable[_ColumnExpressionArgument[bool] | bool]) -> Iterable[Base]:
        """ Filter collection by filters. """

    @abstractmethod
    def update(self, id: int, upd_obj: Base) -> None:
        """ Update an existing object from the existing collection. """

    @abstractmethod
    def delete(self, obj: Base) -> None:
        """ Delete an object by id. """
    

class SqlDbManager(BaseDbManager):
    def __init__(self, db_link: str):
        self.engine = create_async_engine(
            db_link
        )
        # SQLModel.metadata.create_all(self.engine)

    async def create(self, objs: Iterable[Base]) -> None:
        async with AsyncSession(self.engine) as session:
            session.add_all(objs)
            await session.commit()

    async def get(self, obj_type: type, id: int) -> Base:
        async with AsyncSession(self.engine) as session:
            return session.get(obj_type, id)
        
    async def filter(self, obj_type: type, filters: Iterable[_ColumnExpressionArgument[bool] | bool]) -> SelectOfScalar:
        async with AsyncSession(self.engine) as session:
            expression = select(obj_type).where(*filters)
            return await session.exec(expression)
        
    async def update(self, id: int, upd_obj: Base) -> None:
        async with AsyncSession(self.engine) as session:
            obj = session.get(type(obj), id)
            if not obj:
                raise ValueError("Object not found.")
            
            obj_to_update = upd_obj.model_dump()
            for k, v in obj_to_update.items():
                setattr(obj, k, v)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
        
    async def delete(self, obj: Base) -> None:
        async with AsyncSession(self.engine) as session:
            await session.delete(obj)
            await session.commit()
