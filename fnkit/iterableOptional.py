from typing     import TypeVar, Union, Callable, Generic, Iterator
from .noneType  import NoneType

T = TypeVar('T')
E = TypeVar('E')
R = TypeVar('R')

class IterableOptional(Generic[T]):
    """
    Represents an optional value with an iterable interface.
    
    Methods:
    - `is_some()`: Checks if the value is present.
    - `is_err()`: Checks if an error is present.
    - `is_none()`: Checks if the value is absent.
    - `unwrap()`: Retrieves the value.
    - `map()`: Applies a function to the value.
    - `map_err()`: Applies a function to the error.
    - `or_else()`: Returns a fallback value if absent or an error.
    - `expect()`: Retrieves the value, raising an error if absent or an error.
    - `get()`: Retrieves the value or a default.
    - `to_iter()`: Returns an iterator over the value.
    """

    def __init__(self, value: Union[T, E, NoneType]):
        if isinstance(value, (T, E, NoneType)):
            self._value: Union[T, E, NoneType] = value
        else:
            raise TypeError("Invalid type for IterableOptional, must be T, E, or NoneType.")

    def is_some(self) -> bool:
        """
        Checks if the value is present.
        """
        return isinstance(self._value, T)

    def is_err(self) -> bool:
        """
        Checks if an error is present.
        """
        return isinstance(self._value, E)

    def is_none(self) -> bool:
        """
        Checks if the value is absent.
        """
        return self._value is None

    def unwrap(self) -> Union[T, E]:
        """
        Retrieves the value.
        """
        if self.is_err():
            raise ValueError("Cannot unwrap an error value.")
        if self.is_none():
            raise ValueError("Cannot unwrap a None value")
        return self._value

    def map(self, fn: Callable[[T], R]) -> "IterableOptional[R]":
        """
        Applies a function to the value.
        """
        if self.is_some():
            return IterableOptional(fn(self._value))
        return self

    def map_err(self, fn: Callable[[E], R]) -> "IterableOptional[T]":
        """
        Applies a function to the error.
        """
        if self.is_err():
            return IterableOptional(fn(self._value))
        return self

    def or_else(self, fn: Callable[[], Union[T, E]]) -> Union[T, E]:
        """
        Returns the current value if present; executes a fallback if absent or an error.
        """
        if self.is_some():
            return self._value
        return fn()

    def expect(self, msg: str) -> Union[T, E]:
        """
        Retrieves the value, raising an error if absent or an error.
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

    def to_iter(self) -> Iterator[Union[T, E]]:
        """
        Returns an iterator over the value.
        """
        if self.is_some() or self.is_err():
            yield self._value

    def __repr__(self) -> str:
        return f"IterableOptional({self._value!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, IterableOptional):
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
