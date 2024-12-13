from .option import Option
from typing import TypeVar, Callable

T = TypeVar('T')
R = TypeVar('R')

class NoneType(Option[T]):
    """
    Represents the absence of a value.
    
    Inherits from `Option` and overrides methods to control behavior for a None value.
    
    Methods:
    - `is_some()`: Returns False.
    - `is_none()`: Returns True.
    - `unwrap()`: Raises a `ValueError`.
    - `map()`: Returns itself, no transformation.
    """

    def is_some(self) -> bool:
        """
        Checks if the value is present.
        """
        return False

    def is_none(self) -> bool:
        """
        Checks if the value is absent.
        """
        return True

    def unwrap(self) -> None:
        """
        Raises an error indicating that a `None` value cannot be unwrapped.
        """
        raise ValueError("Cannot unwrap a None value")

    def map(self, fn: Callable[[T], R]) -> "NoneType":
        """
        Returns itself since there is no value to transform.
        """
        return self

    def __repr__(self) -> str:
        return "None"

    def __eq__(self, other) -> bool:
        return isinstance(other, NoneType)

    def __str__(self) -> str:
        return "None"

    def __int__(self) -> int:
        raise TypeError("Cannot convert None to int")

    def __float__(self) -> float:
        raise TypeError("Cannot convert None to float")

    def __bool__(self) -> bool:
        return False
