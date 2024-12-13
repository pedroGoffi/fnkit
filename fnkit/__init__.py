import asyncio
from typing             import Callable, List, Union, Awaitable, TypeVar
from .chainedResult     import ChainedResult
from .multiiErrorResult import MultiErrorResult
from .asyncResult       import AsyncResult
T = TypeVar('T')
E = TypeVar('E')
R = TypeVar('R')

# Assuming ChainedResult, MultiErrorResult, and AsyncResult are defined as provided in previous responses

def chain(result: Union[T, E], func: Callable[[T], 'ChainedResult[R, E]']) -> Union['ChainedResult[R, E]', 'ChainedResult[R, E]']:
    """
    Chains another computation function if the current value is successful.

    :param result: Current value, which can be of type `T` or `E`.
    :param func: Function to chain if the current value is successful.
    :return: New result of type `ChainedResult[R, E]`.
    """
    if isinstance(result, E):
        return ChainedResult(result)
    return func(result)

def map_value(result: Union[T, E], func: Callable[[T], R]) -> Union['ChainedResult[R, E]', 'ChainedResult[R, E]']:
    """
    Maps a function over a successful result.

    :param result: Current value, which can be of type `T` or `E`.
    :param func: Function to apply to the successful value.
    :return: New result of type `ChainedResult[R, E]`.
    """
    if isinstance(result, T):
        return ChainedResult(func(result))
    return ChainedResult(result)

def map_error(result: Union[T, E], func: Callable[[E], R]) -> Union['MultiErrorResult[R, E]', 'MultiErrorResult[T, E]']:
    """
    Maps an error to another type.

    :param result: Current value, which can be of type `T` or `E`.
    :param func: Function to apply to the error.
    :return: New result of type `MultiErrorResult[R, E]`.
    """
    if isinstance(result, E):
        return MultiErrorResult(func(result))
    return MultiErrorResult(result)

def or_else(result: Union[T, E], fn: Callable[[], 'ChainedResult[R, E]']) -> Union['ChainedResult[R, E]', 'ChainedResult[R, E]']:
    """
    Executes a fallback computation if an error occurs.

    :param result: Current value, which can be of type `T` or `E`.
    :param fn: Fallback function to execute if an error occurs.
    :return: New result of type `ChainedResult[R, E]`.
    """
    if isinstance(result, E):
        return fn()
    return ChainedResult(result)

def add_error(result: Union[T, List[E]], error: E) -> 'MultiErrorResult[T, E]':
    """
    Adds an error to the result.

    :param result: Current value, which can be of type `T` or `List[E]`.
    :param error: Error to add.
    :return: New result of type `MultiErrorResult[T, E]`.
    """
    if isinstance(result, list):
        result.append(error)
        return MultiErrorResult(result)
    return MultiErrorResult([error])

def add_error_to_async(result: Union[Awaitable[T], E], error: E) -> 'AsyncResult[T, E]':
    """
    Adds an error to an asynchronous result.

    :param result: Current value, which can be an `Awaitable` or `E`.
    :param error: Error to add.
    :return: New result of type `AsyncResult[T, E]`.
    """
    if isinstance(result, E):
        return AsyncResult(result, error)
    return AsyncResult(result, None)

def or_else_async(result: Union[Awaitable[T], E], fn: Callable[[], 'AsyncResult[R, E]']) -> 'AsyncResult[R, E]':
    """
    Executes a fallback computation if an error occurs in an asynchronous result.

    :param result: Current value, which can be an `Awaitable` or `E`.
    :param fn: Fallback function to execute if an error occurs.
    :return: New result of type `AsyncResult[R, E]`.
    """
    if isinstance(result, E):
        return fn()
    return AsyncResult(result)

def map_async(result: Union[Awaitable[T], E], func: Callable[[T], R]) -> 'AsyncResult[R, E]':
    """
    Maps a function over an asynchronous result.

    :param result: Current value, which can be an `Awaitable` or `E`.
    :param func: Function to apply to the asynchronous value.
    :return: New result of type `AsyncResult[R, E]`.
    """
    async def new_value() -> R:
        return func(await result)
    return AsyncResult(new_value(), result.error)

def map_error_async(result: Union[Awaitable[T], E], func: Callable[[E], R]) -> 'AsyncResult[T, R]':
    """
    Maps an error in an asynchronous result.

    :param result: Current value, which can be an `Awaitable` or `E`.
    :param func: Function to apply to the error.
    :return: New result of type `AsyncResult[T, R]`.
    """
    if result.error is not None:
        return AsyncResult(result.value, func(result.error))
    return result

