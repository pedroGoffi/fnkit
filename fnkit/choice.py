from typing     import TypeVar, Union, Callable, Generic
from .option    import Option
from .noneType  import NoneType

T = TypeVar('T')
E = TypeVar('E')
R = TypeVar('R')

class Choice(Generic[T, E]):
    """
    Represents a choice that can either hold a value (`Some(T)`), an error (`Err(E)`), or be absent (`None`).
    
    Methods:
    - `is_some()`: Returns True if the value is present.
    - `is_err()`: Returns True if an error is present.
    - `is_none()`: Returns True if absent.
    - `unwrap()`: Retrieves the value if present; raises an error if absent.
    - `map()`: Applies a function to the value if present.
    - `map_err()`: Applies a function to the error if present.
    - `or_else()`: Returns the current value if present; executes a fallback if absent or an error.
    - `and_then()`: Chains another computation if the value is present.
    - `expect()`: Retrieves the value, raising an error if it's absent or an error.
    - `get()`: Retrieves the value or a default if absent or an error.
    """

    def __init__(self, value: Union[T, E, NoneType]):        
        self._value: Union[T, E, NoneType] = value
        

    def is_some(self) -> bool:
        """
        Checks if the value is present.
        """
        return isinstance(self._value, T)

    def is_err(self) -> bool:
        """
        Checks if the result is an error.
        """
        return isinstance(self._value, E)

    def is_none(self) -> bool:
        """
        Checks if the value is absent.
        """
        return self._value is None

    def unwrap(self) -> Union[T, E]:
        """
        Retrieves the value if present; raises an error if absent or an error.
        """
        if self.is_err():
            raise ValueError("Cannot unwrap an error value.")
        if self.is_none():
            raise ValueError("Cannot unwrap a None value")
        return self._value

    def map(self, fn: Callable[[T], R]) -> "Choice[R, E]":
        """
        Applies a function to the value if present.
        """
        if self.is_some():
            return Choice(fn(self._value))
        return self

    def map_err(self, fn: Callable[[E], R]) -> "Choice[T, R]":
        """
        Applies a function to the error if present.
        """
        if self.is_err():
            return Choice(fn(self._value))
        return self

    def or_else(self, fn: Callable[[], Union[T, E]]) -> Union[T, E]:
        """
        Returns the current value if present; executes a fallback if absent or an error.
        """
        if self.is_some():
            return self._value
        return fn()

    def and_then(self, fn: Callable[[T], "Choice[R, E]"]) -> "Choice[R, E]":
        """
        Chains another computation if the value is present.
        """
        if self.is_some():
            return fn(self._value)
        return Choice(None)

    def expect(self, msg: str) -> Union[T, E]:
        """
        Retrieves the value, raising an error if it's absent or an error.
        """
        if self.is_none():
            raise ValueError(msg)
        if self.is_err():
            raise ValueError(msg)
        return self._value

    def get(self, default: Union[T, E]) -> Union[T, E]:
        """
        Retrieves the value or a default if absent or an error.
        """
        if self.is_some():
            return self._value
        return default

    def __repr__(self) -> str:
        return f"Choice({self._value!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Choice):
            return self._value == other._value
        return False

    def __str__(self) -> str:
        return str(self._value)

    def __int__(self) -> int:
        if self.is_some():
            return int(self._value)
        raise TypeError("Cannot convert None or error to int")

    def __float__(self) -> float:
        if self.is_some():
            return float(self._value)
        raise TypeError("Cannot convert None or error to float")

    def __bool__(self) -> bool:
        return self.is_some()
