from sqlalchemy import Delete, delete


def delete_(cls, **kwargs) -> Delete:
    """Generate delete statement

    Returns:
        Delete: delete statement
    """
    stmt = delete(cls).filter_by(**kwargs)
    return stmt
