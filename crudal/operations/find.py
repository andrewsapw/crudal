import typing as t

from sqlalchemy import Select, select

from .base import _select_stmt_fields

_T = t.TypeVar("_T")


def find(
    cls: t.Union[t.Any, t.Tuple],
    offset: t.Optional[int] = None,
    rows: t.Optional[int] = None,
    **kwargs
) -> Select:
    select_stmt = _select_stmt_fields(fields=cls, offset=offset, rows=rows)
    stmt = select_stmt.filter_by(**kwargs)
    return stmt


def all(cls):
    stmt = _select_stmt_fields(fields=cls)
    return stmt


def exists(cls, **kwargs):
    stmt = select(cls).filter_by(**kwargs)
    return stmt
