import random
import string

import pytest
import pytest_asyncio
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, Session, mapped_column, sessionmaker

from crudal import DeclarativeCrudBase, DeclarativeCrudBaseAsync

engine = create_engine("sqlite://")
SessionLocal = sessionmaker(engine, expire_on_commit=False)


async_engine = create_async_engine(
    "sqlite+aiosqlite://",
)
SessionLocalAsync = async_sessionmaker(async_engine, expire_on_commit=False)


class Person(DeclarativeCrudBase):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class PersonSession(Person):
    __session__ = SessionLocal


class PersonAsync(DeclarativeCrudBaseAsync):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class PersonAsyncSession(PersonAsync):
    __session__ = SessionLocalAsync


@pytest.fixture()
def async_model():
    return PersonAsync


@pytest.fixture()
def async_model_ws():
    """Async model with session"""
    return PersonAsyncSession


@pytest.fixture()
def sync_model():
    return Person


@pytest.fixture()
def sync_model_ws():
    """Sync model with session"""
    return PersonSession


@pytest.fixture
def session():
    with Session(bind=engine) as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def async_session():
    async with async_engine.begin() as conn:
        await conn.run_sync(DeclarativeCrudBaseAsync.metadata.create_all)

    async with SessionLocalAsync() as session:
        yield session


@pytest.fixture
def random_string(N: int = 10):
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(N)
    )


DeclarativeCrudBase.metadata.create_all(bind=engine)
