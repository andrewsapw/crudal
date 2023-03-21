from sqlalchemy import delete
from sqlalchemy import Delete


def delete_(cls, **kwargs) -> Delete:
    stmt = delete(cls).filter_by(**kwargs)
    return stmt
