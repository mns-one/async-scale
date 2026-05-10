import asyncio
from ..simulation.start import JobSimulation

async def process_data(size: int) -> None:
        asyncio.create_task(JobSimulation.start_sim(size))
