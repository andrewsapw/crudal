# CRUDAL

Ready to use CRUD methods for SQLAlchemy models. Both *Sync* and *Async*

```
pip install crudal
```

# Examples



## Sync


### Model initialization

```python
from crudal import DeclarativeCrudBase

from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

engine = create_engine("sqlite://")
SessionLocal = sessionmaker(engine, expire_on_commit=False)


class User(DeclarativeCrudBase):
    __tablename__ = "person"
    __session__ = sessionmaker(engine, expire_on_commit=False)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


DeclarativeCrudBase.metadata.create_all(bind=engine)
```
### Add new item

```python
user = User(name="Andrew")
user.add()
```

### Find item

Find all users with name equals *Andrew*
```python
users_found = User.find(name="Andrew")
for u in users_found:
    assert u.name == "Andrew" 
```

### Update item

Change name of all users with name *Andrew* to *John* 

```python
User.update(session=session, values=dict(name="John"), name="Andrew")
```

### Delete item

```python
User.delete(name="John")
```

## Async



```python
from crudal import DeclarativeCrudBaseAsync

from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import Mapped, Session, mapped_column


class User(DeclarativeCrudBaseAsync):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

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
