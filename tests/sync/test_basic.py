from conftest import Person
from sqlalchemy.orm import Session


def test_add(session: Session):
    p = Person(name="Andrew")
    p.add(session=session, commit=True)

    assert p in p.all(session=session)
    assert p in p.find(session=session, name="Andrew")
    assert p not in p.find(session=session, name="Not Andrew")


def test_delete(session: Session):
    p = Person(name="Andrew")
    p.add(session=session, commit=True)
    assert p in Person.all(session=session)

    Person.delete(session=session, name="Andrew")

    assert p not in Person.all(session=session)
