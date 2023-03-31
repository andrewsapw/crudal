from sqlalchemy.orm import Session

from crudal.base_sync import DeclarativeCrudBase


def test_add(sync_model, session: Session):
    p = sync_model(name="Andrew")
    p.add(session, commit=True)

    assert p in p.all(session)
    assert p in p.find(session, name="Andrew")
    assert p not in p.find(session, name="Not Andrew")


def test_add_many(sync_model, session: Session):
    p1 = sync_model(name="Andrew")
    p2 = sync_model(name="John")
    sync_model.add_many(session, items=[p1, p2], commit=True)

    assert p1 in sync_model.all(session)
    assert p2 in sync_model.all(session)


def test_delete(sync_model: DeclarativeCrudBase, session: Session):
    p = sync_model(name="Andrew")
    p.add(session, commit=True)
    assert p in sync_model.all(session)

    sync_model.delete(session, name="Andrew")

    assert p not in sync_model.all(session)
