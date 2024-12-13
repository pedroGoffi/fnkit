from fnkit import ChainedResult
from typing import Callable

def chain(result: ChainedResult, func: Callable[[ChainedResult], ChainedResult]) -> ChainedResult:
    """
    Chains another function to be applied if the result succeeds.
    """
    return func(result)

def map_value(result: ChainedResult, func: Callable) -> ChainedResult:
    """
    Applies a function to the value of the result if it exists.
    """
    if result.value is not None:
        return ChainedResult(value=func(result.value))
    return result

def or_else(result: ChainedResult, fallback: Callable[[ChainedResult], ChainedResult]) -> ChainedResult:
    """
    Returns a fallback result if the initial result fails.
    """
    if result.value is None and result.errors:
        return fallback(result)
    return result

def main():
    # Example of synchronous chaining
    result = ChainedResult(value=42)
    result = map_value(result, lambda x: x * 2)
    result = or_else(result, lambda r: ChainedResult(error="Fallback"))

    if result.errors:  # Use result.errors instead of result.error
        print(f"Error: {result.errors}")
    else:
        print(f"Success: {result.value}")

if __name__ == "__main__":
    main()
