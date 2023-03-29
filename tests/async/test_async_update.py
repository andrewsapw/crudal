import pytest
from conftest import PersonAsync, async_engine
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_async_update():
    async with AsyncSession(bind=async_engine) as async_session:
        p = PersonAsync(name="AndrewSON")
        p = await p.add(async_session, commit=True)

        assert p in (await p.all(async_session))

        new_name = "AndrewSON new Name"
        new_values = dict(name=new_name)
        await PersonAsync.update(async_session, values=new_values, name="AndrewSON")

        p_new = await PersonAsync.find(async_session, name=new_name)

        assert len(p_new) == 1
        assert p.id == p_new[0].id
