import asyncio
from .seed_data import SeedData
from ..app_feature.scaler import Scaler
from .state import State
from .db_utils import clear_jobs

class JobSimulation:
    
    async def start_sim(size: int):
        State.queued = 0
        State.in_process = 0
        State.workers_alive = 0
        State.stop_tokens = 0
        State.jobs_done = 0

        State.inflow_size = size
        State.data_flow = True

        clear = clear_jobs()
        asyncio.create_task(SeedData.data_inflow())


         