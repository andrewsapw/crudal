import typing as t

from sqlalchemy import select


def _select_stmt_fields(
    fields, rows: t.Optional[int] = None, offset: t.Optional[int] = None
):
    if isinstance(t, tuple) or isinstance(t, list):
        stmt = select(*fields)
    else:
        stmt = select(fields)

    if offset is not None:
        stmt = stmt.offset(offset)

    if rows is not None:
        stmt = stmt.limit(rows)

    return stmt
