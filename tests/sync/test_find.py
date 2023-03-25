from conftest import Person
from sqlalchemy.orm import Session


def test_find(session: Session):
    p = Person(name="Andrew")
    p.add(session=session, commit=True)

    assert p in p.all(session=session)
    assert p in p.find(session=session, name="Andrew")
    assert p not in p.find(session=session, name="Not Andrew")


def test_find_by_pk(session: Session):
    p = Person(name="Andrew")
    p.add(session=session, commit=True)

    item_id = p.id
    p_found = Person.find_by_pk(session=session, pk=item_id)
    assert p_found is not None
    assert p_found == p
