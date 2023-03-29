import typing as t
from functools import wraps


def with_session_async(f: t.Callable):
    @wraps(f)
    async def wrapper(session=None, **kwargs):
        ref = f.__self__

        if session is not None:
            return await f(ref, session, **kwargs)
        elif session is None and ref._session() is not None:
            return await f(ref, ref._session(), **kwargs)
        else:
            raise ValueError("Neither function session or class session exists")

    return wrapper
