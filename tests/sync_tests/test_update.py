from sqlalchemy.orm import Session


def test_update(sync_model, session: Session, random_string):
    p = sync_model(name="AndrewSON")
    p = p.add(session, commit=True)

    assert p in p.all(session)

    new_name = random_string
    new_values = dict(name=new_name)
    sync_model.update(session, values=new_values, name="AndrewSON")

    p_new = sync_model.find(session, name=new_name)

    assert len(p_new) == 1
    assert p.id == p_new[0].id
