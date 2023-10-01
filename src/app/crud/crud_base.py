from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
UpdateSchemaInternalType = TypeVar("UpdateSchemaInternalType", bound=BaseModel)
DeleteSchemaType = TypeVar("DeleteSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, UpdateSchemaInternalType, DeleteSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def create(
            self, db: AsyncSession, object: CreateSchemaType
    ) -> ModelType:
        object_dict = object.model_dump()
        db_object = self._model(**object_dict)
        db.add(db_object)
        await db.commit()
        return db_object

    async def get(self, db: AsyncSession, **kwargs) -> Optional[ModelType]:
        query = select(self._model).filter_by(**kwargs)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_multi(
            self, db: AsyncSession, offset: int = 0, limit: int = 100, **kwargs
    ) -> List[ModelType]:
        query = select(self._model) \
            .filter_by(**kwargs) \
            .offset(offset) \
            .limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()

    async def update(
            self,
            db: AsyncSession,
            object: Union[UpdateSchemaType, Dict[str, Any]],
            db_object: ModelType | None = None,
            **kwargs
    ) -> Optional[ModelType]:
        db_object = db_object or await self.get(db=db, **kwargs)
        if db_object:
            if isinstance(object, dict):
                update_data = object
            else:
                update_data = object.model_dump(exclude_unset=True)
            
            update_data.update({"updated_at": datetime.utcnow()})
            for field in object.__dict__:
                if field in update_data:
                    setattr(db_object, field, update_data[field])
            db.add(db_object)
            await db.commit()

        return db_object

    async def db_delete(
            self,
            db: AsyncSession,
            db_object: ModelType | None = None,
            **kwargs
    ):
        db_object = db_object or await self.get(db=db, **kwargs)
        await db.delete(db_object)
        await db.commit()
        return db_object

    async def delete(
            self,
            db: AsyncSession,
            db_object: ModelType | None = None,
            **kwargs
    ) -> Optional[ModelType]:
        db_object = db_object or await self.get(db=db, **kwargs)
        if db_object:
            if "is_deleted" in db_object.__dict__.keys():
                object_dict = {
                    "is_deleted": True,
                    "deleted_at": datetime.utcnow()
                }
                query = update(self._model) \
                    .filter_by(**kwargs) \
                    .values(object_dict)
                
                await db.execute(query)
                await db.commit()
                await db.refresh(db_object)
            else:
                db_object = await self.db_delete(db=db, db_object=db_object, **kwargs)

        return db_object
