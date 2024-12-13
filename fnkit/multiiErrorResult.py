from typing import Generic, TypeVar, Callable, List, Union

T = TypeVar('T')
R = TypeVar('R')
E = TypeVar('E')

class MultiErrorResult(Generic[T, E]):
    """
    `MultiErrorResult` Class in Python
    
    Holds multiple errors if a computation fails, allowing users to inspect all the reasons for failure.
    
    Attributes:
        _value: The successful computation result, if any.
        _errors: A list of errors that occurred during the computation.
    
    Methods:
        add_error: Adds an error to the list.
        get_errors: Returns a list of all errors.
        is_multi_err: Checks if there are multiple errors.
        unwrap: Retrieves the value if successful or raises an exception.
        map: Maps a function over the successful result.
        map_err: Maps multiple errors to another type.
        or_else: Executes a fallback computation if any computation fails.
    """

    def __init__(self, value: Union[T, E, None], errors: List[E] = None):
        self._value = value
        self._errors = errors if errors is not None else []

    def add_error(self, error: E) -> None:
        """
        Adds an error to the list.
        
        Args:
            error: An error to add.
        """
        self._errors.append(error)

    def get_errors(self) -> List[E]:
        """
        Returns a list of all errors.
        
        Returns:
            A list of errors.
        """
        return self._errors

    def is_multi_err(self) -> bool:
        """
        Checks if there are multiple errors.
        
        Returns:
            True if there are multiple errors, False otherwise.
        """
        return len(self._errors) > 1

    def unwrap(self) -> T:
        """
        Retrieves the value if successful; raises an exception if not.
        
        Raises:
            ValueError: If there are errors in the result.
        
        Returns:
            The successful value.
        """
        if self._errors:
            raise ValueError("Result contains errors: " + str(self._errors))
        return self._value

    def map(self, func: Callable[[T], R]) -> 'MultiErrorResult[R, E]':
        """
        Maps a function over the successful result.
        
        Args:
            func: A function to apply to the successful result.
        
        Returns:
            A new `MultiErrorResult` with the mapped value if successful, or an error if failed.
        """
        if self._errors:
            return MultiErrorResult(self._errors, self._errors)
        try:
            return MultiErrorResult(func(self._value), [])
        except Exception as e:
            return MultiErrorResult([e] + self._errors, self._errors)

    def map_err(self, func: Callable[[List[E]], R]) -> 'MultiErrorResult[R, E]':
        """
        Maps multiple errors to another type.
        
        Args:
            func: A function to apply to the list of errors.
        
        Returns:
            A new `MultiErrorResult` with the mapped error.
        """
        if self._errors:
            return MultiErrorResult(func(self._errors), [])
        return self

    def or_else(self, fn: Callable[[], 'MultiErrorResult[R, E]']) -> 'MultiErrorResult[R, E]':
        """
        Executes a fallback computation if any computation fails.
        
        Args:
            fn: A fallback function that returns a new `MultiErrorResult`.
        
        Returns:
            The current result if successful; otherwise, the result of the fallback computation.
        """
        if self._errors:
            return fn()
        return self
