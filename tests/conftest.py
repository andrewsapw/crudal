import random
import string

import pytest
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Mapped, Session, mapped_column

from crudal.base_sync import DeclarativeCrudBase

engine = create_engine("sqlite://")
async_engine = create_async_engine(
    "sqlite+aiosqlite://",
)


class Person(DeclarativeCrudBase):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


@pytest.fixture()
def person_model():
    return Person


@pytest.fixture
def session():
    with Session(bind=engine) as session:
        yield session


@pytest.fixture
async def async_session():
    async with AsyncSession(bind=async_engine) as session:
        yield session


@pytest.fixture
def random_string(N: int = 10):
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(N)
    )


DeclarativeCrudBase.metadata.create_all(bind=engine)
