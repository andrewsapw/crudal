import pytest
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import Mapped, Session, mapped_column

from crudal.base import DeclarativeCrudBase

engine = create_engine("sqlite://")


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


DeclarativeCrudBase.metadata.create_all(bind=engine)
