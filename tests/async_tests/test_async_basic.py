import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from crudal.base_async import DeclarativeCrudBaseAsync


@pytest.mark.asyncio
async def test_add(async_model: DeclarativeCrudBaseAsync, async_session: AsyncSession):
    p = async_model(name="Andrew")
    p = await p.add(async_session, commit=True)

    assert p in await p.all(async_session)
    assert p in await p.find(async_session, name="Andrew")
    assert p not in await p.find(async_session, name="Not Andrew")


@pytest.mark.asyncio
async def test_add_many(
    async_model: DeclarativeCrudBaseAsync, async_session: AsyncSession
):
    p1 = async_model(name="Andrew")
    p2 = async_model(name="John")
    await async_model.add_many(async_session, items=[p1, p2], commit=True)

    assert p1 in await async_model.all(async_session)
    assert p2 in await async_model.all(async_session)


@pytest.mark.asyncio
async def test_delete(
    async_model: DeclarativeCrudBaseAsync, async_session: AsyncSession
):
    p = async_model(name="Andrew")
    await p.add(async_session, commit=True)
    assert p in await async_model.all(async_session)

    await async_model.delete(async_session, name="Andrew")

    assert p not in await async_model.all(async_session)
