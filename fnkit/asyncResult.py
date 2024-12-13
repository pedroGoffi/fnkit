from typing import Generic, TypeVar, Callable, Awaitable

T = TypeVar('T')
R = TypeVar('R')
E = TypeVar('E')

class AsyncResult(Generic[T, E]):
    """
    `AsyncResult` Class in Python
    
    Handles results of asynchronous computations.
    
    Attributes:
        computation: The original async computation, if any.
        value: The result of the asynchronous computation, if any.
        error: The error that occurred during the computation, if any.
    
    Methods:
        await: Awaits the computation.
        map: Maps a function over the successful result.
        map_err: Maps an error to another type.
        or_else: Executes a fallback computation if any computation fails.
        unwrap: Retrieves the value or raises an exception.
        expect: Retrieves the value, raising an exception if an error occurs.
        map_async: Maps an asynchronous function over the successful result.
    """

    def __init__(self, computation: Awaitable[T], error: E = None):
        self.computation = computation
        self.value = None
        self.error = error

    async def Await(self) -> T:
        """
        Awaits the computation.
        
        Returns:
            The result of the computation.
        
        Raises:
            Exception: If an error occurred during the computation.
        """
        try:
        
            self.value = await self.computation()
            return self.value
        except Exception as e:
            self.error = e
            raise

    def map(self, func: Callable[[T], R]) -> 'AsyncResult[R, E]':
        """
        Maps a function over the successful result.
        
        Args:
            func: A function to apply to the successful result.
        
        Returns:
            A new `AsyncResult` with the mapped value if successful, or an error if failed.
        """
        if self.error:
            return AsyncResult(computation=lambda: self.error)  # Directly return error
        try:
            return AsyncResult(computation=lambda: func(self.value), error=None)
        except Exception as e:
            return AsyncResult(computation=lambda: e, error=None)

    def map_err(self, func: Callable[[E], R]) -> 'AsyncResult[T, R]':
        """
        Maps an error to another type.
        
        Args:
            func: A function to apply to the error.
        
        Returns:
            A new `AsyncResult` with the mapped error.
        """
        if self.error:
            return AsyncResult(computation=lambda: func(self.error), error=None)
        return self

    def or_else(self, fn: Callable[[], 'AsyncResult[R, E]']) -> 'AsyncResult[R, E]':
        """
        Executes a fallback computation if any computation fails.
        
        Args:
            fn: A fallback function that returns a new `AsyncResult`.
        
        Returns:
            The current result if successful; otherwise, the result of the fallback computation.
        """
        if self.error:
            return fn()
        return self

    def unwrap(self) -> T:
        """
        Retrieves the value if successful; raises an exception if not.
        
        Raises:
            ValueError: If an error occurred during the computation.
        
        Returns:
            The successful value.
        """
        if self.error:
            raise ValueError("Computation failed with error: " + str(self.error))
        return self.value

    def expect(self, msg: str) -> T:
        """
        Retrieves the value, raising an exception with a message if an error occurs.
        
        Args:
            msg: The message for the exception.
        
        Raises:
            ValueError: If an error occurred during the computation.
        
        Returns:
            The successful value.
        """
        if self.error:
            raise ValueError(msg + " | Error: " + str(self.error))
        return self.value

    async def map_async(self, func: Callable[[T], Awaitable[R]]) -> 'AsyncResult[R, E]':
        """
        Maps an asynchronous function over the successful result.
        
        Args:
            func: An asynchronous function to apply to the successful result.
        
        Returns:
            A new `AsyncResult` with the mapped value if successful, or an error if failed.
        """
        
        if self.error:
            return AsyncResult(computation=lambda: self.error)  # Directly return error
        try:
            
            new_value = await func(self.value)
            print(new_value.computation())
            return AsyncResult(computation=lambda: new_value, error=None)
        except Exception as e:
            return AsyncResult(computation=lambda: e, error=None)
