from sqlalchemy.orm import Session

from crudal.base_sync import DeclarativeCrudBase


def test_add(sync_model, session: Session):
    p = sync_model(name="Andrew")
    p.add(session=session, commit=True)

    assert p in p.all(session=session)
    assert p in p.find(session=session, name="Andrew")
    assert p not in p.find(session=session, name="Not Andrew")


def test_delete(sync_model: DeclarativeCrudBase, session: Session):
    p = sync_model(name="Andrew")
    p.add(session, commit=True)
    assert p in sync_model.all(session)

    sync_model.delete(session, name="Andrew")

    assert p not in sync_model.all(session)
