from typing import Any, Dict, Generic, List, Type, TypeVar, Union
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import select, update, delete, func, and_, inspect
from sqlalchemy.sql import Join
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.row import Row

from .helper import (
    _extract_matching_columns_from_schema, 
    _extract_matching_columns_from_kwargs,
    _auto_detect_join_condition,
    _add_column_with_prefix
)
from app.core.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
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
        db_object: ModelType = self._model(**object_dict)
        db.add(db_object)
        await db.commit()
        return db_object

    async def get(
            self, 
            db: AsyncSession, 
            schema_to_select: Union[Type[BaseModel], List, None] = None,
            **kwargs: Any
    ) -> Dict | None:
        """
        Fetch a single record based on filters.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        schema_to_select : Union[Type[BaseModel], List, None], optional
            Pydantic schema for selecting specific columns. Default is None to select all columns.
        kwargs : dict
            Filters to apply to the query.

        Returns
        -------
        Dict | None
            The fetched database row or None if not found.
        """
        to_select = _extract_matching_columns_from_schema(model=self._model, schema=schema_to_select)
        stmt = select(*to_select) \
            .filter_by(**kwargs)
        
        db_row = await db.execute(stmt)
        result: Row = db_row.first()
        if result is not None:
            out: dict = dict(result._mapping)
        
        return out
    
    async def exists(
            self, 
            db: AsyncSession, 
            **kwargs: Any
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
    
    async def count(
        self, 
        db: AsyncSession,
        **kwargs: Any
    ) -> int:
        """
        Count the records based on filters.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        kwargs : dict
            Filters to apply to the query.

        Returns
        -------
        int
            Total count of records that match the applied filters.

        Note
        ----
        This method provides a quick way to get the count of records without retrieving the actual data.
        """
        conditions = [getattr(self._model, key) == value for key, value in kwargs.items()]
        combined_conditions = and_(*conditions)

        count_query = select(func.count()).filter(combined_conditions)
        total_count: int = await db.scalar(count_query)

        return total_count

    async def get_multi(
            self, 
            db: AsyncSession, 
            offset: int = 0, 
            limit: int = 100, 
            schema_to_select: Union[Type[BaseModel], List[Type[BaseModel]], None] = None,
            **kwargs: Any
    ) -> Dict[str, Any]:
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
        schema_to_select : Union[Type[BaseModel], List[Type[BaseModel]], None], optional
            Pydantic schema for selecting specific columns. Default is None to select all columns.
        kwargs : dict
            Filters to apply to the query.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing the fetched rows under 'data' key and total count under 'total_count'.
        """
        to_select = _extract_matching_columns_from_schema(model=self._model, schema=schema_to_select)
        stmt = select(*to_select) \
            .filter_by(**kwargs) \
            .offset(offset) \
            .limit(limit)
        
        result = await db.execute(stmt)
        data = [dict(row) for row in result.mappings()]

        total_count = await self.count(db=db, **kwargs)

        return {"data": data, "total_count": total_count}
    
    async def get_joined(
            self,
            db: AsyncSession,
            join_model: Type[ModelType],
            join_prefix: str | None = None,
            join_on: Union[Join, None] = None,
            schema_to_select: Union[Type[BaseModel], List, None] = None,
            join_schema_to_select: Union[Type[BaseModel], List, None] = None,
            join_type: str = "left",
            **kwargs: Any
    ) -> dict | None:
        """
        Fetches a single record with a join on another model. If 'join_on' is not provided, the method attempts 
        to automatically detect the join condition using foreign key relationships.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        join_model : Type[ModelType]
            The model to join with.
        join_prefix : Optional[str]
            Optional prefix to be added to all columns of the joined model. If None, no prefix is added.
        join_on : Join, optional
            SQLAlchemy Join object for specifying the ON clause of the join. If None, the join condition is 
            auto-detected based on foreign keys.
        schema_to_select : Union[Type[BaseModel], List, None], optional
            Pydantic schema for selecting specific columns from the primary model.
        join_schema_to_select : Union[Type[BaseModel], List, None], optional
            Pydantic schema for selecting specific columns from the joined model.
        join_type : str, default "left"
            Specifies the type of join operation to perform. Can be "left" for a left outer join or "inner" for an inner join.
        kwargs : dict
            Filters to apply to the query.

        Returns
        -------
        Dict | None
            The fetched database row or None if not found.

        Examples
        --------
        Simple example: Joining User and Tier models without explicitly providing join_on
        ```python
        result = await crud_user.get_joined(
            db=session,
            join_model=Tier,
            schema_to_select=UserSchema,
            join_schema_to_select=TierSchema
        )
        ```

        Complex example: Joining with a custom join condition, additional filter parameters, and a prefix
        ```python
        from sqlalchemy import and_
        result = await crud_user.get_joined(
            db=session,
            join_model=Tier,
            join_prefix="tier_",
            join_on=and_(User.tier_id == Tier.id, User.is_superuser == True),
            schema_to_select=UserSchema,
            join_schema_to_select=TierSchema,
            username="john_doe"
        )
        ```

        Return example: prefix added, no schema_to_select or join_schema_to_select
        ```python
        {
            "id": 1,
            "name": "John Doe",
            "username": "john_doe",
            "email": "johndoe@example.com",
            "hashed_password": "hashed_password_example",
            "profile_image_url": "https://profileimageurl.com/default.jpg",
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "created_at": "2023-01-01T12:00:00",
            "updated_at": "2023-01-02T12:00:00",
            "deleted_at": null,
            "is_deleted": false,
            "is_superuser": false,
            "tier_id": 2,
            "tier_name": "Premium",
            "tier_created_at": "2022-12-01T10:00:00",
            "tier_updated_at": "2023-01-01T11:00:00"
        }
        ```
        """
        if join_on is None:
            join_on = _auto_detect_join_condition(self._model, join_model)

        primary_select = _extract_matching_columns_from_schema(model=self._model, schema=schema_to_select)
        join_select = []

        if join_schema_to_select:
            columns = _extract_matching_columns_from_schema(model=join_model, schema=join_schema_to_select)
        else:
            columns = inspect(join_model).c
            
        for column in columns:
            labeled_column = _add_column_with_prefix(column, join_prefix)
            if f"{join_prefix}{column.name}" not in [col.name for col in primary_select]:
                join_select.append(labeled_column)

        if join_type == "left":
            stmt = select(*primary_select, *join_select).outerjoin(join_model, join_on)
        elif join_type == "inner":
            stmt = select(*primary_select, *join_select).join(join_model, join_on)
        else:
            raise ValueError(f"Invalid join type: {join_type}. Only 'left' or 'inner' are valid.")

        for key, value in kwargs.items():
            if hasattr(self._model, key):
                stmt = stmt.where(getattr(self._model, key) == value)

        db_row = await db.execute(stmt)
        result: Row = db_row.first()
        if result:
            out: dict = dict(result._mapping)
            return out
        
        return None
    
    async def get_multi_joined(
            self,
            db: AsyncSession,
            join_model: Type[ModelType],
            join_prefix: str | None = None,
            join_on: Union[Join, None] = None,
            schema_to_select: Union[Type[BaseModel], List[Type[BaseModel]], None] = None,
            join_schema_to_select: Union[Type[BaseModel], List[Type[BaseModel]], None] = None,
            join_type: str = "left",
            offset: int = 0,
            limit: int = 100,
            **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Fetch multiple records with a join on another model, allowing for pagination.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        join_model : Type[ModelType]
            The model to join with.
        join_prefix : Optional[str]
            Optional prefix to be added to all columns of the joined model. If None, no prefix is added.
        join_on : Join, optional
            SQLAlchemy Join object for specifying the ON clause of the join. If None, the join condition is 
            auto-detected based on foreign keys.
        schema_to_select : Union[Type[BaseModel], List[Type[BaseModel]], None], optional
            Pydantic schema for selecting specific columns from the primary model.
        join_schema_to_select : Union[Type[BaseModel], List[Type[BaseModel]], None], optional
            Pydantic schema for selecting specific columns from the joined model.
        join_type : str, default "left"
            Specifies the type of join operation to perform. Can be "left" for a left outer join or "inner" for an inner join.
        offset : int, default 0
            The offset (number of records to skip) for pagination.
        limit : int, default 100
            The limit (maximum number of records to return) for pagination.
        kwargs : dict
            Filters to apply to the primary query.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the fetched rows under 'data' key and total count under 'total_count'.

        Examples
        --------
        # Fetching multiple User records joined with Tier records, using left join
        users = await crud_user.get_multi_joined(
            db=session,
            join_model=Tier,
            join_prefix="tier_",
            schema_to_select=UserSchema,
            join_schema_to_select=TierSchema,
            offset=0,
            limit=10
        )
        """
        if join_on is None:
            join_on = _auto_detect_join_condition(self._model, join_model)

        primary_select = _extract_matching_columns_from_schema(model=self._model, schema=schema_to_select)
        join_select = []

        if join_schema_to_select:
            columns = _extract_matching_columns_from_schema(model=join_model, schema=join_schema_to_select)
        else:
            columns = inspect(join_model).c

        for column in columns:
            labeled_column = _add_column_with_prefix(column, join_prefix)
            if f"{join_prefix}{column.name}" not in [col.name for col in primary_select]:
                join_select.append(labeled_column)

        if join_type == "left":
            stmt = select(*primary_select, *join_select).outerjoin(join_model, join_on)
        elif join_type == "inner":
            stmt = select(*primary_select, *join_select).join(join_model, join_on)
        else:
            raise ValueError(f"Invalid join type: {join_type}. Only 'left' or 'inner' are valid.")

        for key, value in kwargs.items():
            if hasattr(self._model, key):
                stmt = stmt.where(getattr(self._model, key) == value)

        stmt = stmt.offset(offset).limit(limit)

        db_rows = await db.execute(stmt)
        data = [dict(row._mapping) for row in db_rows]

        total_count = await self.count(db=db, **kwargs)

        return {"data": data, "total_count": total_count}

    async def update(
            self, 
            db: AsyncSession, 
            object: Union[UpdateSchemaType, Dict[str, Any]], 
            **kwargs: Any
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
        
        if "updated_at" in update_data.keys():
            update_data["updated_at"] = datetime.utcnow()

        stmt = update(self._model) \
            .filter_by(**kwargs) \
            .values(update_data)
        
        await db.execute(stmt)
        await db.commit()

    async def db_delete(
            self, 
            db: AsyncSession, 
            **kwargs: Any
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
            **kwargs: Any
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
        db_row = db_row or await self.exists(db=db, **kwargs)
        if db_row:
            if "is_deleted" in self._model.__table__.columns:
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
