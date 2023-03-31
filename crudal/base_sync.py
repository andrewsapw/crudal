import typing as t

from sqlalchemy import Result, ScalarResult
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, Session

from crudal import operations
from crudal.types import CRUDALType
from crudal.utils import with_session_sync

_T = t.TypeVar("_T", bound=CRUDALType)


def _crud_stmt_scalars(stmt, session: Session) -> ScalarResult:
    return session.scalars(stmt)


def _crud_stmt_execute(stmt, session: Session) -> Result:
    return session.execute(stmt)


class DeclarativeCrudBase(DeclarativeBase):
    __session__ = None

    @classmethod
    def _get_primary_key(cls):
        """Return PK column name"""
        return inspect(cls).primary_key[0].name

    @classmethod
    @with_session_sync
    def find(
        cls: t.Type[_T],
        session: Session,
        /,
        *,
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
    @with_session_sync
    def find_by_pk(
        cls: t.Type[_T], session: Session, /, *, pk: t.Any
    ) -> t.Optional[_T]:
        """Find row by its primary key

        Example:
        ```
        # find user with id 1
        User.find_by_pk(session=session, pk=1)
        ```

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
        result = cls.find(session, **{pk_col: pk})
        if len(result) == 1:
            return result[0]
        elif len(result) > 1:
            raise ValueError(
                f"Found more than one items ({len(result)}) with {pk_col}={pk}"
            )
        else:
            return None

    @classmethod
    @with_session_sync
    def exists(cls, session: Session, /, **filters) -> bool:
        """Check if items exists in table

        Example:
        ```
        # check if user with name Andrew exists
        User.exists(session, name="Andrew")
        ```

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
    @with_session_sync
    def all(cls: t.Type[_T], session: Session, /) -> t.Sequence[_T]:
        """Get all table items

        Example:
        ```
        # get all users
        User.all(session)
        ```

        Args:
            session (Session): SQLAlchemy session

        Returns:
            t.Sequence[_T]: Found items
        """
        stmt = operations.find(cls)
        result = _crud_stmt_scalars(stmt, session=session)
        return result.all()

    @classmethod
    @with_session_sync
    def delete(cls, session: Session, /, *, commit: bool = False, **filters) -> bool:
        """Delete items from table

        Example:
        ```
        # delete all users with name Andrew
        User.delete(session, name="Andrew")
        ```

        Args:
            session (Session): SQLAlchemy session
            commit (bool, optional): Commit or not. Defaults to False.
            **filters: search filters

        Returns:
            bool: True if deleted, False if not
        """
        exists = cls.exists(session, **filters)
        if not exists:
            return False

        delete_stmt = operations.delete_(cls=cls, **filters)
        session.execute(delete_stmt)
        if commit:
            session.commit()

        return True

    @classmethod
    @with_session_sync
    def add_many(
        cls: t.Type[_T], session: Session, /, *, items: t.List[_T], commit: bool = False
    ) -> None:
        """Add many new items to table

        Example:
        ```
        # add new users
        User.add_many(session, items=[User(name="Andrew"), User(name="John")])
        ```

        Args:
            session (Session): SQLAlchemy session
            items (t.List[_T]): items to add
            commit (bool, optional): Commit or not. Defaults to False.

        """
        session.add_all(items)
        if commit:
            session.commit()

    @with_session_sync
    def add(self: _T, session: Session, /, *, commit: bool = False) -> _T:
        """Add one item to table.

        Example:
        ```
        # add new user
        User(name="Andrew").add(session)
        ```

        Args:
            session (Session): SQLAlchemy async session
            commit (bool, optional): Commit or not. Defaults to False.
        """
        session.add(self)
        if commit:
            session.commit()

        return self

    @classmethod
    @with_session_sync
    def update(
        cls: t.Type[_T], session: Session, /, *, values: dict, **filters
    ) -> t.Type[_T]:
        """Update table items values

        Example:
        ```
        # update all users with name Andrew to name John
        User.update(session, values={"name": "John"}, name="Andrew")
        ```

        Args:
            session (Session): SQLAlchemy session
            values (dict): values to update
            **filters: search filters

        Returns:
            t.Type[_T]: updated item

        """
        stmt = operations.update_(cls, values=values, **filters)
        return _crud_stmt_execute(stmt=stmt, session=session)