def from_result(result: Union[T, E]) -> 'ChainedResult[T, E]':
    """
    Converts a raw value or error to a chained result.

    :param result: The raw value or error.
    :return: `ChainedResult` wrapping the given value or error.
    """
    if isinstance(result, E):
        return ChainedResult(result)
    return ChainedResult(result)

def from_error(result: Union[T, E]) -> 'MultiErrorResult[T, E]':
    """
    Converts a raw value or error to a multi-error result.

    :param result: The raw value or error.
    :return: `MultiErrorResult` wrapping the given error or value.
    """
    if isinstance(result, E):
        return MultiErrorResult([result])
    return MultiErrorResult([result])

def from_async(result: Awaitable[T]) -> 'AsyncResult[T, E]':
    """
    Converts an asynchronous result to an `AsyncResult`.

    :param result: The asynchronous result.
    :return: `AsyncResult` wrapping the asynchronous value.
    """
    async def async_result() -> T:
        return await result
    return AsyncResult(async_result())

def from_async_error(result: Awaitable[E]) -> 'AsyncResult[T, E]':
    """
    Converts an asynchronous result to an `AsyncResult` with error.

    :param result: The asynchronous result.
    :return: `AsyncResult` wrapping the asynchronous error.
    """
    async def async_result() -> E:
        return await result
    return AsyncResult(None, async_result())

def to_result(result: Union[T, E]) -> Union['ChainedResult[T, E]', 'MultiErrorResult[T, E]']:
    """
    Converts a value to a `ChainedResult` or `MultiErrorResult`.

    :param result: The value to convert.
    :return: `ChainedResult` if the value is `T`, `MultiErrorResult` if the value is `E`.
    """
    if isinstance(result, E):
        return MultiErrorResult(result)
    return ChainedResult(result)

def to_async(result: Union[T, E]) -> Union['AsyncResult[T, E]', 'AsyncResult[T, E]']:
    """
    Converts a value to an `AsyncResult`.

    :param result: The value to convert.
    :return: `AsyncResult` wrapping the asynchronous value or error.
    """
    if isinstance(result, E):
        return AsyncResult(None, result)
    return AsyncResult(result)

def to_async_result(result: Union[T, E]) -> 'AsyncResult[T, E]':
    """
    Converts a value to an `AsyncResult`.

    :param result: The value to convert.
    :return: `AsyncResult` wrapping the asynchronous value or error.
    """
    if isinstance(result, E):
        return AsyncResult(None, result)
    return AsyncResult(result)

def merge(results: List[Union[T, E]]) -> 'MultiErrorResult[T, E]':
    """
    Merges a list of values or errors into a multi-error result.

    :param results: A list of values or errors.
    :return: `MultiErrorResult` wrapping the list of values or errors.
    """
    errors = [result for result in results if isinstance(result, E)]
    return MultiErrorResult(errors)

def flatten(results: List['ChainedResult[T, E]']) -> 'MultiErrorResult[T, E]':
    """
    Flattens a list of chained results into a multi-error result.

    :param results: A list of chained results.
    :return: `MultiErrorResult` containing all the errors from the chained results.
    """
    errors = [result for result in results if isinstance(result, MultiErrorResult)]
    return MultiErrorResult(errors)

def combine(results: List['ChainedResult[T, E]']) -> 'MultiErrorResult[T, E]':
    """
    Combines a list of chained results into a single result.

    :param results: A list of chained results.
    :return: `MultiErrorResult` containing all the values from the chained results.
    """
    values = [result for result in results if isinstance(result, ChainedResult)]
    return MultiErrorResult(values)

def parallel(results: List[Awaitable[T]]) -> 'AsyncResult[List[T], E]':
    """
    Executes a list of asynchronous computations in parallel.

    :param results: A list of asynchronous computations.
    :return: `AsyncResult` containing a list of results or errors.
    """
    async def gather() -> List[T]:
        return await asyncio.gather(*results)
    return AsyncResult(gather())

def race(results: List[Awaitable[T]]) -> 'AsyncResult[T, E]':
    """
    Races a list of asynchronous computations and returns the first result.

    :param results: A list of asynchronous computations.
    :return: `AsyncResult` containing the first result or error.
    """
    async def race_result() -> T:
        done, pending = await asyncio.wait(results, return_when=asyncio.FIRST_COMPLETED)
        if done:
            return done.pop().result()
        raise Exception("No result from race")
    return AsyncResult(race_result())

