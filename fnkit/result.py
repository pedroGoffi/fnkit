from typing         import Generic, TypeVar, Union, Callable
from .noneType      import NoneType

T = TypeVar('T')
R = TypeVar('R')
E = TypeVar('E')

class Result(Generic[T, E]):
    """
    Represents a computation that could either succeed (`Ok(T)`) or fail (`Err(E)`).
    
    Methods:
    - `is_ok()`: Returns True if the result is successful.
    - `is_err()`: Returns True if the result is an error.
    - `unwrap()`: Retrieves the value if successful; raises an error if failed.
    - `map()`: Applies a function to the value if successful.
    - `map_err()`: Applies a function to the error if it exists.
    - `or_else()`: Returns the value if successful; otherwise, executes a fallback function.
    - `expect()`: Retrieves the value, raising an error if it’s not successful.
    - `get()`: Retrieves the value or a default if failed.
    """

    def __init__(self, value: Union[T, E, NoneType]):
        if isinstance(value, (T, E, NoneType)):
            self._value: Union[T, E, NoneType] = value
        else:
            raise TypeError("Invalid type for Result, must be T, E, or NoneType.")

    def is_ok(self) -> bool:
        """
        Checks if the result is successful.
        """
        return isinstance(self._value, T)

    def is_err(self) -> bool:
        """
        Checks if the result is an error.
        """
        return isinstance(self._value, E)

    def unwrap(self) -> T:
        """
        Retrieves the value if successful; raises an error if failed.
        """
        if self.is_err():
            raise ValueError("Cannot unwrap an error value.")
        return self._value

    def map(self, fn: Callable[[T], R]) -> "Result[R, E]":
        """
        Applies a function to the value if successful.
        """
        if self.is_ok():
            return Result(fn(self._value))
        return self

    def map_err(self, fn: Callable[[E], R]) -> "Result[T, R]":
        """
        Applies a function to the error if it exists.
        """
        if self.is_err():
            return Result(fn(self._value))
        return self

    def or_else(self, fn: Callable[[], T]) -> T:
        """
        Returns the value if successful; otherwise, executes a fallback function.
        """
        if self.is_ok():
            return self._value
        return fn()

    def expect(self, msg: str) -> T:
        """
        Retrieves the value, raising an error if it's not successful.
        """
        if self.is_err():
            raise ValueError(msg)
        return self._value

    def get(self, default: T) -> T:
        """
        Retrieves the value or a default if failed.
        """
        if self.is_ok():
            return self._value
        return default

    def __repr__(self) -> str:
        return f"Result({self._value!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Result):
            return self._value == other._value
        return False

    def __str__(self) -> str:
        return str(self._value)

    def __int__(self) -> int:
        if self.is_ok():
            return int(self._value)
        raise TypeError("Cannot convert error to int")

    def __float__(self) -> float:
        if self.is_ok():
            return float(self._value)
        raise TypeError("Cannot convert error to float")

    def __bool__(self) -> bool:
        return self.is_ok()
