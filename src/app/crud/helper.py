from typing import Any

from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql.elements import Label
from sqlalchemy.sql.schema import Column

from ..core.db.database import Base


def _extract_matching_columns_from_schema(model: type[Base], schema: type[BaseModel] | list | None) -> list[Any]:
    """Retrieves a list of ORM column objects from a SQLAlchemy model that match the field names in a given
    Pydantic schema.

    Parameters
    ----------
    model: Type[Base]
        The SQLAlchemy ORM model containing columns to be matched with the schema fields.
    schema: Type[BaseModel]
        The Pydantic schema containing field names to be matched with the model's columns.

    Returns
    -------
    list[Any]
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


def _extract_matching_columns_from_kwargs(model: type[Base], kwargs: dict) -> list[Any]:
    if kwargs is not None:
        kwargs_fields = kwargs.keys()
        column_list = []
        for column_name in kwargs_fields:
            if hasattr(model, column_name):
                column_list.append(getattr(model, column_name))

    return column_list


def _extract_matching_columns_from_column_names(model: type[Base], column_names: list) -> list[Any]:
    column_list = []
    for column_name in column_names:
        if hasattr(model, column_name):
            column_list.append(getattr(model, column_name))

    return column_list


def _auto_detect_join_condition(
    base_model: type[DeclarativeMeta], join_model: type[DeclarativeMeta]
) -> ColumnElement | None:
    """Automatically detects the join condition for SQLAlchemy models based on foreign key relationships. This
    function scans the foreign keys in the base model and tries to match them with columns in the join model.

    Parameters
    ----------
    base_model : Type[DeclarativeMeta]
        The base SQLAlchemy model from which to join.
    join_model : Type[DeclarativeMeta]
        The SQLAlchemy model to join with the base model.

    Returns
    -------
    Optional[ColumnElement]
        A SQLAlchemy ColumnElement representing the join condition, if successfully detected.

    Raises
    ------
    ValueError
        If the join condition cannot be automatically determined, a ValueError is raised.

    Example
    -------
    # Assuming User has a foreign key reference to Tier:
    join_condition = auto_detect_join_condition(User, Tier)
    """
    fk_columns = [col for col in inspect(base_model).c if col.foreign_keys]
    join_on = next(
        (
            base_model.__table__.c[col.name] == join_model.__table__.c[list(col.foreign_keys)[0].column.name]
            for col in fk_columns
            if list(col.foreign_keys)[0].column.table == join_model.__table__
        ),
        None,
    )

    if join_on is None:
        raise ValueError("Could not automatically determine join condition. Please provide join_on.")

    return join_on


def _add_column_with_prefix(column: Column, prefix: str | None) -> Label:
    """Creates a SQLAlchemy column label with an optional prefix.

    Parameters
    ----------
    column : Column
        The SQLAlchemy Column object to be labeled.
    prefix : Optional[str]
        An optional prefix to prepend to the column's name.

    Returns
    -------
    Label
        A labeled SQLAlchemy Column object.
    """
    column_label = f"{prefix}{column.name}" if prefix else column.name
    return column.label(column_label)
