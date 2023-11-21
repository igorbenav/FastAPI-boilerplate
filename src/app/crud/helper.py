from typing import Any, List, Type, Union

from pydantic import BaseModel

from app.core.database import Base

def _extract_matching_columns_from_schema(model: Type[Base], schema: Union[Type[BaseModel], list, None]) -> List[Any]:
    """
    Retrieves a list of ORM column objects from a SQLAlchemy model that match the field names in a given Pydantic schema.

    Parameters
    ----------
    model: Type[Base]
        The SQLAlchemy ORM model containing columns to be matched with the schema fields.
    schema: Type[BaseModel]
        The Pydantic schema containing field names to be matched with the model's columns.

    Returns
    -------
    List[Any]
        A list of ORM column objects from the model that correspond to the field names defined in the schema.
    """
    column_list = list(model.__table__.columns)
    if schema is not None:
        if isinstance(schema, list):
            schema_fields = schema
        else:
            schema_fields = schema.model_fields.keys()
        
        column_list = []
        for column_name in schema_fields:
            if hasattr(model, column_name):
                column_list.append(getattr(model, column_name))
    
    return column_list


def _extract_matching_columns_from_kwargs(model: Type[Base], kwargs: dict) -> List[Any]:
    if kwargs is not None:
        kwargs_fields = kwargs.keys()
        column_list = []
        for column_name in kwargs_fields:
            if hasattr(model, column_name):
                column_list.append(getattr(model, column_name))
    
    return column_list


def _extract_matching_columns_from_column_names(model: Type[Base], column_names: list) -> List[Any]:
    column_list = []
    for column_name in column_names:
        if hasattr(model, column_name):
            column_list.append(getattr(model, column_name))

    return column_list
