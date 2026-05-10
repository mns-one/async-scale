import asyncio

class State:

    lock = asyncio.Lock()

    queued = 0                 # pending jobs
    in_process = 0             # currently processing
    workers_alive = 0          # running workers
    stop_tokens = 0            # worker scale-down requests
    jobs_done = 0

    target_pct = 30
    inflow_size = 0
    data_flow = False

