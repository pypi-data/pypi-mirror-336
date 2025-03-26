import asyncio
import inspect
import logging
import time
from functools import wraps
from .exception import exception_to_dict
from .jsonable_encoder import jsonable_encoder


async def retry_async(func, *args, sleep_time=2, max_attempts=3, backoff=2, exceptions=(Exception,), **kwargs):
    """
    Retry an asynchronous function up to `max_attempts` times with exponential backoff.

    Parameters:
        func (callable): The async function to be executed.
        *args: Positional arguments for `func`.
        sleep_time (float): Initial delay (in seconds) before retrying.
        max_attempts (int): Maximum number of attempts.
        backoff (float): Factor by which the delay increases after each attempt.
        exceptions (tuple): A tuple of exception types to catch and retry.
        **kwargs: Keyword arguments for `func`.

    Returns:
        The return value of `func` if it succeeds.

    Raises:
        Exception: The last exception encountered after all attempts have failed.
    """
    delay = sleep_time
    for attempt in range(1, max_attempts + 1):
        try:
            return await func(*args, **kwargs)
        except exceptions as e:
            error_dict = exception_to_dict(e)
            error_dict['kwargs'] = jsonable_encoder(kwargs)
            error_dict['args'] = jsonable_encoder(args)
            if attempt == max_attempts:
                logging.error(
                    msg=f"We could not finish the current job in the function {func.__name__}.",
                    extra={
                        'details': dict(
                            controller=func.__name__,
                            subject=f'Error at {func.__name__}',
                            payload=error_dict,
                            footprint=True,
                        )
                    }
                )
                raise e
            else:
                logging.warning(
                    msg=f"An error happened while we retry to run {func.__name__} at the {attempt} attempt{'s' if attempt > 1 else ''}.",
                    extra={
                        'details': dict(
                            controller=func.__name__,
                            subject=f'Warning at retrying {func.__name__}',
                            payload=error_dict,
                            footprint=True,
                        )
                    }
                )
            await asyncio.sleep(delay)
            delay *= backoff


def retry(func, *args, sleep_time=2, max_attempts=3, backoff=2, exceptions=(Exception,), **kwargs):
    """
    Retry a function (synchronous or asynchronous) up to `max_attempts` times with exponential backoff.

    For asynchronous functions, this returns an awaitable that must be awaited.

    Parameters:
        func (callable): The function to be executed (sync or async).
        *args: Positional arguments for `func`.
        sleep_time (float): Initial delay (in seconds) before retrying.
        max_attempts (int): Maximum number of attempts.
        backoff (float): Factor by which the delay increases after each attempt.
        exceptions (tuple): A tuple of exception types to catch and retry.
        **kwargs: Keyword arguments for `func`.

    Returns:
        The return value of `func` if it succeeds. For async functions,
        this is an awaitable that yields the result.

    Raises:
        Exception: The last exception encountered after all attempts have failed.
    """
    if inspect.iscoroutinefunction(func):
        return retry_async(
            func,
            *args,
            sleep_time=sleep_time,
            max_attempts=max_attempts,
            backoff=backoff,
            exceptions=exceptions,
            **kwargs
        )

    delay = sleep_time
    for attempt in range(1, max_attempts + 1):
        try:
            return func(*args, **kwargs)
        except exceptions as e:
            error_dict = exception_to_dict(e)
            error_dict['kwargs'] = jsonable_encoder(kwargs)
            error_dict['args'] = jsonable_encoder(args)
            if attempt == max_attempts:
                logging.error(
                    msg=f"We could not finish the current job in the function {func.__name__}.",
                    extra={
                        'details': dict(
                            controller=func.__name__,
                            subject=f'Error at {func.__name__}',
                            payload=error_dict,
                            footprint=True,
                        )
                    }
                )
                raise e
            else:
                logging.warning(
                    msg=f"An error happened while we retry to run {func.__name__} at the {attempt} attempt{'s' if attempt > 1 else ''}.",
                    extra={
                        'details': dict(
                            controller=func.__name__,
                            subject=f'Warning at retrying {func.__name__}',
                            payload=error_dict,
                            footprint=True,
                        )
                    }
                )
            time.sleep(delay)
            delay *= backoff


def retry_wrapper(max_attempts=3, sleep_time=2, backoff=2, exceptions=(Exception,)):
    """
    A decorator that retries a function or method until it succeeds or a maximum number of attempts is reached.
    Supports both synchronous and asynchronous functions.

    Parameters:
        max_attempts (int): The maximum number of attempts. Default is 5.
        sleep_time (float): The initial delay between attempts in seconds. Default is 1.
        backoff (float): The multiplier applied to the delay after each attempt. Default is 1.
        exceptions (tuple): A tuple of exceptions to catch. Default is (Exception,).

    Returns:
        function: The wrapped function that will be retried on failure.
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await retry_async(
                func,
                *args,
                max_attempts=max_attempts,
                sleep_time=sleep_time,
                backoff=backoff,
                exceptions=exceptions,
                **kwargs
            )

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return retry(
                func,
                *args,
                max_attempts=max_attempts,
                sleep_time=sleep_time,
                backoff=backoff,
                exceptions=exceptions,
                **kwargs
            )

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
