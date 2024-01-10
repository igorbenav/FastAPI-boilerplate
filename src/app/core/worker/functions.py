import asyncio
import logging
import uvloop
from arq.worker import Worker

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


# -------- background tasks --------
async def sample_background_task(ctx: Worker, name: str) -> str:
    await asyncio.sleep(5)
    return f"Task {name} is complete!"


# -------- base functions --------
async def startup(ctx: Worker) -> None:
    logging.info('Worker Started')


async def shutdown(ctx: Worker) -> None:
    logging.info("Worker end")
