# Redis Client Wrapper

This repository provides a Redis client wrapper for both synchronous and asynchronous interactions with Redis. It allows for easy configuration and connection management using a `RedisConfig` class.

## Features
- Support for both synchronous (`redis.Redis`) and asynchronous (`redis.asyncio.Redis`) clients.
- Configurable Redis connection settings.
- Secure connection handling with optional SSL (`rediss://` support).
- Context managers for clean resource management.

## Installation

```bash
pip install dtpyredis
```

## Usage

### Configuration
You can configure Redis settings using `RedisConfig`:

```python
from dtpyredis.config import RedisConfig
from dtpyredis.connection import RedisInstance

config = (
    RedisConfig()
    .set_redis_host("localhost")
    .set_redis_port(6379)
    .set_redis_db(0)
    .set_redis_password("your_password")
)
```

### Creating a Redis Client

#### Synchronous Client

```python
redis_instance = RedisInstance(config)

with redis_instance.get_redis() as client:
    client.set("foo", "bar")
    value = client.get("foo")
    print(value)  # Output: b'bar'
```

#### Asynchronous Client

```python
import asyncio

async def async_example():
    async with redis_instance.get_async_redis() as async_client:
        await async_client.set("foo", "bar")
        value = await async_client.get("foo")
        print(value)  # Output: b'bar'

asyncio.run(async_example())
```
