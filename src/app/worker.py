import asyncio
import uvloop
from arq.connections import RedisSettings
from arq.worker import Worker
from typing import Any

from .core.config import settings

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

REDIS_QUEUE_HOST = settings.REDIS_QUEUE_HOST
REDIS_QUEUE_PORT = settings.REDIS_QUEUE_PORT


# -------- background tasks --------
async def sample_background_task(ctx: Worker, name: str) -> str:
    await asyncio.sleep(5)
    return f"Task {name} is complete!"


# -------- base functions --------
async def startup(ctx: Worker) -> None:
    print("worker start")


async def shutdown(ctx: Worker) -> None:
    print("worker end")


# -------- class --------
class WorkerSettings:
    functions = [sample_background_task]
    redis_settings = RedisSettings(
        host=REDIS_QUEUE_HOST, 
        port=REDIS_QUEUE_PORT
    )
    on_startup = startup
    on_shutdown = shutdown
    handle_signals = False
