import asyncio
import functools
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


def as_sync(func):
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
        async def wrapper():
            return await func(*args, **kwargs)

        loop = __get_event_loop()
        return loop.run_until_complete(wrapper())

    return inner


def as_async(func):
    """
    Runs a synchronous function from an asynchronous context.

    Args:
        func: The function to run.

    Returns:
        An asynchronous function that will run the base `func` synchronously.
    """
    nest_asyncio.apply()

    @wraps(func)
    async def inner(*args, **kwargs):
        loop = __get_event_loop()
        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

    return inner
