from typing     import TypeVar, Union, Callable
from .option    import Option
from .noneType  import NoneType

T = TypeVar('T')
R = TypeVar('R')

class Some(Option[T]):
    """
    Represents the presence of a value.
    
    Inherits from `Option` and adds specific methods for interacting with a present value.
    
    Methods:
    - Inherits all methods from `Option`.
    - `unwrap()`: Returns the value.
    - `map()`: Applies a function to the value and returns a new `Some`.
    """

    def __init__(self, value: T):
        super().__init__(value)

    def unwrap(self) -> T:
        """
        Retrieves the value.
        """
        return self._value

    def map(self, fn: Callable[[T], R]) -> "Some[R]":
        """
        Applies a function to the value and returns a new `Some`.
        """
        return Some(fn(self._value))

    def __repr__(self) -> str:
        return f"Some({self._value!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Some):
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

def option(value: T) -> Union[Some[T], NoneType]:
    """
    Creates a `Some` instance if value is not `None`; otherwise, returns `NONE`.
    """
    return Some(value) if value is not None else NoneType()
