from .state import State

async def stop_sim_task():
    async with State.lock:
        State.stop_sim = True
        State.data_flow = False
        State.stop_tokens = max(State.stop_tokens, State.workers_alive)
        
