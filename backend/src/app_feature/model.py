from pydantic import BaseModel, Field

class SimPayload(BaseModel):
    client_id: str
    size: int = Field(gt=49, le=300)
    interval: int = Field(gt=1, le=5)
    target: int = Field(gt=9, le=80)

class StatsPayload(BaseModel):
    jobs_to_process: int | None = None
    active_workers: int | None = None
    jobs_done: int | None = None
    new_jobs: int | None = None
