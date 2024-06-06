# asyncr

![PyPI](https://img.shields.io/pypi/v/asyncr?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/asyncr)

`asyncr` is a Python library for helping you handle those pesky async functions with ease! With `asyncr` you can easily
run your async functions in a synchronous way or run your synchronous functions in an async way.

> [!IMPORTANT]
> This library simply runs the functions is the event loop without changing the function code or optimizing it.
> If your code is not async safe, it may not work as expected.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install asyncr.

```bash
pip install asyncr
```

## Usage

```python
from asyncio import get_event_loop

from asyncr import as_sync, as_async


# Create a new async function and wrap it with as_sync, now it will be a sync function.
@as_sync
async def async_function():
    return "Hello, Sync World!"


print(async_function())


# Create a new sync function and wrap it with as_async, now it will be an async function.
@as_async
def sync_function():
    return "Hello, Async World!"


print(get_event_loop().run_until_complete(sync_function()))
```

You can also pass a the loop for running the functions as the parameter for the decorator. If no loop is provided, the
default loop will be used.

```python
from asyncio import get_event_loop, new_event_loop

from asyncr import as_sync, as_async


# Create a new async function and wrap it with as_sync, now it will be a sync function.
@as_sync(new_event_loop())
async def async_function():
    return "Hello, Sync World!"

print(async_function())
```

## Contributing

Please open an issue first to discuss what you would like to change.
I welcome any and all criticism, feedback, and suggestions even if I may not agree.
