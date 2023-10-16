from typing import Callable
import functools

from fastapi import Request, Response
from fastapi.responses import JSONResponse
import redis.asyncio as redis
from redis.asyncio import Redis, ConnectionPool
from fastapi.responses import JSONResponse

pool: ConnectionPool | None = None
client: Redis | None = None

def cache(key_prefix: str, expiration: int = 3600) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def inner(request: Request, *args, **kwargs) -> Response:
            resource_id = args[0]  # Assuming the resource ID is the first argument
            cache_key = f"{key_prefix}:{resource_id}"
            
            if request.method == "GET":
                # Check if the data exists in the cache for GET requests
                cached_data = await client.get(cache_key)
                if cached_data:
                    # If data exists in the cache, return it
                    return JSONResponse(content=cached_data.decode(), status_code=200)
            
            # Call the original function for both all types of requests
            result = await func(request, *args, **kwargs)
            
            if request.method == "GET":
                # Store the result in the cache for GET requests with the specified expiration time
                await client.set(cache_key, result, expire=expiration)
            else:
                # Invalidate the cache for other types of requests
                await redis.delete(cache_key)
            
            return JSONResponse(content=result, status_code=200)
        
        return inner

    return wrapper
