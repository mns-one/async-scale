import asyncio
from src.simulation.start import start_sim

async def process_data(size: int) -> None:
        asyncio.create_task(start_sim(size))
