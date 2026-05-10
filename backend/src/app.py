from fastapi import FastAPI, Depends
from typing import Annotated
from .api import register_routes
from .database.engine import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from .database import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

db_dependency = Annotated[Session, Depends(get_db)]

register_routes(app)