import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from crudal import DeclarativeCrudBaseAsync


@pytest.mark.asyncio
async def test_find(
    async_model: DeclarativeCrudBaseAsync, async_session: AsyncSession
):
    p = async_model(name="Andrew")
    p = await p.add(async_session, commit=True)

    assert p in await p.all(async_session)
    assert p in await p.find(async_session, name="Andrew")
    assert p not in await p.find(async_session, name="Not Andrew")


@pytest.mark.asyncio
async def test_find_by_pk(async_model: DeclarativeCrudBaseAsync, async_session: AsyncSession):
    p = async_model(name="Andrew")
    p = await p.add(async_session, commit=True)

    item_id = p.id
    p_found = await async_model.find_by_pk(async_session, pk=item_id)
    assert p_found is not None
    assert p_found == p
