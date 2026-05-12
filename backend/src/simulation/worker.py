import asyncio
import random

from .errors import DatabaseError, WorkerError
from .state import State
from .db_utils import claim_pending_job, mark_job_completed, mark_dependent_jobs_failed


async def start_worker():
    # update flag on new worker
    async with State.lock:
        State.workers_alive += 1

    job_id = None    
    
    try:
        while True:
            # scale-down check between jobs
            async with State.lock:
                if State.stop_tokens > 0:   # check for scale down request
                    State.stop_tokens -= 1
                    break
                if State.queued <= 0:       # exit if empty queue and no incoming data
                    if not State.data_flow:   
                        break

            # claim job
            job_id = claim_pending_job()
            if job_id == -1:                  # sleep if no job available
                await asyncio.sleep(1)
                continue
            
            # update job state flags
            async with State.lock:
                State.queued -= 1
                State.in_process += 1

            # simulate job processing delay
            process_time = random.randint(1, 5)
            await asyncio.sleep(process_time)
            
            # decide job success failure using random and update status
            num = random.randint(1,100)
            if num%3 == 0:
                success = True
            else:
                success = False    

            failed_dependents = 0    
            if success:
                mark_job_completed(job_id, True)
            else:
                mark_job_completed(job_id, False)
                failed_dependents = mark_dependent_jobs_failed(job_id)    

            # update job state flags
            async with State.lock:
                State.in_process -= 1
                State.queued = max(0, State.queued - failed_dependents)
                if success:
                    State.jobs_done += 1

    except DatabaseError as e:
        if job_id is None:
            message = "Worker failed before acquiring job"
        else:
            message = f"Worker failed processing job {job_id}"

        raise WorkerError(
            message
        ) from e
                    
    finally:
        # update flag on exit
        async with State.lock:
            State.workers_alive -= 1
       
