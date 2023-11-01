from typing import Any, Dict, Generic, List, Type, TypeVar, Union
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.row import Row

from .helper import _extract_matching_columns_from_schema, _extract_matching_columns_from_kwargs

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
UpdateSchemaInternalType = TypeVar("UpdateSchemaInternalType", bound=BaseModel)
DeleteSchemaType = TypeVar("DeleteSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, UpdateSchemaInternalType, DeleteSchemaType]):
    """
    Base class for CRUD operations on a model.

    Parameters
    ----------
    model : Type[ModelType]
        The SQLAlchemy model type.
    """
    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def create(
            self, 
            db: AsyncSession, 
            object: CreateSchemaType
    ) -> ModelType:
        """
        Create a new record in the database.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        object : CreateSchemaType
            The Pydantic schema containing the data to be saved.

        Returns
        -------
        ModelType
            The created database object.
        """
        object_dict = object.model_dump()
        db_object = self._model(**object_dict)
        db.add(db_object)
        await db.commit()
        return db_object

    async def get(
            self, 
            db: AsyncSession, 
            schema_to_select: Type[BaseModel] | None = None, 
            **kwargs
    ) -> ModelType | None:
        """
        Fetch a single record based on filters.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        schema_to_select : Type[BaseModel] | None, optional
            Pydantic schema for selecting specific columns. Default is None to select all columns.
        kwargs : dict
            Filters to apply to the query.

        Returns
        -------
        ModelType | None
            The fetched database row or None if not found.
        """
        to_select = _extract_matching_columns_from_schema(model=self._model, schema=schema_to_select)
        stmt = select(*to_select) \
            .filter_by(**kwargs)
        
        result = await db.execute(stmt)
        return result.first()
    
    async def get_multi(
            self, 
            db: AsyncSession, 
            offset: int = 0, 
            limit: int = 100, 
            schema_to_select: Type[BaseModel] | None = None, 
            **kwargs
    ) -> List[ModelType]:
        """
        Fetch multiple records based on filters.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        offset : int, optional
            Number of rows to skip before fetching. Default is 0.
        limit : int, optional
            Maximum number of rows to fetch. Default is 100.
        schema_to_select : Type[BaseModel] | None, optional
            Pydantic schema for selecting specific columns. Default is None to select all columns.
        kwargs : dict
            Filters to apply to the query.

        Returns
        -------
        List[ModelType]
            List of fetched database rows.
        """
        to_select = _extract_matching_columns_from_schema(model=self._model, schema=schema_to_select)
        stmt = select(*to_select) \
            .filter_by(**kwargs) \
            .offset(offset) \
            .limit(limit)
        
        result = await db.execute(stmt)
        return result.all()
    
    async def exists(
            self, 
            db: AsyncSession, 
            **kwargs
    ) -> bool:
        """
        Check if a record exists based on filters.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        kwargs : dict
            Filters to apply to the query.

        Returns
        -------
        bool
            True if a record exists, False otherwise.
        """
        to_select = _extract_matching_columns_from_kwargs(model=self._model, kwargs=kwargs)
        stmt = select(*to_select) \
            .filter_by(**kwargs) \
            .limit(1)
        result = await db.execute(stmt)
        
        return result.first() is not None
        
    async def update(
            self, 
            db: AsyncSession, 
            object: Union[UpdateSchemaType, Dict[str, Any]], 
            **kwargs
    ) -> None:
        """
        Update an existing record in the database.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        object : Union[UpdateSchemaType, Dict[str, Any]]
            The Pydantic schema or dictionary containing the data to be updated.
        kwargs : dict
            Filters for the update.

        Returns
        -------
        None
        """
        if isinstance(object, dict):
            update_data = object
        else:
            update_data = object.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()

        stmt = update(self._model) \
            .filter_by(**kwargs) \
            .values(update_data)
        
        await db.execute(stmt)
        await db.commit()

    async def db_delete(
            self, 
            db: AsyncSession, 
            **kwargs
    ) -> None:
        """
        Delete a record in the database.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        kwargs : dict
            Filters for the delete.

        Returns
        -------
        None
        """
        stmt = delete(self._model).filter_by(**kwargs)
        await db.execute(stmt)
        await db.commit()

    async def delete(
            self, 
            db: AsyncSession, 
            db_row: Row | None = None, 
            **kwargs
    ) -> None:
        """
        Soft delete a record if it has "is_deleted" attribute, otherwise perform a hard delete.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        db_row : Row | None, optional
            Existing database row to delete. If None, it will be fetched based on `kwargs`. Default is None.
        kwargs : dict
            Filters for fetching the database row if not provided.

        Returns
        -------
        None
        """
        db_row = db_row or await self.get(db=db, **kwargs)
        if db_row:
            if "is_deleted" in db_row:
                object_dict = {
                    "is_deleted": True,
                    "deleted_at": datetime.utcnow()
                }
                stmt = update(self._model) \
                    .filter_by(**kwargs) \
                    .values(object_dict)
                
                await db.execute(stmt)
                await db.commit()

            else:
                stmt = delete(self._model).filter_by(**kwargs)
                await db.execute(stmt)
                await db.commit()
