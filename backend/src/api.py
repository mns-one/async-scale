from fastapi import FastAPI
from src.app_feature.controller import router as main_router

def register_routes(app: FastAPI):
    app.include_router(main_router)