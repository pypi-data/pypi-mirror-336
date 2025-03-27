from typing import Awaitable, Callable, Protocol, TypeVar, Union

from .context import Context

C = TypeVar('C', bound=Context)
NextFn = Callable[[], Awaitable[None]]
MiddlewareFn = Callable[[C, NextFn], Awaitable[None]]

class MiddlewareObj(Protocol[C]):
    def middleware(self) -> MiddlewareFn[C]:
        ...

Middleware = Union[MiddlewareFn[C], MiddlewareObj[C]] 