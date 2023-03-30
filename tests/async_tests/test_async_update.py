import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from crudal import DeclarativeCrudBaseAsync


@pytest.mark.asyncio
async def test_async_update(
    async_model: DeclarativeCrudBaseAsync, async_session: AsyncSession
):
    p = async_model(name="AndrewSON")
    p = await p.add(async_session, commit=True)

    assert p in (await p.all(async_session))

    new_name = "AndrewSON new Name"
    new_values = dict(name=new_name)
    await async_model.update(async_session, values=new_values, name="AndrewSON")

    p_new = await async_model.find(async_session, name=new_name)

    assert len(p_new) == 1
    assert p.id == p_new[0].id
