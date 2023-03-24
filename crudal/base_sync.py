import typing as t

from sqlalchemy import ScalarResult
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, Session

from crudal import operations
from crudal.types import CRUDALType

_T = t.TypeVar("_T", bound=CRUDALType)


def _execute_crud_stmt(stmt, session: Session) -> ScalarResult:
    return session.scalars(stmt)


class DeclarativeCrudBase(DeclarativeBase):
    @classmethod
    def _get_primary_key(cls):
        return inspect(cls).primary_key[0].name

    @classmethod
    def find(cls: t.Type[_T], session: Session, **filters) -> t.Sequence[_T]:
        stmt = operations.find(cls, **filters)
        result = _execute_crud_stmt(stmt, session=session)
        return result.all()

    @classmethod
    def find_by_pk(cls: t.Type[_T], session: Session, pk: t.Any) -> t.Optional[_T]:
        pk_col = cls._get_primary_key()
        result = cls.find(session=session, **{pk_col: pk})
        if len(result) == 1:
            return result[0]
        elif len(result) > 1:
            raise ValueError(
                f"Found more than one items ({len(result)}) with {pk_col}={pk}"
            )
        else:
            return None

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

    @classmethod
    def add_many(cls: t.Type[_T], session: Session, items: t.List[_T]) -> None:
        session.add_all(items)

    def add(self, session: Session, commit: bool = False) -> None:
        session.add(self)
        if commit:
            session.commit()
        return
