from sqlalchemy import Update, update


def update_(cls, values: dict, **filters) -> Update:
    """Generate update statement

    Args:
        values (dict): values to update

    Returns:
        Update: update statement
    """
    stmt = update(cls).filter_by(**filters).values(**values)
    return stmt
