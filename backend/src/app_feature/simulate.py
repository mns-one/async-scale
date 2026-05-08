import asyncio
from .ws_manager import hub
from . import controller

async def start_sim(size: int):
    for i in range(size):
        msg = f"Message -> {i}"
        await hub.broadcast(msg)      
        await asyncio.sleep(3)

    controller.IS_STARTED = False    