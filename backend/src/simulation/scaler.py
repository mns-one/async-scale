# scaler.py
import asyncio
import math
from .state import State
from .worker import start_worker
from ..app_feature.ws_manager import hub

POLL_SECONDS = 0.5  # interval for scaling process

async def process_data():
    try:
        # keep process alive until incoming data or jobs left
        while State.data_flow or State.queued > 0 or State.in_process > 0:
            
            # take snapshot of current flags
            async with State.lock:
                queued = State.queued
                in_process = State.in_process
                alive = State.workers_alive
                done = State.jobs_done

            total_jobs = queued + in_process

            # get diff between target throughput and current throughput
            desired = 0
            if total_jobs > 0:
                desired = math.ceil((State.target / 100.0) * total_jobs)
                desired = max(1, desired)  # keep at least 1 active when backlog exists

            diff = desired - alive
            print(f"diff= {diff}")

            # start more workers to meet target
            if diff > 0:
                spawn_n = diff
                print(f"Starting {spawn_n} workers")
                for _ in range(spawn_n):
                    asyncio.create_task(start_worker())

            # remove workers if above target
            elif diff < 0:
                down_n = abs(diff)
                print(f"Stopping {down_n} workers")
                async with State.lock:
                    State.stop_tokens += down_n   # set request flag for worker to read
            
            # print stats of current poll
            async with State.lock:
                ratio = 0.0 if total_jobs == 0 else (in_process / total_jobs) * 100.0

            print(
                f"Total_Jobs={total_jobs} InProcess={in_process} Desired={desired} "
                f"Workers={alive} Current Throughput={ratio:.2f}%  "
            )
            stats = {
                "jobs_to_process": total_jobs,
                "active_workers": alive,
                "jobs_done": done
            }
            await hub.broadcast(stats)

            await asyncio.sleep(POLL_SECONDS)
    finally:
        # mark end of simulation
        State.is_started = False

    




