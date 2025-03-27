from typing import Any, Callable, List, Protocol, TypeVar, Union

T = TypeVar('T')
MaybeArray = Union[T, List[T]]

class Guard(Protocol[T]):
    """
    Функция для проверки условия
    """
    def __call__(self, value: T) -> bool: 
        ... 