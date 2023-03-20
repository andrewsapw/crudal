import typing as t

from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import ScalarResult

from crudal import operations

_T = t.TypeVar("_T")


def _execute_crud_stmt(stmt, session: Session) -> ScalarResult:
    return session.scalars(stmt)


class DeclarativeCrudBase(DeclarativeBase):
    @classmethod
    def find(cls: t.Type[_T], session: Session, **filters) -> t.Sequence[_T]:
        stmt = operations.find(cls, **filters)
        result = _execute_crud_stmt(stmt, session=session)
        return result.all()

    @classmethod
    def exists(cls, session: Session, **filters) -> bool:
        stmt = operations.find(cls, **filters)
        result = _execute_crud_stmt(stmt, session=session)
        return True if result.first() is not None else False

    @classmethod
    def all(cls: t.Type[_T], session: Session) -> t.Sequence[_T]:
        stmt = operations.find(cls)
        result = _execute_crud_stmt(stmt, session=session)
        return result.all()

    @classmethod
    def delete(cls, session: Session, **filters) -> bool:
        exists = cls.exists(session=session, **filters)
        if not exists:
            return False

        delete_stmt = operations.delete_(cls=cls, **filters)
        session.execute(delete_stmt)
        return True
