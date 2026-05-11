from pydantic import BaseModel, Field

class SimPayload(BaseModel):
    client_id: str
    size: int = Field(gt=0, le=500)
    interval: int = Field(gt=0, le=5)
    target: int = Field(gt=0, le=90)