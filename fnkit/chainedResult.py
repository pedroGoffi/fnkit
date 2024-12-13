from typing import Generic, TypeVar, Callable, Union, List

T = TypeVar('T')
R = TypeVar('R')
E = TypeVar('E')

class ChainedResult(Generic[T, E]):
    """
    `ChainedResult` Class in Python
    
    Chains multiple computations and handles their results.
    
    Attributes:
        value: The successful computation result, if any.
        errors: A list of errors that occurred during any computation.
    
    Methods:
        chain: Chains another computation to the current result.
        map: Maps a function over the successful result.
        map_err: Maps an error to another type.
        unwrap: Retrieves the value if successful, raises an exception otherwise.
        or_else: Executes a fallback computation if any computation in the chain fails.
        expect: Retrieves the value, raises an exception with a message if an error occurs.
    """

    def __init__(self, value: Union[T, E, None], errors: List[E] = None):
        self.value = value
        self.errors = errors if errors is not None else []

    def chain(self, func: Callable[[T], 'ChainedResult[R, E]']) -> 'ChainedResult[R, E]':
        """
        Chains another computation to the current result.
        
        Args:
            func: A function that takes the current result value and returns a new `ChainedResult`.
        
        Returns:
            A new `ChainedResult` with the result of the chained computation.
        """
        if isinstance(self.value, Exception):
            return ChainedResult(self.value, self.errors)
        try:
            return func(self.value)
        except Exception as e:
            return ChainedResult(e, self.errors + [e])

    def map(self, func: Callable[[T], R]) -> 'ChainedResult[R, E]':
        """
        Maps a function over the successful result.
        
        Args:
            func: A function to apply to the successful result.
        
        Returns:
            A new `ChainedResult` with the mapped value if successful, or an error if failed.
        """
        if isinstance(self.value, Exception):
            return ChainedResult(self.value, self.errors)
        try:
            return ChainedResult(func(self.value), self.errors)
        except Exception as e:
            return ChainedResult(e, self.errors + [e])

    def map_err(self, func: Callable[[E], R]) -> 'ChainedResult[T, R]':
        """
        Maps an error to another type.
        
        Args:
            func: A function to apply to the errors.
        
        Returns:
            A new `ChainedResult` with the mapped error.
        """
        if isinstance(self.value, Exception):
            return ChainedResult(func(self.value), self.errors)
        return self

    def unwrap(self) -> T:
        """
        Retrieves the value if successful; raises an exception if not.
        
        Raises:
            ValueError: If there is an error in the result.
        
        Returns:
            The successful value.
        """
        if isinstance(self.value, Exception):
            raise ValueError("Result contains errors: " + str(self.errors))
        return self.value

    def or_else(self, fn: Callable[[], 'ChainedResult[R, E]']) -> 'ChainedResult[R, E]':
        """
        Executes a fallback computation if any computation in the chain fails.
        
        Args:
            fn: A fallback function that returns a new `ChainedResult`.
        
        Returns:
            The current result if successful; otherwise, the result of the fallback computation.
        """
        if isinstance(self.value, Exception):
            return fn()
        return self

    def expect(self, msg: str) -> T:
        """
        Retrieves the value, raising an exception with a message if an error occurs.
        
        Args:
            msg: The message for the exception.
        
        Raises:
            ValueError: If there is an error in the result.
        
        Returns:
            The successful value.
        """
        if isinstance(self.value, Exception):
            raise ValueError(msg + " | Errors: " + str(self.errors))
        return self.value
