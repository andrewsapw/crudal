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
    def _get_primary_key(cls):
        return inspect(cls).primary_key[0].name

    @classmethod
    async def find(cls: t.Type[_T], session: AsyncSession, **filters) -> t.Sequence[_T]:
        stmt = operations.find(cls, **filters)
        result = await _execute_crud_stmt(stmt, session=session)
        return result.all()

    @classmethod
    async def find_by_pk(
        cls: t.Type[_T], session: AsyncSession, pk: t.Any
    ) -> t.Optional[_T]:
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
        stmt = operations.find(cls, **filters)
        result = await _execute_crud_stmt(stmt, session=session)
        return True if result.first() is not None else False

    @classmethod
    async def all(cls: t.Type[_T], session: AsyncSession) -> t.Sequence[_T]:
        stmt = operations.find(cls)
        result = await _execute_crud_stmt(stmt, session=session)
        return result.all()

    @classmethod
    async def delete(cls, session: AsyncSession, **filters) -> bool:
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
        session.add_all(items)

    async def add(self, session: AsyncSession, commit: bool = False) -> None:
        session.add(self)
        if commit:
            await session.commit()

        return
