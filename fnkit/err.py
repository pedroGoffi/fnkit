from typing     import TypeVar, Callable
from .result    import Result

T = TypeVar('T')
E = TypeVar('E')
R = TypeVar('R')


class Err(Result[T, E]):
    """
    Represents a failed computation with an error.
    
    Inherits from `Result` and adds specific methods for interacting with an error.
    
    Methods:
    - `unwrap()`: Raises an error as there is no value.
    - `map()`: Returns itself since there is no value to map.
    - `map_err()`: Applies a function to the error and returns a new `Err`.
    """

    def __init__(self, error: E):
        super().__init__(error)

    def unwrap(self) -> None:
        """
        Raises an error indicating that the computation failed.
        """
        raise ValueError("Cannot unwrap an error value.")

    def map(self, fn: Callable[[T], R]) -> "Err[E]":
        """
        Returns itself as there is no value to map.
        """
        return self

    def map_err(self, fn: Callable[[E], R]) -> "Err[R]":
        """
        Applies a function to the error and returns a new `Err`.
        """
        return Err(fn(self._value))

    def __repr__(self) -> str:
        return f"Err({self._value!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Err):
            return self._value == other._value
        return False

    def __str__(self) -> str:
        return str(self._value)

    def __int__(self) -> int:
        raise TypeError("Cannot convert error to int")

    def __float__(self) -> float:
        raise TypeError("Cannot convert error to float")

    def __bool__(self) -> bool:
        return False
