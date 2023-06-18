import asyncio
from functools import wraps

import nest_asyncio


def __get_event_loop():
    """
    Gets an event loop.

    Returns:
        The current event loop or a new one if the is no running event loop.
    """
    try:
        return asyncio.get_event_loop()
    except RuntimeError as e:
        if 'There is no current event loop' in str(e):
            return asyncio.new_event_loop()

        raise


def run_async(func):
    """
    Runs an async function from a synchronous context.

    Args:
        func: The function to run.

    Returns:
        A synchronous function that will run the base `func` asynchronously.
    """
    nest_asyncio.apply()

    @wraps(func)
    def inner(*args, **kwargs):
        result = None

        async def wrapper():
            nonlocal result
            result = await func(*args, **kwargs)

        loop = __get_event_loop()
        loop.run_until_complete(wrapper())

        return result

    return inner
