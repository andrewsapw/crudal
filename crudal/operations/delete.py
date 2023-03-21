from sqlalchemy import Delete, delete


def delete_(cls, **kwargs) -> Delete:
    stmt = delete(cls).filter_by(**kwargs)
    return stmt
