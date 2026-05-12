import asyncio

class State:

    lock = asyncio.Lock()
    
    stop_sim = False
    is_started = False         # simulation running status
    queued = 0                 # pending jobs
    in_process = 0             # currently processing
    workers_alive = 0          # running workers
    stop_tokens = 0            # worker scale-down requests
    jobs_done = 0              # successfully completed jobs
    data_flow = False          # flag to set if new jobs will arrive or not
    
    # user configurable
    target = 0                 # process x% of available jobs
    inflow_size = 0            # max size limit of each new batch of jobs
    inflow_interval = 0        # gap between each new job batch arrival

