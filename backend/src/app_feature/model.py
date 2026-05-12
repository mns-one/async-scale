from pydantic import BaseModel, Field

class SimPayload(BaseModel):
    client_id: str
    size: int = Field(gt=0, le=500)
    interval: int = Field(gt=0, le=5)
    target: int = Field(gt=0, le=90)

class StatsPayload(BaseModel):
    jobs_to_process: int | None = None
    active_workers: int | None = None
    jobs_done: int | None = None
    new_jobs: int | None = None
