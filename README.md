# CRUDAL

Ready to use CRUD methods for SQLAlchemy models

```
pip install crudal
```

## Features

Sync:
- [ ] Find
- [ ] Find by primary key
- [ ] Add
- [ ] Add many
- [ ] Delete
- [ ] Update

Async:
- [ ] Find
  - [ ] with options
- [ ] Find by primary key
- [ ] Add
- [ ] Add many
- [ ] Delete
- [ ] Update


## Usage

```python

from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import Mapped, Session, mapped_column

from crudal import DeclarativeCrudBase

engine = create_engine("sqlite://")

class Person(DeclarativeCrudBase):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

 with Session(bind=engine) as session:
    p = Person(name="Andrew")
    p.add(session=session)

    p_found = Person.find(session=session, name="Andrew")

```
