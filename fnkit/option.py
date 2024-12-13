from typing import Generic, TypeVar, Union, Callable

T = TypeVar('T')
R = TypeVar('R')

class Option(Generic[T]):
    """
    Represents an optional value that can either be present (`Some`) or absent (`None`).
    
    Methods:
    - `is_some()`: Returns True if the value is present.
    - `is_none()`: Returns True if the value is absent.
    - `unwrap()`: Retrieves the value if present; raises an error if absent.
    - `map()`: Applies a function to the value if present.
    - `filter()`: Filters the value using a predicate function.
    - `flat_map()`: Applies a function that returns another `Option` to the value if present.
    - `or_else()`: Returns the current value if present; otherwise, returns a fallback value.
    - `and_then()`: Chains another `Option` computation if the value is present.
    - `contains()`: Checks if the current `Option` contains a specific value.
    - `get()`: Retrieves the value or a default if absent.
    """
    _value: Union[T, None]
    def __init__(self, value: Union[T, None]):        
        self._value = value

    def is_some(self) -> bool:
        """
        Checks if the value is present.
        """
        return self._value is not None

    def is_none(self) -> bool:
        """
        Checks if the value is absent.
        """
        return self._value is None

    def unwrap(self) -> T:
        """
        Retrieves the value if present; raises a `ValueError` if absent.
        """
        if self.is_none():
            raise ValueError("Cannot unwrap a None value")
        return self._value

    def map(self, fn: Callable[[T], R]) -> "Option[R]":
        """
        Applies a function to the value if present and returns a new `Option` with the result.
        """
        if self.is_some():
            return Option(fn(self._value))
        return Option(None)

    def filter(self, predicate: Callable[[T], bool]) -> "Option[T]":
        """
        Filters the value using a predicate function; returns `None` if the predicate fails.
        """
        if self.is_some() and predicate(self._value):
            return self
        return Option(None)

    def flat_map(self, fn: Callable[[T], "Option[R]"]) -> "Option[R]":
        """
        Applies a function that returns another `Option` to the value if present.
        """
        if self.is_some():
            return fn(self._value)
        return Option(None)

    def or_else(self, fn: Callable[[], T]) -> T:
        """
        Returns the current value if present; otherwise, executes a fallback function and returns its result.
        """
        return self._value if self.is_some() else fn()

    def and_then(self, fn: Callable[[T], "Option[R]"]) -> "Option[R]":
        """
        Chains another `Option` computation if the value is present.
        """
        if self.is_some():
            return fn(self._value)
        return Option(None)

    def contains(self, value: T) -> bool:
        """
        Checks if the current `Option` contains a specific value.
        """
        return self.is_some() and self._value == value

    def get(self, default: T) -> T:
        """
        Retrieves the value if present; otherwise, returns a default value.
        """
        return self._value if self.is_some() else default

    def __repr__(self) -> str:
        return f"Option({self._value!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Option):
            return self._value == other._value
        return False

    def __str__(self) -> str:
        return str(self._value)

    def __int__(self) -> int:
        if self.is_some():
            return int(self._value)
        raise TypeError("Cannot convert None to int")

    def __float__(self) -> float:
        if self.is_some():
            return float(self._value)
        raise TypeError("Cannot convert None to float")

    def __bool__(self) -> bool:
        return self.is_some()
