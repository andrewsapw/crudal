import pytest

from crudal.base_async import DeclarativeCrudBaseAsync


@pytest.mark.asyncio
async def test_is_add(async_model_ws: DeclarativeCrudBaseAsync):
    p = async_model_ws(name="Andrew")
    p = await p.add(commit=True)

    assert p.id in [i.id for i in await p.all()]
    assert p.id in [i.id for i in await p.find(name="Andrew")]
    assert p.id not in [i.id for i in await p.find(name="Not Andrew")]


@pytest.mark.asyncio
async def test_is_delete(async_model_ws: DeclarativeCrudBaseAsync):
    p = async_model_ws(name="Andrew")
    p = await p.add(commit=True)

    assert p.id in [i.id for i in await async_model_ws.all()]

    await async_model_ws.delete(name="Andrew", commit=True)

    assert p.id not in [i.id for i in await async_model_ws.all()]
