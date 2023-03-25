from sqlalchemy import Update, update


def update_(cls, values: dict, **filters) -> Update:
    stmt = update(cls).filter_by(**filters).values(**values)
    return stmt
