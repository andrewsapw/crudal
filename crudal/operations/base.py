import typing as t

from sqlalchemy import select


def _select_stmt_fields(fields):
    if isinstance(t, tuple) or isinstance(t, list):
        stmt = select(*fields)
    else:
        stmt = select(fields)

    return stmt
