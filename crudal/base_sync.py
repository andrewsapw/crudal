import typing as t

from sqlalchemy import Result, ScalarResult
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, Session

from crudal import operations
from crudal.types import CRUDALType

_T = t.TypeVar("_T", bound=CRUDALType)


def _crud_stmt_scalars(stmt, session: Session) -> ScalarResult:
    return session.scalars(stmt)


def _crud_stmt_execute(stmt, session: Session) -> Result:
    return session.execute(stmt)


class DeclarativeCrudBase(DeclarativeBase):
    @classmethod
    def _get_primary_key(cls):
        """Return PK column name"""
        return inspect(cls).primary_key[0].name

    @classmethod
    def find(
        cls: t.Type[_T],
        session: Session,
        rows: t.Optional[int] = None,
        offset: int = 0,
        **filters,
    ) -> t.Sequence[_T]:
        """Find items in table.

        Example:
        ```
        # find all users with name Andrew
        User.find(session=session, name="Andrew")
        ```

        Args:
            session (Session): SQLAlchemy session
            rows(int, optional): Number of rows to return. Defaults to None.
            offset(int, optional): Number of rows to skip. Defaults to 0.
            **filters: search filters

        Returns:
            t.Sequence[_T]: Found items
        """
        stmt = operations.find(cls, offset=offset, rows=rows, **filters)
        result = _crud_stmt_scalars(stmt, session=session)
        return result.all()

    @classmethod
    def find_by_pk(cls: t.Type[_T], session: Session, pk: t.Any) -> t.Optional[_T]:
        """Find row by its primary key

        Args:
            session (Session): SQLAlchemy session
            pk (t.Any): primary key value

        Raises:
            ValueError: Multiple rows found by one primary key

        Returns:
            t.Optional[_T]: found item.
                If None - no items with such primary keys exists
        """
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
        """Check if items exists in table

        Args:
            session (AsyncSession): SQLAlchemy session
            **filters: search filters

        Returns:
            bool: True if exists, False if not
        """
        stmt = operations.find(cls, **filters)
        result = _crud_stmt_scalars(stmt, session=session)
        return True if result.first() is not None else False

    @classmethod
    def all(cls: t.Type[_T], session: Session) -> t.Sequence[_T]:
        """Get all table items"""
        stmt = operations.find(cls)
        result = _crud_stmt_scalars(stmt, session=session)
        return result.all()

    @classmethod
    def delete(cls, session: Session, **filters) -> bool:
        """Delete items from table"""
        exists = cls.exists(session=session, **filters)
        if not exists:
            return False

        delete_stmt = operations.delete_(cls=cls, **filters)
        session.execute(delete_stmt)
        return True

    @classmethod
    def add_many(cls: t.Type[_T], session: Session, items: t.List[_T]) -> None:
        """Add many new items to table"""
        session.add_all(items)

    def add(self: _T, session: Session, commit: bool = False) -> _T:
        """Add one item to table.

        Args:
            session (Session): SQLAlchemy async session
            commit (bool, optional): Commit or not. Defaults to False.
        """
        session.add(self)
        if commit:
            session.commit()

        return self

    @classmethod
    def update(cls: t.Type[_T], session: Session, values: dict, **filters):
        """Update table items values"""
        stmt = operations.update_(cls, values=values, **filters)
        return _crud_stmt_execute(stmt=stmt, session=session)
