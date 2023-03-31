import typing as t

from sqlalchemy import Result, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase

from crudal import operations
from crudal.types import CRUDALTypeAsync
from crudal.utils import with_session_async

_T = t.TypeVar("_T", bound=CRUDALTypeAsync)


async def _crud_stmt_scalars(stmt, session: AsyncSession) -> ScalarResult:
    return await session.scalars(stmt)


async def _crud_stmt_execute(stmt, session: AsyncSession) -> Result:
    return await session.execute(stmt)


class DeclarativeCrudBaseAsync(DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}
    __session__ = None

    @classmethod
    def _get_primary_key(cls) -> str:
        """Return PK column name"""
        return inspect(cls).primary_key[0].name

    @classmethod
    @with_session_async
    async def find(
        cls: t.Type[_T],
        session: AsyncSession,
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
        await User.find(session, name="Andrew")
        ```

        Args:
            session (AsyncSession): SQLAlchemy session
            rows(int, optional): Number of rows to return. Defaults to None.
            offset(int, optional): Number of rows to skip. Defaults to 0.
            **filters: search filters

        Returns:
            t.Sequence[_T]: Found items
        """
        stmt = operations.find(cls, offset=offset, rows=rows, **filters)
        result = await _crud_stmt_scalars(stmt, session=session)
        return result.all()

    @classmethod
    @with_session_async
    async def find_by_pk(
        cls: t.Type[_T], session: AsyncSession, /, *, pk: t.Any
    ) -> t.Optional[_T]:
        """Find row by its primary key

        Example:
        ```
        # find user with id 1
        await User.find_by_pk(session, pk=1)
        ```

        Args:
            session (AsyncSession): SQLAlchemy session
            pk (t.Any): primary key value

        Raises:
            ValueError: Multiple rows found by one primary key

        Returns:
            t.Optional[_T]: found item.
                If None - no items with such primary keys exists
        """
        pk_col = cls._get_primary_key()
        result = await cls.find(session, **{pk_col: pk})
        if len(result) == 1:
            return result[0]
        elif len(result) > 1:
            raise ValueError(
                f"Found more than one items ({len(result)}) with {pk_col}={pk}"
            )
        else:
            return None

    @classmethod
    @with_session_async
    async def exists(cls, session: AsyncSession, /, **filters) -> bool:
        """Check if items exists in table

        Example:
        ```
        # check if user with name Andrew exists
        await User.exists(session, name="Andrew")
        ```

        Args:
            session (AsyncSession): SQLAlchemy session
            **filters: search filters

        Returns:
            bool: True if exists, False if not
        """
        stmt = operations.find(cls, **filters)
        result = await _crud_stmt_scalars(stmt, session=session)
        return True if result.first() is not None else False

    @classmethod
    @with_session_async
    async def all(cls: t.Type[_T], session: AsyncSession, /) -> t.Sequence[_T]:
        """Get all table items

        Example:
        ```
        # get all users
        await User.all(session)
        ```

        Args:
            session (AsyncSession): SQLAlchemy session

        Returns:
            t.Sequence[_T]: all table items

        """
        stmt = operations.find(cls)
        result = await _crud_stmt_scalars(stmt, session=session)
        return result.all()

    @classmethod
    @with_session_async
    async def delete(
        cls, session: AsyncSession, /, commit: bool = False, **filters
    ) -> bool:
        """Delete items from table

        Example:
        ```
        # delete all users with name Andrew
        await User.delete(session, name="Andrew")
        ```

        Args:
            session (AsyncSession): SQLAlchemy session
            commit (bool, optional): commit after deleting. Defaults to False.

        Returns:
            bool: _description_
        """
        exists = await cls.exists(session, **filters)
        if not exists:
            return False

        delete_stmt = operations.delete_(cls=cls, **filters)
        await session.execute(delete_stmt)

        if commit:
            await session.commit()

        return True

    @classmethod
    @with_session_async
    async def add_many(
        cls: t.Type[_T],
        session: AsyncSession,
        /,
        *,
        items: t.List[_T],
        commit: bool = False,
    ) -> None:
        """Add many new items to table

        Example:
        ```
        users = [User(name="Andrew"), User(name="Bob")]
        await User.add_many(session, items=users)
        ```

        Args:
            session (AsyncSession): SQLAlchemy session
            items (t.List[_T]): list of items to add
            commit (bool, optional): commit after adding. Defaults to False.
        """
        session.add_all(items)
        if commit:
            await session.commit()

    @with_session_async
    async def add(self: _T, session: AsyncSession, /, *, commit: bool = False) -> _T:
        """Add one item to table.

        Example:
        ```
        user = User(name="Andrew")
        await user.add(session)
        ```

        Args:
            session (AsyncSession): SQLAlchemy async session
            commit (bool, optional): Commit or not. Defaults to False.
        """
        session.add(self)
        if commit:
            await session.commit()
            await session.refresh(self)

        return self

    @classmethod
    async def update(
        cls: t.Type[_T], session: AsyncSession, /, *, values: dict, **filters
    ):
        """Update table items values

        Example:
        ```
        # update all users with name Andrew to name Bob
        await User.update(session, values={"name": "Bob"}, name="Andrew")
        ```

        Args:
            session (AsyncSession): SQLAlchemy session
            values (dict): values to update
            **filters: search filters
        """
        stmt = operations.update_(cls, values=values, **filters)
        return await _crud_stmt_execute(stmt=stmt, session=session)
