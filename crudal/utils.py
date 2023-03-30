import typing as t
from functools import wraps


def with_session_sync(f: t.Callable):
    @wraps(f)
    def wrapper(ref, session=None, **kwargs):
        if session is not None:
            return f(ref, session, **kwargs)
        elif session is None and ref.__session__ is not None:
            with ref.__session__() as session:
                return f(ref, session, **kwargs)
        else:
            raise ValueError("Neither function session or class session exists")

    return wrapper


def with_session_async(f: t.Callable):
    @wraps(f)
    async def wrapper(ref, session=None, **kwargs):
        if session is not None:
            return await f(ref, session, **kwargs)
        elif session is None and ref.__session__ is not None:
            async with ref.__session__() as session:
                return await f(ref, session, **kwargs)

        else:
            raise ValueError("Neither function session or class session exists")

    return wrapper
