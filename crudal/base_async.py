import typing as t

from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase

from crudal import operations
from crudal.types import CRUDALTypeAsync

_T = t.TypeVar("_T", bound=CRUDALTypeAsync)


async def _execute_crud_stmt(stmt, session: AsyncSession) -> ScalarResult:
    return await session.scalars(stmt)


class DeclarativeCrudBaseAsync(DeclarativeBase):
    @classmethod
    def _get_primary_key(cls) -> str:
        """Return PK column name"""
        return inspect(cls).primary_key[0].name

    @classmethod
    async def find(
        cls: t.Type[_T],
        session: AsyncSession,
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
            session (AsyncSession): SQLAlchemy session
            rows(int, optional): Number of rows to return. Defaults to None.
            offset(int, optional): Number of rows to skip. Defaults to 0.
            **filters: search filters

        Returns:
            t.Sequence[_T]: Found items
        """
        stmt = operations.find(cls, offset=offset, rows=rows, **filters)
        result = await _execute_crud_stmt(stmt, session=session)
        return result.all()

    @classmethod
    async def find_by_pk(
        cls: t.Type[_T], session: AsyncSession, pk: t.Any
    ) -> t.Optional[_T]:
        """Find row by its primary key

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
        result = await cls.find(session=session, **{pk_col: pk})
        if len(result) == 1:
            return result[0]
        elif len(result) > 1:
            raise ValueError(
                f"Found more than one items ({len(result)}) with {pk_col}={pk}"
            )
        else:
            return None

    @classmethod
    async def exists(cls, session: AsyncSession, **filters) -> bool:
        """Check if items exists in table

        Args:
            session (AsyncSession): SQLAlchemy session
            **filters: search filters

        Returns:
            bool: True if exists, False if not
        """
        stmt = operations.find(cls, **filters)
        result = await _execute_crud_stmt(stmt, session=session)
        return True if result.first() is not None else False

    @classmethod
    async def all(cls: t.Type[_T], session: AsyncSession) -> t.Sequence[_T]:
        """Get all table items"""
        stmt = operations.find(cls)
        result = await _execute_crud_stmt(stmt, session=session)
        return result.all()

    @classmethod
    async def delete(cls, session: AsyncSession, **filters) -> bool:
        """Delete items from table"""
        exists = cls.exists(session=session, **filters)
        if not exists:
            return False

        delete_stmt = operations.delete_(cls=cls, **filters)
        await session.execute(delete_stmt)
        return True

    @classmethod
    async def add_many(
        cls: t.Type[_T], session: AsyncSession, items: t.List[_T]
    ) -> None:
        """Add many new items to table"""
        session.add_all(items)

    async def add(self: _T, session: AsyncSession, commit: bool = False) -> _T:
        """Add one item to table.

        Args:
            session (AsyncSession): SQLAlchemy async session
            commit (bool, optional): Commit or not. Defaults to False.
        """
        session.add(self)
        if commit:
            await session.commit()

        return self

    @classmethod
    async def update(cls: t.Type[_T], session: AsyncSession, values: dict, **filters):
        """Update table items values"""
        stmt = operations.update_(cls, values=values, **filters)
        return await _execute_crud_stmt(stmt=stmt, session=session)
