import typing as t

from sqlalchemy import select
from sqlalchemy import Select


from sqlalchemy.orm import DeclarativeBase

from .base import _select_stmt_fields

_T = t.TypeVar("_T")


def find(cls: t.Union[t.Any, t.Tuple], **kwargs) -> Select:
    select_stmt = _select_stmt_fields(fields=cls)
    stmt = select_stmt.filter(**kwargs)
    return stmt


def all(cls):
    stmt = _select_stmt_fields(fields=cls)
    return stmt


def exists(cls, **kwargs):
    stmt = select(cls).filter(**kwargs)
    return stmt