def handle_error(result: Union[T, E], handler: Callable[[E], R]) -> Union[T, R]:
    """
    Handles an error by applying a handler function.

    :param result: Current value, which can be `T` or `E`.
    :param handler: Function to apply to the error.
    :return: Transformed value of type `R` if an error, else `T`.
    """
    if isinstance(result, E):
        return handler(result)
    return result

def handle_async_error(result: Awaitable[T], handler: Callable[[E], R]) -> 'AsyncResult[T, R]':
    """
    Handles an asynchronous error by applying a handler function.

    :param result: Asynchronous result.
    :param handler: Function to apply to the error.
    :return: `AsyncResult` containing transformed error or value.
    """
    async def handle() -> T:
        try:
            return await result
        except E as e:
            return handler(e)
    return AsyncResult(handle())

def sequence(results: List[Awaitable[T]]) -> 'AsyncResult[List[T], E]':
    """
    Executes a sequence of asynchronous computations.

    :param results: A list of asynchronous computations.
    :return: `AsyncResult` containing a list of values or errors.
    """
    async def sequence_result() -> List[T]:
        return [await r for r in results]
    return AsyncResult(sequence_result())

def reduce(results: List[T], func: Callable[[T, T], T]) -> T:
    """
    Reduces a list of values using a binary function.

    :param results: A list of values.
    :param func: A binary function.
    :return: The reduced result.
    """
    return func(results[0], results[1]) if len(results) > 1 else results[0]

def reduce_error(results: List[E], func: Callable[[E, E], E]) -> E:
    """
    Reduces a list of errors using a binary function.

    :param results: A list of errors.
    :param func: A binary function.
    :return: The reduced error.
    """
    return func(results[0], results[1]) if len(results) > 1 else results[0]

def filter_results(results: List[Union[T, E]], predicate: Callable[[T], bool]) -> List[T]:
    """
    Filters a list of values based on a predicate.

    :param results: A list of values or errors.
    :param predicate: A predicate function.
    :return: A list of filtered values.
    """
    return [result for result in results if isinstance(result, T) and predicate(result)]

def filter_errors(results: List[Union[T, E]], predicate: Callable[[E], bool]) -> List[E]:
    """
    Filters a list of errors based on a predicate.

    :param results: A list of values or errors.
    :param predicate: A predicate function.
    :return: A list of filtered errors.
    """
    return [result for result in results if isinstance(result, E) and predicate(result)]

def merge_async(results: List[Awaitable[T]]) -> 'AsyncResult[List[T], E]':
    """
    Merges a list of asynchronous computations into a multi-error result.

    :param results: A list of asynchronous computations.
    :return: `AsyncResult` containing a list of results or errors.
    """
    async def merge_result() -> List[T]:
        return await asyncio.gather(*results)
    return AsyncResult(merge_result())

def reduce_async(results: List[Awaitable[T]], func: Callable[[T, T], T]) -> 'AsyncResult[T, E]':
    """
    Reduces a list of asynchronous computations using a binary function.

    :param results: A list of asynchronous computations.
    :param func: A binary function.
    :return: `AsyncResult` containing the reduced result.
    """
    async def reduce_result() -> T:
        reduced = await results[0]
        for result in results[1:]:
            reduced = func(reduced, await result)
        return reduced
    return AsyncResult(reduce_result())

def filter_async(results: List[Awaitable[T]], predicate: Callable[[T], bool]) -> 'AsyncResult[List[T], E]':
    """
    Filters a list of asynchronous computations based on a predicate.

    :param results: A list of asynchronous computations.
    :param predicate: A predicate function.
    :return: `AsyncResult` containing filtered values or errors.
    """
    async def filter_result() -> List[T]:
        return [await r for r in results if predicate(await r)]
    return AsyncResult(filter_result())

def sequence_async(results: List[Awaitable[Union[T, E]]]) -> 'AsyncResult[List[Union[T, E]], E]':
    """
    Executes a sequence of asynchronous computations.

    :param results: A list of asynchronous computations.
    :return: `AsyncResult` containing a list of values or errors.
    """
    async def sequence_result() -> List[Union[T, E]]:
        return [await r for r in results]
    return AsyncResult(sequence_result())
