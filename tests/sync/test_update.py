from conftest import Person
from sqlalchemy.orm import Session


def test_update(session: Session):
    p = Person(name="AndrewSON")
    p = p.add(session=session, commit=True)

    assert p in p.all(session=session)

    new_name = "AndrewSON new Name"
    new_values = dict(name=new_name)
    Person.update(session=session, values=new_values, name="AndrewSON")

    p_new = Person.find(session=session, name=new_name)

    assert len(p_new) == 1
    assert p.id == p_new[0].id
