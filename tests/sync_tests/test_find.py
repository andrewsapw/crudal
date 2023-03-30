from sqlalchemy.orm import Session


def test_find(sync_model, session: Session):
    p = sync_model(name="Andrew")
    p.add(session=session, commit=True)

    assert p in p.all(session=session)
    assert p in p.find(session=session, name="Andrew")
    assert p not in p.find(session=session, name="Not Andrew")


def test_find_by_pk(sync_model, session: Session):
    p = sync_model(name="Andrew")
    p.add(session=session, commit=True)

    item_id = p.id
    p_found = sync_model.find_by_pk(session=session, pk=item_id)
    assert p_found is not None
    assert p_found == p
