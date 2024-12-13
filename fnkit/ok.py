from typing     import TypeVar, Callable
from .result    import Result

T = TypeVar('T')
E = TypeVar('E')
R = TypeVar('R')

class Ok(Result[T, E]):
    """
    Represents a successful computation with a value.
    
    Inherits from `Result` and adds specific methods for interacting with a successful computation.
    
    Methods:
    - `unwrap()`: Returns the value.
    - `map()`: Applies a function to the value and returns a new `Ok`.
    - `map_err()`: Returns itself as there is no error to map.
    """

    def __init__(self, value: T):
        super().__init__(value)

    def unwrap(self) -> T:
        """
        Retrieves the value.
        """
        return self._value

    def map(self, fn: Callable[[T], R]) -> "Ok[R]":
        """
        Applies a function to the value and returns a new `Ok`.
        """
        return Ok(fn(self._value))

    def map_err(self, fn: Callable[[E], R]) -> "Ok[T]":
        """
        Returns itself as there is no error to map.
        """
        return self

    def __repr__(self) -> str:
        return f"Ok({self._value!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Ok):
            return self._value == other._value
        return False

    def __str__(self) -> str:
        return str(self._value)

    def __int__(self) -> int:
        return int(self._value)

    def __float__(self) -> float:
        return float(self._value)

    def __bool__(self) -> bool:
        return True
