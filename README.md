# CRUDAL

Ready to use CRUD methods for SQLAlchemy models. Both *Sync* and *Async*

```
pip install crudal
```

# Examples

```python

from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import Mapped, Session, mapped_column

from crudal import DeclarativeCrudBase

engine = create_engine("sqlite://")

class User(DeclarativeCrudBase):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

DeclarativeCrudBase.metadata.create_all(bind=engine)
```

## Find

```python

with Session(bind=engine) as session:
    p = User(name="Andrew")
    p.add(session=session)

    p2 = User(name="Bob")
    p2.add(session=session)

    # find person with name "Andrew"
    andrew = User.find(session=session, name="Andrew")

    all_users = User.all(session=session)

    for u in all_users:
      print(u.name)

```


###
