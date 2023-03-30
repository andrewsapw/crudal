from crudal import DeclarativeCrudBase


def test_is_add(sync_model_ws: DeclarativeCrudBase):
    p = sync_model_ws(name="Andrew")
    p = p.add(commit=True)

    assert p.id in [i.id for i in p.all()]
    assert p.id in [i.id for i in p.find(name="Andrew")]
    assert p.id not in [i.id for i in p.find(name="Not Andrew")]


def test_is_delete(sync_model_ws: DeclarativeCrudBase):
    p = sync_model_ws(name="Andrew")
    p = p.add(commit=True)

    assert p.id in [i.id for i in sync_model_ws.all()]

    sync_model_ws.delete(name="Andrew", commit=True)

    assert p.id not in [i.id for i in sync_model_ws.all()]
