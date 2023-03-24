import typing as t

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

_T = t.TypeVar("_T")


class CRUDALType(t.Protocol):
    @classmethod
    def _get_primary_key(cls) -> str:
        """Table primary key"""
        raise NotImplementedError()

    @classmethod
    def find(cls: t.Type[_T], session: Session, **filters) -> t.Sequence[_T]:
        """Find items"""
        raise NotImplementedError()

    @classmethod
    def find_by_pk(cls: t.Type[_T], pk: t.Any, session: Session) -> t.Optional[_T]:
        raise NotImplementedError()

    @classmethod
    def exists(cls, session: Session, **filters) -> bool:
        raise NotImplementedError()

    @classmethod
    def all(cls: t.Type[_T], session: Session) -> t.Sequence[_T]:
        raise NotImplementedError()

    @classmethod
    def delete(cls, session: Session, **filters) -> bool:
        raise NotImplementedError()

    @classmethod
    def add_many(cls: t.Type[_T], session: Session, items: t.List[_T]) -> None:
        raise NotImplementedError()

    def add(self, session: Session, commit: bool = False) -> None:
        raise NotImplementedError()


class CRUDALTypeAsync(t.Protocol):
    @classmethod
    def _get_primary_key(cls) -> str:
        """Table primary key"""
        raise NotImplementedError()

    @classmethod
    async def find(cls: t.Type[_T], session: AsyncSession, **filters) -> t.Sequence[_T]:
        """Find items"""
        raise NotImplementedError()

    @classmethod
    async def find_by_pk(
        cls: t.Type[_T], pk: t.Any, session: AsyncSession
    ) -> t.Optional[_T]:
        raise NotImplementedError()

    @classmethod
    async def exists(cls, session: AsyncSession, **filters) -> bool:
        raise NotImplementedError()

    @classmethod
    async def all(cls: t.Type[_T], session: AsyncSession) -> t.Sequence[_T]:
        raise NotImplementedError()

    @classmethod
    async def delete(cls, session: AsyncSession, **filters) -> bool:
        raise NotImplementedError()

    @classmethod
    async def add_many(
        cls: t.Type[_T], session: AsyncSession, items: t.List[_T]
    ) -> None:
        raise NotImplementedError()

    async def add(self, session: AsyncSession, commit: bool = False) -> None:
        raise NotImplementedError()
