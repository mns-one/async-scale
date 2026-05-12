import asyncio

from ..app_feature.model import SimPayload
from .errors import graceful_shutdown
from .seed_data import data_inflow
from .scaler import process_data
from .state import State
from .db_utils import clear_jobs

  
async def start_sim(sim_data: SimPayload):
    clear_jobs()    # clear jobs table before starting

    State.stop_sim = False
    State.is_started = True
    State.queued = 0
    State.in_process = 0
    State.workers_alive = 0
    State.stop_tokens = 0
    State.jobs_done = 0

    State.inflow_size = sim_data.size
    State.inflow_interval = sim_data.interval
    State.target = sim_data.target
    State.data_flow = True

    inflow_task = asyncio.create_task(data_inflow(), name="data_inflow")
    scaler_task = asyncio.create_task(process_data(), name="process_data")
    tasks = [inflow_task, scaler_task]

    try:
        await asyncio.gather(*tasks)  # raise error if any task fails

    except Exception as e:
        await graceful_shutdown(tasks, e)
        raise

    finally:
        State.is_started = False
