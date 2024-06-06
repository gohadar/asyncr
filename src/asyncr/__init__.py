import asyncio
from asyncio import AbstractEventLoop
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


def as_sync(loop: AbstractEventLoop = __get_event_loop()):
    """
    Runs an async function from a synchronous context.

    Args:
        loop: The loop to run the function in.

    Returns:
        A synchronous function that will run the base `func` asynchronously.
    """
    nest_asyncio.apply()

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            async def wrapper():
                return await func(*args, **kwargs)

            return loop.run_until_complete(wrapper())

        return inner

    # We want to also support the decorator being called without the parentheses and in this case the loop will be the
    # function to be decorated. In this case we want to use the default loop.
    if callable(loop):
        actual_function = loop
        loop = __get_event_loop()

        return decorator(actual_function)

    return decorator


def as_async(loop: AbstractEventLoop = __get_event_loop()):
    """
    Runs a synchronous function from an asynchronous context.

    Args:
        loop: The loop to run the function in.

    Returns:
        An asynchronous function that will run the base `func` synchronously.
    """
    nest_asyncio.apply()

    def decorator(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            async def wrapper():
                return func(*args, **kwargs)

            return loop.run_until_complete(wrapper())

        return inner

    # We want to also support the decorator being called without the parentheses and in this case the loop will be the
    # function to be decorated. In this case we want to use the default loop.
    if callable(loop):
        actual_function = loop
        loop = __get_event_loop()

        return decorator(actual_function)

    return decorator
