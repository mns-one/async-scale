import logging
import asyncio

from .state import State

logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    pass

class WorkerError(Exception):
    pass

async def graceful_shutdown(tasks: list[asyncio.Task], reason: Exception):
    logger.exception("Simulation shutdown triggered: %s", reason)

    # ask workers to stop between jobs
    async with State.lock:
        State.data_flow = False
        State.stop_tokens = max(State.stop_tokens, State.workers_alive)

    # cancel top-level tasks
    for t in tasks:
        if not t.done():
            t.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

