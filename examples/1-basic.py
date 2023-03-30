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

# add new user with name "Andrew"
user = User(name="Andrew")
user.add(commit=True)

# find all users with name "Andrew"
users_found = User.find(name="Andrew")
assert users_found

for u in users_found:
    assert u.name == "Andrew"

# Change name of all users with name "Andrew" to "John"
new_values = dict(name="John")
User.update(values=new_values, name="Andrew")

