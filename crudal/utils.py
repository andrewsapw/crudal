import typing as t
from functools import wraps

from crudal.types import CRUDALType

T = t.TypeVar("T", bound=CRUDALType)
_RT = t.TypeVar("_RT")  # return type
P = t.ParamSpec("P")


def with_session_sync(f: t.Callable[P, _RT]) -> t.Callable[P, _RT]:
    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        ref = args[0]
        if len(args) >= 2:
            session = args[1]
        else:
            session = None

        if session is not None:
            return f(ref, session, **kwargs)
        elif session is None and ref.__session__ is not None:
            with ref.__session__() as session:
                return f(ref, session, **kwargs)
        else:
            raise ValueError("Neither function session or class session exists")

    return wrapper


def with_session_async(f: t.Callable[P, _RT]) -> t.Callable[P, _RT]:
    @wraps(f)
    async def wrapper(*args: P.args, **kwargs: P.kwargs):
        ref = args[0]
        if len(args) >= 2:
            session = args[1]
        else:
            session = None

        if session is not None:
            return await f(ref, session, **kwargs)
        elif session is None and ref.__session__ is not None:
            async with ref.__session__() as session:
                return await f(ref, session, **kwargs)

        else:
            raise ValueError("Neither function session or class session exists")

    return wrapper
