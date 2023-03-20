import typing as t

from sqlalchemy import select
from sqlalchemy import Select


from sqlalchemy.orm import DeclarativeBase

_T = t.TypeVar("_T")


def find(cls: t.Union[t.Any, t.Tuple], **kwargs) -> Select:
    if isinstance(t, tuple) or isinstance(t, list):
        stmt = select(*cls).filter(**kwargs)
    else:
        stmt = select(cls).filter(**kwargs)

    return stmt


def all(cls, **kwargs):
    stmt = select(cls)
    return stmt


def exists(cls, **kwargs):
    stmt = select(cls).filter(**kwargs)
    return stmt
