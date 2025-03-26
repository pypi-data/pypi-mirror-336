import hashlib
import json
import logging
import zlib
from functools import wraps
from typing import Any
from dtpyutils.exception import exception_to_dict
from dtpyutils.jsonable_encoder import jsonable_encoder
from redis import Redis
from .connection import RedisInstance


def get_data_directly(
        func,
        *args,
        **kwargs
):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logging.error(
            msg='Error occurred while executing the function.',
            extra={
                'details': dict(
                    controller='caching.get_data_directly',
                    subject='Error on running a function',
                    payload=exception_to_dict(e),
                    footprint=True,
                )
            }
        )
        raise e


def cache_data(
        response: dict,
        cache_key: str,
        redis_instance: Redis,
        expire: int | None = None
):
    try:
        compressed_main_value = zlib.compress(json.dumps(jsonable_encoder(response)).encode('utf-8'))
        redis_instance.delete(cache_key)
        if expire:
            redis_instance.setex(name=cache_key, value=compressed_main_value, time=expire)
        else:
            redis_instance.set(name=cache_key, value=compressed_main_value)

    except Exception as exception:
        logging.error(
            msg='We faced an error while we want to cache data.',
            extra={
                'details': dict(
                    controller='caching.cache_data',
                    subject='Error on caching data',
                    payload={
                        'expire': expire,
                        'cache_key': cache_key,
                        'error': exception_to_dict(exception),
                    },
                    footprint=True,
                )
            }
        )

    return response


def cache_function(
    func: callable,
    redis: RedisInstance,
    namespace: str,
    expire: int | None = None,
    cache_only_for: list[dict[str, Any]] = None,
    skip_cache_keys: set[str] = None,
    *args,
    **kwargs,
):
    """
    Call a function with caching support. If a cached value exists in Redis, it is returned.
    Otherwise, the function is executed, its result is cached, and then returned.

    :param redis: An instance of redis class.
    :param skip_cache_keys: The keys that we should not involve them in caching:
    :param func: The function to be called.
    :param namespace: A string used as a namespace in the cache key.
    :param expire: Optional expiration time (in seconds) for the cache entry.
    :param cache_only_for: The situation that caching should be done.
    :param args: Positional arguments for `func`.
    :param kwargs: Keyword arguments for `func`.
    :return: The result of the function call, possibly validated via the response_model.
    """
    if skip_cache_keys is None:
        skip_cache_keys = set()

    if cache_only_for is not None:
        should_be_cached = False
        for cache_condition in cache_only_for:
            cache_col = cache_condition.get('kwarg')
            if cache_condition.get('operator') == 'in' and kwargs.get(cache_col) in cache_condition.get('value'):
                should_be_cached = True
                break

        if not should_be_cached:
            return get_data_directly(func=func, *args, **kwargs)

    # Extract a website value if provided and remove potential non-deterministic keys.
    kwargs_key = {k: v for k, v in kwargs.items() if k not in skip_cache_keys}

    # Build a deterministic cache key.
    cache_key = ""
    if namespace:
        cache_key += f"{namespace}:"
    if args:
        args_hash = hashlib.sha256(json.dumps(args, default=str).encode('utf-8')).hexdigest()
        cache_key += f"{args_hash}:"
    if kwargs_key:
        kwargs_hash = hashlib.sha256(json.dumps(kwargs_key, default=str).encode('utf-8')).hexdigest()
        cache_key += f"{kwargs_hash}:"
    cache_key = cache_key.rstrip(':')

    with redis.get_redis_client() as redis_instance:
        # Attempt to retrieve cached data.
        try:
            cache_compressed = redis_instance.get(cache_key)
        except Exception as exception:
            logging.error(
                msg='Error while trying to retrieve data from cache.',
                extra={
                    'details': dict(
                        controller='caching.cache_function',
                        subject='Error on get cached data',
                        payload={
                            'redis_key': cache_key,
                            'error': exception_to_dict(exception)
                        },
                        footprint=True,
                    )
                }
            )
            cache_compressed = None

        if cache_compressed is not None:
            try:
                response = json.loads(zlib.decompress(cache_compressed).decode('utf-8'))
                return response
            except Exception as exception:
                logging.error(
                    msg='Error during decompressing or loading cached data.',
                    extra={
                        'details': dict(
                            controller='caching.cache_function',
                            subject='Error on reading cache',
                            payload={
                                'redis_key': cache_key,
                                'error': exception_to_dict(exception)
                            },
                            footprint=True,
                        )
                    }
                )

        # If cache miss or error in retrieving cache, execute the function.
        result = get_data_directly(func=func, *args, **kwargs)

        # Cache the result.
        try:
            compressed_value = zlib.compress(json.dumps(jsonable_encoder(result)).encode('utf-8'))
            redis_instance.delete(cache_key)
            if expire:
                redis_instance.setex(name=cache_key, value=compressed_value, time=expire)
            else:
                redis_instance.set(name=cache_key, value=compressed_value)
        except Exception as exception:
            logging.error(
                msg='Error occurred while caching the result.',
                extra={
                    'details': dict(
                        controller='caching.cache_function',
                        subject='Error on reading cache',
                        payload={
                            'redis_key': cache_key,
                            'error': exception_to_dict(exception)
                        },
                        footprint=True,
                    )
                }
            )
        return result


def cache_wrapper(
    redis: RedisInstance,
    namespace: str,
    expire: int | None = None,
    cache_only_for: list[dict[str, Any]] = None,
    skip_cache_keys: set[str] = None,
):
    def decorator(func: callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cache_function(
                func=func,
                redis=redis,
                namespace=namespace,
                expire=expire,
                cache_only_for=cache_only_for,
                skip_cache_keys=skip_cache_keys,
                *args,
                **kwargs,
            )
        return wrapper

    return decorator
