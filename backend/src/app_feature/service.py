import asyncio
from src.simulation.start import start_sim
from .model import SimPayload

async def process_data(payload: SimPayload) -> None:
        asyncio.create_task(start_sim(payload))
