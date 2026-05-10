import asyncio
import random

from .state import State
from .db_utils import create_random_jobs


async def data_inflow():
    # seed new data with intervals
    for _ in range(10):
        roll = random.randint(1, State.inflow_size)
        new_jobs = create_random_jobs(roll)
        async with State.lock:
            State.queued += new_jobs
            total_jobs = State.queued
        print(f"News jobs arrived -> {new_jobs}, Total jobs -> {total_jobs}")
        await asyncio.sleep(3)

    # flag to mark end of incoming data    
    State.data_flow = False
    
