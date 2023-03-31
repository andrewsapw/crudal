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
    """Generate select statement with filters.

    Args:
        cls (t.Union[t.Any, t.Tuple]): table class
        offset (t.Optional[int], optional): number of rows to skip. Defaults to None.
        rows (t.Optional[int], optional): number of rows to return. Defaults to None.
        **kwargs: search filters

    Returns:
        Select: _description_
    """
    select_stmt = _select_stmt_fields(fields=cls, offset=offset, rows=rows)
    stmt = select_stmt.filter_by(**kwargs)
    return stmt


def all(cls) -> Select:
    """Generate select to return all items.

    Returns:
        Select: select statement
    """
    stmt = _select_stmt_fields(fields=cls)
    return stmt


def exists(cls, **kwargs) -> Select:
    """Generate select statement to check if item exists.

    Returns:
        Select: select statement
    """
    stmt = select(cls).filter_by(**kwargs)
    return stmt
